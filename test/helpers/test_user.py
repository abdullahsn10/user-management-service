from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.helpers import user as user_helper
from test.utils.conftest_user import *
from test.utils.conftest_db import mock_db


def test_create_user(user: schemas.UserBase, mock_db: Session) -> None:
    """
    Unit test for create_user helper function, this ensures the logic of the function is correct
    and the function behaves as expected. This test mocks the db session and its methods, so that
    the actual database is not used during the test, and the test is isolated. This means that the
    test not check the persistence of the data in the database, but rather the logic of the function.

    Args:
    - user (schemas.UserBase): A Pydantic UserBase object
    - mock_db (Session): A mock SQLAlchemy session object
    """

    # Mocking db.add, db.commit, db.refresh
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    # Call the actual function under test
    created_user = user_helper._create_user(
        request=user, role=models.UserRole.ADMIN, branch_id=1, db=mock_db
    )

    # Assertions to ensure the user is created with the correct data
    assert created_user.first_name == user.first_name
    assert created_user.last_name == user.last_name
    assert created_user.email == user.email
    assert created_user.role == models.UserRole.ADMIN
    assert created_user.branch_id == 1

    # Verify that db.add was called with the correct user model
    mock_db.add.assert_called_once()

    # Ensure db.commit and db.refresh were called once
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_is_user_exists(mock_db: Session) -> None:
    """
    Unit test for is_user_exists helper function.
    Args:
    - mock_db (Session): A mock SQLAlchemy session object
    """

    # Create mock objects for query, filter, and first (to simulate chain calls)
    mock_query = MagicMock()
    mock_db.query = MagicMock(return_value=mock_query)
    mock_query.filter = MagicMock(return_value=mock_query)
    mock_query.first = MagicMock(
        return_value=None
    )  # Adjust this as needed to simulate different scenarios

    # Call the actual function under test
    user_helper._is_user_exist(email="test@example.com", db=mock_db)

    # Verify that session methods were called with the correct arguments
    mock_db.query.assert_called_once_with(models.User)
    mock_query.filter.assert_called_once()
    mock_query.first.assert_called_once()
