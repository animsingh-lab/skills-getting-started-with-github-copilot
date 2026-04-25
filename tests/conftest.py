"""
Test configuration and fixtures for the FastAPI application.
"""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to the initial in-memory state between tests."""
    original_state = {
        name: {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": activity["participants"].copy(),
        }
        for name, activity in activities.items()
    }

    yield

    for name, activity in original_state.items():
        activities[name] = activity
