"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_successful(client, mock_activities):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client, mock_activities):
    """Test that signup actually adds the participant to the activity."""
    email = "newstudent@mergington.edu"
    
    # Get activities before signup
    response_before = client.get("/activities")
    activities_before = response_before.json()
    participants_before = activities_before["Chess Club"]["participants"]
    
    # Sign up
    client.post("/activities/Chess%20Club/signup?email=" + email)
    
    # Get activities after signup
    response_after = client.get("/activities")
    activities_after = response_after.json()
    participants_after = activities_after["Chess Club"]["participants"]
    
    # Verify participant was added
    assert len(participants_after) == len(participants_before) + 1
    assert email in participants_after


def test_signup_duplicate_student_returns_error(client, mock_activities):
    """Test that signing up twice for the same activity returns an error."""
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    
    response = client.post(
        "/activities/Chess%20Club/signup?email=" + email
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_invalid_activity_returns_404(client, mock_activities):
    """Test that signing up for non-existent activity returns 404."""
    response = client.post(
        "/activities/NonExistent%20Activity/signup?email=student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_preserves_existing_participants(client, mock_activities):
    """Test that signup preserves existing participants."""
    email = "newstudent@mergington.edu"
    
    # Get original participants
    response = client.get("/activities")
    activities = response.json()
    original_participants = activities["Programming Class"]["participants"].copy()
    
    # Sign up to different activity
    client.post("/activities/Chess%20Club/signup?email=" + email)
    
    # Verify Programming Class participants unchanged
    response = client.get("/activities")
    activities = response.json()
    assert activities["Programming Class"]["participants"] == original_participants


def test_signup_multiple_students_to_same_activity(client, mock_activities):
    """Test that multiple different students can sign up for same activity."""
    email1 = "newstudent1@mergington.edu"
    email2 = "newstudent2@mergington.edu"
    
    response1 = client.post("/activities/Chess%20Club/signup?email=" + email1)
    response2 = client.post("/activities/Chess%20Club/signup?email=" + email2)
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Both should be in the activity
    response = client.get("/activities")
    activities = response.json()
    participants = activities["Chess Club"]["participants"]
    
    assert email1 in participants
    assert email2 in participants
