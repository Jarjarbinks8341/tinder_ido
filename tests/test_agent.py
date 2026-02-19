from tests.conftest import register, login, auth_headers, seed_candidate


class TestAgent:
    def test_get_agent_requires_auth(self, client):
        resp = client.get("/agent/me")
        assert resp.status_code == 403

    def test_get_agent_created_on_register(self, client):
        register(client)
        token = login(client)
        resp = client.get("/agent/me", headers=auth_headers(token))
        assert resp.status_code == 200
        data = resp.json()
        assert data["user_id"] == 1
        assert data["status"] == "pending"
        assert "Test User" in data["name"]
        assert "id" in data
        assert "created_at" in data

    def test_each_user_has_own_agent(self, client):
        register(client, email="user1@test.com", name="Alice")
        token1 = login(client, email="user1@test.com")
        register(client, email="user2@test.com", name="Bob")
        token2 = login(client, email="user2@test.com")

        resp1 = client.get("/agent/me", headers=auth_headers(token1))
        resp2 = client.get("/agent/me", headers=auth_headers(token2))

        assert resp1.json()["id"] != resp2.json()["id"]
        assert "Alice" in resp1.json()["name"]
        assert "Bob" in resp2.json()["name"]


class TestMatchmaker:
    def test_get_matchmaker_requires_auth(self, client):
        resp = client.get("/matchmaker")
        assert resp.status_code == 403

    def test_matchmaker_empty_before_swipes(self, client):
        register(client)
        token = login(client)
        resp = client.get("/matchmaker", headers=auth_headers(token))
        assert resp.status_code == 200
        assert resp.json() == []

    def test_matchmaker_populated_after_right_swipe(self, client, db):
        register(client)
        token = login(client)
        candidate = seed_candidate(db, name="Alice", tags="hiking")

        client.post(f"/swipes/{candidate.id}",
                    json={"direction": "right"},
                    headers=auth_headers(token))

        resp = client.get("/matchmaker", headers=auth_headers(token))
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 1
        assert results[0]["status"] == "pending"
        assert results[0]["candidate"]["name"] == "Alice"
        assert results[0]["contact_notes"] is None

    def test_matchmaker_not_created_for_left_swipe(self, client, db):
        register(client)
        token = login(client)
        candidate = seed_candidate(db)

        client.post(f"/swipes/{candidate.id}",
                    json={"direction": "left"},
                    headers=auth_headers(token))

        resp = client.get("/matchmaker", headers=auth_headers(token))
        assert resp.status_code == 200
        assert resp.json() == []

    def test_matchmaker_multiple_right_swipes(self, client, db):
        register(client)
        token = login(client)
        c1 = seed_candidate(db, name="Alice")
        c2 = seed_candidate(db, name="Bob", gender="male")
        c3 = seed_candidate(db, name="Carol", gender="female", age=30)

        client.post(f"/swipes/{c1.id}", json={"direction": "right"}, headers=auth_headers(token))
        client.post(f"/swipes/{c2.id}", json={"direction": "left"}, headers=auth_headers(token))
        client.post(f"/swipes/{c3.id}", json={"direction": "right"}, headers=auth_headers(token))

        resp = client.get("/matchmaker", headers=auth_headers(token))
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 2
        names = {r["candidate"]["name"] for r in results}
        assert names == {"Alice", "Carol"}

    def test_matchmaker_isolated_per_user(self, client, db):
        candidate = seed_candidate(db)
        register(client, email="user1@test.com")
        token1 = login(client, email="user1@test.com")
        register(client, email="user2@test.com")
        token2 = login(client, email="user2@test.com")

        client.post(f"/swipes/{candidate.id}",
                    json={"direction": "right"},
                    headers=auth_headers(token1))

        resp = client.get("/matchmaker", headers=auth_headers(token2))
        assert resp.status_code == 200
        assert resp.json() == []
