import pytest

ACTIVITY = "Chess Club"
EMAIL = "student@example.com"


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert ACTIVITY in data


def test_signup_success(client):
    response = client.post(f"/activities/{ACTIVITY}/signup", params={"email": EMAIL})
    assert response.status_code == 200
    # Check participant added
    activities = client.get("/activities").json()
    assert EMAIL in activities[ACTIVITY]["participants"]


def test_signup_duplicate(client):
    client.post(f"/activities/{ACTIVITY}/signup", params={"email": EMAIL})
    response = client.post(f"/activities/{ACTIVITY}/signup", params={"email": EMAIL})
    assert response.status_code == 400


def test_signup_nonexistent_activity(client):
    response = client.post("/activities/Nonexistent/signup", params={"email": EMAIL})
    assert response.status_code == 404


def test_unregister_success(client):
    client.post(f"/activities/{ACTIVITY}/signup", params={"email": EMAIL})
    response = client.delete(f"/activities/{ACTIVITY}/unregister", params={"email": EMAIL})
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert EMAIL not in activities[ACTIVITY]["participants"]


def test_unregister_nonexistent_email(client):
    response = client.delete(f"/activities/{ACTIVITY}/unregister", params={"email": "notfound@example.com"})
    assert response.status_code == 400


def test_unregister_nonexistent_activity(client):
    response = client.delete("/activities/Nonexistent/unregister", params={"email": EMAIL})
    assert response.status_code == 404
