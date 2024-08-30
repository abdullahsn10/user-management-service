from fastapi import APIRouter, Depends, HTTPException, status
from src import schemas
from sqlalchemy.orm import Session
from src.settings.database import get_db
from src.security.oauth2 import require_role
from src.models.user import UserRole
from src.exceptions.exception import UserManagementServiceException
from src.utils.control_access import check_if_user_can_access_shop
from src.helpers import report
from datetime import date

router = APIRouter(tags=["Reports"], prefix="/reports")


@router.get(
    "/coffee-shops/{coffee_shop_id}/new-customers",
    response_model=schemas.NewCustomersReport,
)
def list_new_customers_endpoint(
    coffee_shop_id: int,
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(require_role([UserRole.ADMIN])),
):
    """
    GET endpoint to list number of new customers in a given period
    """
    try:
        check_if_user_can_access_shop(
            user_coffee_shop_id=current_user.coffee_shop_id,
            target_coffee_shop_id=coffee_shop_id,
        )
        return report.list_new_customers(
            db=db,
            coffee_shop_id=coffee_shop_id,
            from_date=from_date,
            to_date=to_date,
        )
    except UserManagementServiceException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
