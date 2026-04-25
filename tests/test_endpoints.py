"""
Tests for the FastAPI endpoints in the Mergington High School API.
"""


def test_root_redirects_to_index(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client, reset_activities):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_has_correct_structure(client, reset_activities):
    response = client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_signup_successful(client, reset_activities):
    response = client.post("/activities/Basketball Team/signup?email=student@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    response = client.get("/activities")
    assert "student@mergington.edu" in response.json()["Basketball Team"]["participants"]


def test_signup_activity_not_found(client, reset_activities):
    response = client.post("/activities/Nonexistent Club/signup?email=student@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_signup(client, reset_activities):
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_full(client, reset_activities):
    from app import activities

    activity = activities["Debate Club"]
    activity["participants"] = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]

    response = client.post("/activities/Debate Club/signup?email=full_test@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]


def test_unregister_successful(client, reset_activities):
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    response = client.get("/activities")
    assert email not in response.json()["Chess Club"]["participants"]


def test_unregister_activity_not_found(client, reset_activities):
    response = client.delete("/activities/Nonexistent Club/unregister?email=student@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_student_not_signed_up(client, reset_activities):
    response = client.delete("/activities/Basketball Team/unregister?email=not_registered@mergington.edu")
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]
