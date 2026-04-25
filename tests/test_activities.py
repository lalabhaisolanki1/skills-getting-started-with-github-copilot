"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client, mock_activities):
    """Test that GET /activities returns all available activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Check that we have activities
    assert len(activities) > 0
    
    # Check that each activity has required fields
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_has_chess_club(client, mock_activities):
    """Test that GET /activities includes Chess Club activity."""
    response = client.get("/activities")
    activities = response.json()
    
    assert "Chess Club" in activities
    assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_get_activities_participants_are_lists(client, mock_activities):
    """Test that participants are returned as lists."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        participants = activity_data["participants"]
        assert isinstance(participants, list)
        # All participants should be strings (email addresses)
        for participant in participants:
            assert isinstance(participant, str)
