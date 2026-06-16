def test_signup_unregister_and_signup_again_flow(client):
    activity = "Soccer Club"
    email = "journey.student@mergington.edu"

    signup_response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": email},
    )
    assert unregister_response.status_code == 200

    second_signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )
    assert second_signup_response.status_code == 200
