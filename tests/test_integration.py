"""
Integration test: full boy-browses-girls journey.

Scenario
--------
1. Seed a pool of girl candidates with varied profiles.
2. Alex (a boy) registers → his Agent is auto-created.
3. Alex searches for girls (no filters, then tag-filtered).
4. Alex swipes left on girls he's not interested in.
5. Alex swipes right on 3 girls he likes.
6. Verify each right-swipe created a Matchmaker record (status=pending),
   meaning the message was "delivered" to those girls' matchmakers.
7. Verify left-swipes produced no Matchmaker records.
8. Verify Alex's swipe history is complete and correct.
"""

import pytest
from tests.conftest import auth_headers, seed_candidate


# ---------------------------------------------------------------------------
# Fixture: seed a pool of female candidates
# ---------------------------------------------------------------------------

GIRL_PROFILES = [
    {"name": "Sophie Turner",  "age": 25, "tags": "hiking,coffee,travel",    "location": "NYC"},
    {"name": "Mia Chen",       "age": 27, "tags": "music,art,coffee",         "location": "LA"},
    {"name": "Ava Rodriguez",  "age": 24, "tags": "yoga,wellness,cooking",    "location": "Miami"},
    {"name": "Emma Park",      "age": 29, "tags": "hiking,photography,nature","location": "Denver"},
    {"name": "Luna Brooks",    "age": 26, "tags": "gaming,tech,coffee",       "location": "SF"},
]


@pytest.fixture()
def girl_pool(db):
    """Seed female candidates; return list ordered by insertion."""
    candidates = []
    for profile in GIRL_PROFILES:
        c = seed_candidate(
            db,
            name=profile["name"],
            gender="female",
            age=profile["age"],
            tags=profile["tags"],
            location=profile["location"],
        )
        candidates.append(c)
    return candidates


@pytest.fixture()
def alex(client):
    """Register Alex (a boy) and return his auth headers."""
    client.post("/auth/register", json={
        "email": "alex@example.com",
        "password": "secret123",
        "name": "Alex",
        "gender": "male",
        "age": 28,
    })
    resp = client.post("/auth/login", json={
        "email": "alex@example.com",
        "password": "secret123",
    })
    return auth_headers(resp.json()["access_token"])


# ---------------------------------------------------------------------------
# Integration test
# ---------------------------------------------------------------------------

class TestBoySwipesGirls:

    def test_full_journey(self, client, db, girl_pool, alex):
        # ── Step 1: Alex sees the full girl pool ─────────────────────────────
        resp = client.post("/candidates/search",
                           json={"gender": "female"},
                           headers=alex)
        assert resp.status_code == 200
        visible = resp.json()
        assert len(visible) == 5, "Alex should see all 5 girls"
        visible_names = {g["name"] for g in visible}
        assert visible_names == {p["name"] for p in GIRL_PROFILES}

        # ── Step 2: Alex narrows with a tag filter (coffee lovers) ────────────
        resp = client.post("/candidates/search",
                           json={"gender": "female", "tags": ["coffee"]},
                           headers=alex)
        assert resp.status_code == 200
        coffee_lovers = resp.json()
        coffee_names = {g["name"] for g in coffee_lovers}
        # Sophie, Mia, and Luna all have "coffee" in their tags
        assert coffee_names == {"Sophie Turner", "Mia Chen", "Luna Brooks"}

        # ── Step 3: Build the swipe plan ──────────────────────────────────────
        # Index by name for easy lookup
        pool_by_name = {c.name: c for c in girl_pool}

        likes    = ["Sophie Turner", "Emma Park", "Luna Brooks"]  # right swipe → 3 girls
        dislikes = ["Mia Chen", "Ava Rodriguez"]                  # left swipe

        # ── Step 4: Swipe left on girls Alex isn't interested in ─────────────
        for name in dislikes:
            cid = pool_by_name[name].id
            resp = client.post(f"/swipes/{cid}",
                               json={"direction": "left"},
                               headers=alex)
            assert resp.status_code == 201, f"Left-swipe on {name} failed"
            data = resp.json()
            assert data["direction"] == "left"
            assert data["candidate"]["name"] == name

        # ── Step 5: Swipe right on the 3 girls Alex likes ────────────────────
        for name in likes:
            cid = pool_by_name[name].id
            resp = client.post(f"/swipes/{cid}",
                               json={"direction": "right"},
                               headers=alex)
            assert resp.status_code == 201, f"Right-swipe on {name} failed"
            data = resp.json()
            assert data["direction"] == "right"
            assert data["candidate"]["name"] == name

        # ── Step 6: Swipe history is complete ────────────────────────────────
        resp = client.get("/swipes", headers=alex)
        assert resp.status_code == 200
        history = resp.json()
        assert len(history) == 5, "Alex should have 5 swipes total"

        history_map = {s["candidate"]["name"]: s["direction"] for s in history}
        for name in likes:
            assert history_map[name] == "right", f"{name} should be right-swiped"
        for name in dislikes:
            assert history_map[name] == "left", f"{name} should be left-swiped"

        # ── Step 7: Alex's Agent exists and is in pending state ───────────────
        resp = client.get("/agent/me", headers=alex)
        assert resp.status_code == 200
        agent = resp.json()
        assert agent["status"] == "pending"
        assert "Alex" in agent["name"]

        # ── Step 8: Matchmaker records created for the 3 right-swiped girls ──
        resp = client.get("/matchmaker", headers=alex)
        assert resp.status_code == 200
        matchmakers = resp.json()

        assert len(matchmakers) == 3, (
            f"Expected 3 matchmaker records (one per right-swipe), got {len(matchmakers)}"
        )

        # Every matchmaker record should be in 'pending' status
        # (awaiting the agent/AI to take action — the MVP placeholder)
        mm_candidate_names = {mm["candidate"]["name"] for mm in matchmakers}
        assert mm_candidate_names == set(likes), (
            f"Matchmaker records should exist for {likes}, got {mm_candidate_names}"
        )
        for mm in matchmakers:
            assert mm["status"] == "pending", (
                f"Matchmaker for {mm['candidate']['name']} should be pending"
            )
            assert mm["contact_notes"] is None, "No outreach notes yet in MVP"
            assert mm["agent_id"] == agent["id"]

        # ── Step 9: No matchmaker records for left-swiped girls ───────────────
        mm_names = {mm["candidate"]["name"] for mm in matchmakers}
        for name in dislikes:
            assert name not in mm_names, (
                f"{name} was left-swiped; should have no matchmaker record"
            )
