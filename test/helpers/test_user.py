from sqlalchemy.orm import Session
from src import models, schemas
from src.helpers import user as user_helper
from test.utils.data_utils import user, user_post_request_body, mock_db


def test_create_user(user: schemas.UserBase, mock_db: Session) -> None:
    """
    Test create_user function
    """
    created_user = user_helper._create_user(
        request=user, role=models.UserRole.ADMIN, branch_id=1, db=mock_db
    )

    assert created_user.first_name == user.first_name
    assert created_user.last_name == user.last_name
    assert created_user.email == user.email
    assert created_user.role == models.UserRole.ADMIN
    assert created_user.branch_id == 1
