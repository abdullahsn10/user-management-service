from fastapi import FastAPI
from src.routers import (
    authentication,
    coffee_shop,
    customer,
    user,
)


app = FastAPI()

# register routes


