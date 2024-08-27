from fastapi import FastAPI
from src.routers import (
    authentication,
    coffee_shop,
    customer,
    user,
)


app = FastAPI()

# register routes
app.include_router(authentication.router)
app.include_router(coffee_shop.router)
