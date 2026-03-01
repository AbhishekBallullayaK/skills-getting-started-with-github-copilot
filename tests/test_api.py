from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_contains_initial_data():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # ensure known activity present
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_duplicate_prevention():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # ensure not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # duplicate should fail
    resp2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp2.status_code == 400


def test_unregister_endpoint():
    email = "toremove@mergington.edu"
    activity = "Chess Club"
    # make sure student is there
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]

    # second delete should give error
    resp2 = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp2.status_code == 400
