from fastapi import APIRouter, Depends, HTTPException, status, Response
from src import schemas
from src.settings.database import get_db
from src.helpers import authentication
from src.exceptions.exception import UserManagementServiceException
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth",
)


@router.post("/signup", response_model=schemas.UserCredentialsResponse)
def signup_endpoint(
    request: schemas.SignUpRequestBody,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    POST endpoint to signup a new coffee shop into the system, also create an admin user for the registered coffee shop
    """
    try:
        response.status_code = status.HTTP_201_CREATED
        return authentication.signup(request=request, db=db)
    except UserManagementServiceException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/login", response_model=schemas.Token)
def login_endpoint(request: schemas.LoginRequestBody, db: Session = Depends(get_db)):
    """
    POST endpoint to login a user into the system
    """
    try:
        return authentication.login(request=request, db=db)
    except UserManagementServiceException as se:
        raise HTTPException(status_code=se.status_code, detail=se.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
