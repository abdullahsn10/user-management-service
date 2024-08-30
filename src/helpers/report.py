from datetime import date
from sqlalchemy.orm import Session
from src import schemas, models


def list_new_customers(
    db: Session, coffee_shop_id: int, from_date: date, to_date: date
) -> schemas.NewCustomersReport:
    """
    This helper function lists all new customers along with their first order date
    *Args:
        db (Session): SQLAlchemy Session
        coffee_shop_id (int): coffee shop id to filter customers
        from_date (date): start date to filter orders
        to_date (date): end date to filter orders
    *Returns:
        NewCustomersReport : number of new customers
    """
    query = db.query(models.Customer).filter(
        models.Customer.coffee_shop_id == coffee_shop_id,
        models.Customer.created >= from_date,
        models.Customer.created <= to_date,
    )
    number_of_new_customers = query.count()

    new_customers = query.all()
    return schemas.NewCustomersReport(
        number_of_new_customers=number_of_new_customers, new_customers=new_customers
    )
