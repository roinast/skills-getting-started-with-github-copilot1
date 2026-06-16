def test_signup_success(client):
    email = "new.student@mergington.edu"
    activity = "Chess Club"

    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]


def test_signup_rejects_duplicate_participant(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"

    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_unknown_activity(client):
    response = client.post("/activities/Unknown Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_when_activity_is_full(client):
    activity = "Chess Club"
    emails_to_fill = [
        "fill1@mergington.edu",
        "fill2@mergington.edu",
        "fill3@mergington.edu",
        "fill4@mergington.edu",
        "fill5@mergington.edu",
        "fill6@mergington.edu",
        "fill7@mergington.edu",
        "fill8@mergington.edu",
        "fill9@mergington.edu",
        "fill10@mergington.edu",
    ]

    for email in emails_to_fill:
        fill_response = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert fill_response.status_code == 200

    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": "overflow@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
