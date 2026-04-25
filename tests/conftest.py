"""
Pytest configuration and fixtures for FastAPI tests.
"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a TestClient instance for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_activities(monkeypatch):
    """
    Create a fresh copy of activities for each test.
    This prevents test data from being shared between tests.
    """
    fresh_activities = copy.deepcopy(activities)
    monkeypatch.setattr("src.app.activities", fresh_activities)
    return fresh_activities
