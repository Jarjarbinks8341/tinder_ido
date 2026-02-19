from tests.conftest import register, login, auth_headers


class TestRegister:
    def test_register_success(self, client):
        resp = register(client)
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "user@test.com"
        assert data["name"] == "Test User"
        assert data["gender"] == "female"
        assert data["age"] == 25
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data
        assert "password_hash" not in data

    def test_register_duplicate_email(self, client):
        register(client)
        resp = register(client)
        assert resp.status_code == 409
        assert "already registered" in resp.json()["detail"]

    def test_register_invalid_age_too_young(self, client):
        resp = register(client, age=17)
        assert resp.status_code == 422

    def test_register_invalid_age_too_old(self, client):
        resp = register(client, age=101)
        assert resp.status_code == 422

    def test_register_password_too_short(self, client):
        resp = register(client, password="abc")
        assert resp.status_code == 422

    def test_register_invalid_email(self, client):
        resp = register(client, email="not-an-email")
        assert resp.status_code == 422

    def test_register_creates_agent(self, client, db):
        from app import models
        register(client)
        agent = db.query(models.Agent).first()
        assert agent is not None
        assert agent.status == models.AgentStatusEnum.pending
        assert "Test User" in agent.name


class TestLogin:
    def test_login_success(self, client):
        register(client)
        resp = client.post("/auth/login", json={
            "email": "user@test.com", "password": "pass123"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        register(client)
        resp = client.post("/auth/login", json={
            "email": "user@test.com", "password": "wrongpass"
        })
        assert resp.status_code == 401

    def test_login_unknown_email(self, client):
        resp = client.post("/auth/login", json={
            "email": "nobody@test.com", "password": "pass123"
        })
        assert resp.status_code == 401

    def test_protected_route_requires_token(self, client):
        resp = client.get("/agent/me")
        assert resp.status_code == 403  # HTTPBearer returns 403 when no header

    def test_protected_route_rejects_bad_token(self, client):
        resp = client.get("/agent/me", headers={"Authorization": "Bearer badtoken"})
        assert resp.status_code == 401
