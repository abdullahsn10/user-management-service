from typing import Dict
from src import schemas, models
from sqlalchemy.orm import Session
from src.exceptions.exception import *
from src.helpers import coffee_shop


def _create_branch(
    request: schemas.BranchBase, coffee_shop_id: int, db: Session
) -> models.Branch:
    """
    This helper function will be used to create a new branch
    *Args:
        request (schemas.BranchBase): schema instance that contains branch details
        db (Session): database session
        coffee_shop_id (int): id of the coffee shop to create the branch in
    *Returns:
        the created branch
    """
    # check if the shop exists
    found_shop = coffee_shop.find_coffee_shop(db=db, coffee_shop_id=coffee_shop_id)

    created_branch = models.Branch(
        name=request.name, location=request.location, coffee_shop_id=coffee_shop_id
    )
    db.add(created_branch)
    db.commit()
    db.refresh(created_branch)
    return created_branch


def find_branch(
    branch_id: int, db: Session, coffee_shop_id: int = None
) -> models.Branch:
    """
    This helper will be used to find a branch by id and coffee shop id
    *Args:
        branch_id (int): branch id to be found
        db (Session): database session
        coffee_shop_id (int): coffee shop id that the branch belongs to
    *Returns:
        the found branch or raise an exception if not found
    """
    query = db.query(models.Branch).filter(
        models.Branch.id == branch_id, models.Branch.deleted == False
    )

    if coffee_shop_id:
        query = query.filter(models.Branch.coffee_shop_id == coffee_shop_id)

    found_branch = query.first()
    if not found_branch:
        raise UserManagementServiceException(
            message=f"Branch with id={branch_id} does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return found_branch
