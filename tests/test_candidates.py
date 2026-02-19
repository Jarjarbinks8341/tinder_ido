from tests.conftest import register, login, auth_headers, seed_candidate


class TestCandidateSearch:
    def setup_method(self):
        pass  # fixtures handle setup

    def _token(self, client):
        register(client)
        return login(client)

    def test_search_requires_auth(self, client):
        resp = client.post("/candidates/search", json={})
        assert resp.status_code == 403

    def test_search_returns_all_when_no_filters(self, client, db):
        seed_candidate(db, name="Alice", gender="female", age=26)
        seed_candidate(db, name="Bob", gender="male", age=28)
        token = self._token(client)
        resp = client.post("/candidates/search", json={}, headers=auth_headers(token))
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_search_filter_by_gender(self, client, db):
        seed_candidate(db, name="Alice", gender="female", age=26)
        seed_candidate(db, name="Bob", gender="male", age=28)
        token = self._token(client)
        resp = client.post("/candidates/search",
                           json={"gender": "male"},
                           headers=auth_headers(token))
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 1
        assert results[0]["name"] == "Bob"

    def test_search_filter_by_min_age(self, client, db):
        seed_candidate(db, name="Young", gender="female", age=22)
        seed_candidate(db, name="Old", gender="female", age=35)
        token = self._token(client)
        resp = client.post("/candidates/search",
                           json={"min_age": 30},
                           headers=auth_headers(token))
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 1
        assert results[0]["name"] == "Old"

    def test_search_filter_by_max_age(self, client, db):
        seed_candidate(db, name="Young", gender="female", age=22)
        seed_candidate(db, name="Old", gender="female", age=35)
        token = self._token(client)
        resp = client.post("/candidates/search",
                           json={"max_age": 25},
                           headers=auth_headers(token))
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 1
        assert results[0]["name"] == "Young"

    def test_search_filter_by_age_range(self, client, db):
        seed_candidate(db, name="Young", gender="female", age=22)
        seed_candidate(db, name="Mid", gender="female", age=28)
        seed_candidate(db, name="Old", gender="female", age=35)
        token = self._token(client)
        resp = client.post("/candidates/search",
                           json={"min_age": 25, "max_age": 30},
                           headers=auth_headers(token))
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 1
        assert results[0]["name"] == "Mid"

    def test_search_filter_by_tags_single_match(self, client, db):
        seed_candidate(db, name="Hiker", tags="hiking,coffee")
        seed_candidate(db, name="Swimmer", tags="swimming,beach")
        token = self._token(client)
        resp = client.post("/candidates/search",
                           json={"tags": ["hiking"]},
                           headers=auth_headers(token))
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 1
        assert results[0]["name"] == "Hiker"

    def test_search_filter_by_tags_any_overlap(self, client, db):
        seed_candidate(db, name="Hiker", tags="hiking,coffee")
        seed_candidate(db, name="Swimmer", tags="swimming,beach")
        seed_candidate(db, name="Both", tags="hiking,beach")
        token = self._token(client)
        resp = client.post("/candidates/search",
                           json={"tags": ["hiking", "beach"]},
                           headers=auth_headers(token))
        assert resp.status_code == 200
        names = {r["name"] for r in resp.json()}
        assert names == {"Hiker", "Swimmer", "Both"}

    def test_search_combined_filters(self, client, db):
        seed_candidate(db, name="Match", gender="male", age=28, tags="hiking,coffee")
        seed_candidate(db, name="WrongGender", gender="female", age=28, tags="hiking")
        seed_candidate(db, name="WrongAge", gender="male", age=40, tags="hiking")
        seed_candidate(db, name="WrongTag", gender="male", age=28, tags="swimming")
        token = self._token(client)
        resp = client.post("/candidates/search",
                           json={"gender": "male", "min_age": 25, "max_age": 35, "tags": ["hiking"]},
                           headers=auth_headers(token))
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 1
        assert results[0]["name"] == "Match"

    def test_search_empty_result(self, client, db):
        seed_candidate(db, name="Alice", gender="female", age=26)
        token = self._token(client)
        resp = client.post("/candidates/search",
                           json={"gender": "male"},
                           headers=auth_headers(token))
        assert resp.status_code == 200
        assert resp.json() == []

    def test_search_invalid_age_filter(self, client):
        token = self._token(client)
        resp = client.post("/candidates/search",
                           json={"min_age": 10},
                           headers=auth_headers(token))
        assert resp.status_code == 422

    def test_search_excludes_already_swiped(self, client, db):
        c1 = seed_candidate(db, name="Alice", gender="female", age=26)
        c2 = seed_candidate(db, name="Bob", gender="male", age=28)
        token = self._token(client)

        # Swipe on Alice
        client.post(f"/swipes/{c1.id}", json={"direction": "right"}, headers=auth_headers(token))

        # Alice should no longer appear in search results
        resp = client.post("/candidates/search", json={}, headers=auth_headers(token))
        assert resp.status_code == 200
        names = {r["name"] for r in resp.json()}
        assert "Alice" not in names
        assert "Bob" in names

    def test_search_excludes_left_swiped_too(self, client, db):
        c1 = seed_candidate(db, name="Alice", gender="female", age=26)
        seed_candidate(db, name="Bob", gender="male", age=28)
        token = self._token(client)

        # Left-swipe on Alice — should still be hidden from search
        client.post(f"/swipes/{c1.id}", json={"direction": "left"}, headers=auth_headers(token))

        resp = client.post("/candidates/search", json={}, headers=auth_headers(token))
        names = {r["name"] for r in resp.json()}
        assert "Alice" not in names
