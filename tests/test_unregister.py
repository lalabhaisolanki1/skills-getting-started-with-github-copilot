"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
"""

import pytest


def test_unregister_successful(client, mock_activities):
    """Test successful unregister from an activity."""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=" + email
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]


def test_unregister_removes_participant(client, mock_activities):
    """Test that unregister actually removes the participant."""
    email = "michael@mergington.edu"
    
    # Get count before unregister
    response_before = client.get("/activities")
    activities_before = response_before.json()
    count_before = len(activities_before["Chess Club"]["participants"])
    
    # Unregister
    client.delete("/activities/Chess%20Club/unregister?email=" + email)
    
    # Get count after unregister
    response_after = client.get("/activities")
    activities_after = response_after.json()
    count_after = len(activities_after["Chess Club"]["participants"])
    
    # Verify participant was removed
    assert count_after == count_before - 1
    assert email not in activities_after["Chess Club"]["participants"]


def test_unregister_student_not_registered_returns_error(client, mock_activities):
    """Test that unregistering a student who isn't signed up returns error."""
    email = "notregistered@mergington.edu"
    
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=" + email
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"].lower()


def test_unregister_invalid_activity_returns_404(client, mock_activities):
    """Test that unregistering from non-existent activity returns 404."""
    response = client.delete(
        "/activities/NonExistent%20Activity/unregister?email=student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_preserves_other_participants(client, mock_activities):
    """Test that unregistering one student doesn't affect others."""
    email_to_remove = "michael@mergington.edu"
    
    # Get other participants
    response = client.get("/activities")
    activities = response.json()
    other_participants = [p for p in activities["Chess Club"]["participants"] if p != email_to_remove]
    
    # Unregister
    client.delete("/activities/Chess%20Club/unregister?email=" + email_to_remove)
    
    # Verify other participants still there
    response = client.get("/activities")
    activities = response.json()
    current_participants = activities["Chess Club"]["participants"]
    
    for participant in other_participants:
        assert participant in current_participants


def test_unregister_then_signup_again(client, mock_activities):
    """Test that a student can unregister and then sign up again."""
    email = "testuser@mergington.edu"
    
    # Sign up
    response1 = client.post("/activities/Chess%20Club/signup?email=" + email)
    assert response1.status_code == 200
    
    # Unregister
    response2 = client.delete("/activities/Chess%20Club/unregister?email=" + email)
    assert response2.status_code == 200
    
    # Sign up again
    response3 = client.post("/activities/Chess%20Club/signup?email=" + email)
    assert response3.status_code == 200
    
    # Verify signed up
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]
