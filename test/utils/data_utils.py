from src import models, schemas
import pytest

from sqlalchemy.orm import Session
from unittest.mock import create_autospec


@pytest.fixture
def user() -> schemas.UserBase:
    """
    Fixture to return a UserBase object
    """
    return schemas.UserBase(
        first_name="John",
        last_name="Doe",
        phone_no="1234567890",
        email="john@test.com",
        password="password",
    )


@pytest.fixture
def user_post_request_body() -> schemas.UserPOSTRequestBody:
    """
    Fixture to return a UserPOSTRequestBody object
    """
    return schemas.UserPOSTRequestBody(
        first_name="John",
        last_name="Doe",
        phone_no="1234567890",
        email="john@test.com",
        password="password",
        role=models.UserRole.ADMIN,
        branch_id=1,
    )


@pytest.fixture
def mock_db() -> Session:
    """Pytest fixture to create a mock Session instance."""
    session = create_autospec(Session)
    return session
