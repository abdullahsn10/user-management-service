from src import schemas
from fastapi import HTTPException, status
from src.security.jwt import verify_token


def _extract_token_data(token: str) -> schemas.TokenData:
    """
    Verify the token and extracts data from it
    Args:
         token (str): the token to verify and extract
    Returns:
        TokenData: the extracted data
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token=token, credentials_exception=credentials_exception)
