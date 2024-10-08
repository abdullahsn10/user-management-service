from sqlalchemy.orm import Session
from src import schemas, models
from src.exceptions import UserManagementServiceException
from fastapi import status


def _find_customer(
    db: Session,
    phone_no: str = None,
    customer_id: int = None,
    coffee_shop_id: int = None,
    exclude_customer_ids: list[int] = None,
) -> models.Customer:
    """
    This helper function used to get a customer by phone number/id and shop id.
    *Args:
        db (Session): SQLAlchemy Session object
        phone_no (str): Phone number to get a customer by phone number
        coffee_shop_id (int): Optional argument, to get the customer in this shop
        customer_id (int): the id of the customer
    *Returns:
        the Customer instance if exists, None otherwise.
    """
    query = db.query(models.Customer)

    if customer_id:
        query = query.filter(models.Customer.id == customer_id)
    elif phone_no:
        query = query.filter(models.Customer.phone_no == phone_no)
    else:
        raise Exception("phone_no or customer_id must be provided")
    if coffee_shop_id:
        query = query.filter(models.Customer.coffee_shop_id == coffee_shop_id)
    if exclude_customer_ids:
        query = query.filter(models.Customer.id.notin_(exclude_customer_ids))
    return query.first()


def get_or_create_customer(
    request: schemas.CustomerPOSTRequestBody,
    db: Session,
    coffee_shop_id: int,
) -> tuple[models.Customer, int]:
    """
    This helper function used to create a new customer if not exists in a specific shop,
     else returns that customer
    *Args:
        request (schemas.CustomerPOSTRequestBody): contains customer details
    *Returns:
        the Customer instance and status code (201 if created, 200 if exists)
    """
    customer_instance = _find_customer(
        db, phone_no=request.phone_no, coffee_shop_id=coffee_shop_id
    )
    status_code = status.HTTP_200_OK
    if not customer_instance:
        customer_instance = models.Customer(
            phone_no=request.phone_no,
            name=request.name,
            coffee_shop_id=coffee_shop_id,
        )
        db.add(customer_instance)
        db.commit()
        db.refresh(customer_instance)
        status_code = status.HTTP_201_CREATED
    return customer_instance, status_code


def _validate_customer_on_update(
    customer_id: int, coffee_shop_id: int, db: Session, customer_phone_no: str
) -> models.Customer:
    """
    This helper function used to validate the customer before updating, it checks if the customer exists
    and the phone number is unique.
    *Args:
        customer_id (int): the id of the customer needed to be updated
        coffee_shop_id (int): the id of the coffee shop in which the customer exists
        db (Session): SQLAlchemy Session object
        customer_phone_no (str): the phone number of the customer that must be unique
    *Returns:
        Raise Exceptions in case of violation, return the customer instance otherwise
    """

    found_customer = _find_customer(
        db=db, customer_id=customer_id, coffee_shop_id=coffee_shop_id
    )
    if not found_customer:
        raise UserManagementServiceException(
            message="Customer Not found", status_code=status.HTTP_404_NOT_FOUND
        )

    # validate customer phone number uniqueness
    if _find_customer(
        db=db,
        phone_no=customer_phone_no,
        coffee_shop_id=coffee_shop_id,
        exclude_customer_ids=[customer_id],
    ):
        raise UserManagementServiceException(
            message="Phone number already exists",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return found_customer


def update_customer(
    request: schemas.CustomerPUTRequestBody,
    db: Session,
    coffee_shop_id: int,
    customer_id: int,
) -> schemas.CustomerResponse:
    """
    This helper function used to validate and update user.
    *Args:
        request (UserPUTRequestBody): The user details to update
        db (Session): A database session.
        admin_coffee_shop_id (int): The coffee shop id of the admin who updated the user.
        user_id (int): the id of the user needed to be updated
    *Returns:
        CustomerResponse: The updated customer
    """

    customer_instance: models.Customer = _validate_customer_on_update(
        customer_id=customer_id,
        db=db,
        coffee_shop_id=coffee_shop_id,
        customer_phone_no=request.phone_no,
    )

    # Update all fields of the customer
    update_data = request.model_dump(
        exclude_unset=True
    )  # Get dictionary of all set fields in request
    for field, value in update_data.items():
        setattr(customer_instance, field, value)

    db.commit()
    db.refresh(customer_instance)
    return schemas.CustomerResponse(
        id=customer_instance.id,
        name=customer_instance.name,
        phone_no=customer_instance.phone_no,
        coffee_shop_id=customer_instance.coffee_shop_id,
        created=customer_instance.created,
    )


def find_all_customers(
    db: Session,
    coffee_shop_id: int,
    customer_phone_no: str = None,
    customer_name: str = None,
) -> list[models.Customer]:
    """
    This helper function used to get all customers or querying by phone number or name
    *Args:
        db (Session): SQLAlchemy Session object
        customer_phone_no (str): Phone number to get a customer by phone number
        customer_name (str): Name to get a customer by name
    *Returns:
        list[models.Customer]: List of customers
    """
    query = db.query(models.Customer).filter(
        models.Customer.coffee_shop_id == coffee_shop_id
    )
    if customer_phone_no:
        query = query.filter(models.Customer.phone_no == customer_phone_no)
    if customer_name:
        query = query.filter(models.Customer.name == customer_name)
    return query.all()


def get_customer_details(
    db: Session, customer_id: int, coffee_shop_id: int
) -> models.Customer:
    """
    This helper function used to get a customer by id
    *Args:
        db (Session): SQLAlchemy Session object
        customer_id (int): the id of the customer
        coffee_shop_id (int): the id of the coffee shop in which the customer exists
    *Returns:
        the customer instance if exists, raise exception otherwise
    """
    found_customer = _find_customer(
        db=db, customer_id=customer_id, coffee_shop_id=coffee_shop_id
    )
    if not found_customer:
        raise UserManagementServiceException(
            message="Customer Not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return found_customer
