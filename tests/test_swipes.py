from tests.conftest import register, login, auth_headers, seed_candidate


class TestSwipes:
    def _setup(self, client, db):
        register(client)
        token = login(client)
        candidate = seed_candidate(db)
        return token, candidate

    def test_swipe_right_success(self, client, db):
        token, candidate = self._setup(client, db)
        resp = client.post(f"/swipes/{candidate.id}",
                           json={"direction": "right"},
                           headers=auth_headers(token))
        assert resp.status_code == 201
        data = resp.json()
        assert data["direction"] == "right"
        assert data["candidate_id"] == candidate.id
        assert data["candidate"]["name"] == candidate.name
        assert "swiped_at" in data

    def test_swipe_left_success(self, client, db):
        token, candidate = self._setup(client, db)
        resp = client.post(f"/swipes/{candidate.id}",
                           json={"direction": "left"},
                           headers=auth_headers(token))
        assert resp.status_code == 201
        assert resp.json()["direction"] == "left"

    def test_swipe_requires_auth(self, client, db):
        candidate = seed_candidate(db)
        resp = client.post(f"/swipes/{candidate.id}", json={"direction": "right"})
        assert resp.status_code == 403

    def test_swipe_invalid_candidate(self, client, db):
        register(client)
        token = login(client)
        resp = client.post("/swipes/9999",
                           json={"direction": "right"},
                           headers=auth_headers(token))
        assert resp.status_code == 404

    def test_swipe_duplicate_rejected(self, client, db):
        token, candidate = self._setup(client, db)
        client.post(f"/swipes/{candidate.id}",
                    json={"direction": "right"},
                    headers=auth_headers(token))
        resp = client.post(f"/swipes/{candidate.id}",
                           json={"direction": "left"},
                           headers=auth_headers(token))
        assert resp.status_code == 409
        assert "already swiped" in resp.json()["detail"]

    def test_swipe_invalid_direction(self, client, db):
        token, candidate = self._setup(client, db)
        resp = client.post(f"/swipes/{candidate.id}",
                           json={"direction": "up"},
                           headers=auth_headers(token))
        assert resp.status_code == 422

    def test_right_swipe_creates_matchmaker(self, client, db):
        from app import models
        token, candidate = self._setup(client, db)
        client.post(f"/swipes/{candidate.id}",
                    json={"direction": "right"},
                    headers=auth_headers(token))
        mm = db.query(models.Matchmaker).first()
        assert mm is not None
        assert mm.candidate_id == candidate.id
        assert mm.status == models.MatchmakerStatusEnum.pending

    def test_left_swipe_does_not_create_matchmaker(self, client, db):
        from app import models
        token, candidate = self._setup(client, db)
        client.post(f"/swipes/{candidate.id}",
                    json={"direction": "left"},
                    headers=auth_headers(token))
        assert db.query(models.Matchmaker).count() == 0

    def test_different_users_can_swipe_same_candidate(self, client, db):
        candidate = seed_candidate(db)
        register(client, email="user1@test.com")
        token1 = login(client, email="user1@test.com")
        register(client, email="user2@test.com")
        token2 = login(client, email="user2@test.com")

        resp1 = client.post(f"/swipes/{candidate.id}",
                            json={"direction": "right"},
                            headers=auth_headers(token1))
        resp2 = client.post(f"/swipes/{candidate.id}",
                            json={"direction": "left"},
                            headers=auth_headers(token2))
        assert resp1.status_code == 201
        assert resp2.status_code == 201


class TestSwipeHistory:
    def test_get_swipe_history_empty(self, client):
        register(client)
        token = login(client)
        resp = client.get("/swipes", headers=auth_headers(token))
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_swipe_history_returns_own_swipes(self, client, db):
        register(client)
        token = login(client)
        c1 = seed_candidate(db, name="Alice")
        c2 = seed_candidate(db, name="Bob", gender="male")
        client.post(f"/swipes/{c1.id}", json={"direction": "right"}, headers=auth_headers(token))
        client.post(f"/swipes/{c2.id}", json={"direction": "left"}, headers=auth_headers(token))

        resp = client.get("/swipes", headers=auth_headers(token))
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 2
        names = {r["candidate"]["name"] for r in results}
        assert names == {"Alice", "Bob"}
        directions = {r["candidate"]["name"]: r["direction"] for r in results}
        assert directions["Alice"] == "right"
        assert directions["Bob"] == "left"

    def test_get_swipe_history_isolated_per_user(self, client, db):
        candidate = seed_candidate(db)
        register(client, email="user1@test.com")
        token1 = login(client, email="user1@test.com")
        register(client, email="user2@test.com")
        token2 = login(client, email="user2@test.com")

        client.post(f"/swipes/{candidate.id}",
                    json={"direction": "right"},
                    headers=auth_headers(token1))

        resp = client.get("/swipes", headers=auth_headers(token2))
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_swipe_history_requires_auth(self, client):
        resp = client.get("/swipes")
        assert resp.status_code == 403
