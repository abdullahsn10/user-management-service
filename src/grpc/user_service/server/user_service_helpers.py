from src import schemas
from fastapi import HTTPException, status
from src.security.jwt import verify_token
from src.exceptions.exception import UserManagementServiceException


def _extract_token_data(token: str) -> schemas.TokenData:
    """
    Verify the token and extracts data from it
    Args:
         token (str): the token to verify and extract
    Returns:
        TokenData: the extracted data
    """
    credentials_exception = UserManagementServiceException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message="Could not validate credentials",
    )
    return verify_token(token=token, credentials_exception=credentials_exception)
