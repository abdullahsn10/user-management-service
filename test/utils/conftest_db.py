from sqlalchemy.orm import Session
from unittest.mock import create_autospec
import pytest


@pytest.fixture
def mock_db() -> Session:
    """Pytest fixture to create a mock Session instance."""
    session = create_autospec(Session)
    return session
