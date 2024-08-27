from sqlalchemy.orm import Session
from src import schemas, models
from src.utils.hashing import Hash
from src.exceptions.exception import *
from src.helpers import coffee_shop, branch
from typing import Union
from fastapi import status


def _is_user_exist(
    db: Session, email: str = None, phone_no: str = None, excluded_user_id: int = None
) -> bool:
    """
    This helper function used to check if a user exists by email or phone
    *Args:
        email (str): The email to check.
        phone_no (str) : The phone number of the user to check
        db (Session): A database session.
        excluded_user_id (int): The user id to exclude from the check.
    *Returns:
        bool: True if the user exists, False otherwise.
    """
    query = db.query(models.User)

    if email:
        query = query.filter(models.User.email == email)
    if phone_no:
        query = query.filter(models.User.phone_no == phone_no)
    if excluded_user_id:
        query = query.filter(models.User.id != excluded_user_id)

    return query.first() is not None


def _create_user(
    request: schemas.UserBase, role: models.UserRole, branch_id: int, db: Session
) -> models.User:
    """
    This helper function used to create a new user.
    *Args:
        request (UserBase): The user to create.
        role (UserRole): The role of the user to create.
        db (Session): A database session.
    *Returns:
        User: The created user.
    """
    # hash the user password
    request.password = Hash.bcrypt_hash(password=request.password)

    created_user_instance = models.User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone_no=request.phone_no,
        password=request.password,
        role=role,
        branch_id=branch_id,
    )
    db.add(created_user_instance)
    db.commit()
    db.refresh(created_user_instance)
    return created_user_instance


def find_user(
    db: Session,
    user_id: int = None,
    phone_no: str = None,
    email: str = None,
    coffee_shop_id: int = None,
    exclude_deleted: bool = True,
) -> models.User:
    """
    This helper function used to get a user by id, coffee_shop_id, ..etc
    *Args:
        user_id (int): The user id.
        phone (str): The phone number of the user.
        email (str): The email of the user.
        db (Session): A database session.
        coffee_shop_id (int): optional argument, if it's provided then this means to put it in the query also
        exclude_deleted (bool): optional argument, default True, if it's True then the query will exclude the deleted users
    *Returns:
        the User instance if exists, None otherwise.
    """
    query = db.query(models.User)

    if user_id:
        query = query.filter(models.User.id == user_id)
    elif phone_no:
        query = query.filter(models.User.phone_no == phone_no)
    elif email:
        query = query.filter(models.User.email == email)
    else:
        raise Exception("You must provide either user_id, phone_no, or email")

    if coffee_shop_id:
        query = query.join(models.Branch).filter(
            models.Branch.coffee_shop_id == coffee_shop_id
        )

    if exclude_deleted:
        query = query.filter(models.User.deleted == False)
    found_user = query.first()
    if not found_user:
        raise UserManagementServiceException(
            message=f"This user does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return found_user
