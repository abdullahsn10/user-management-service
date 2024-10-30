from fastapi import FastAPI
from src.routers import authentication, coffee_shop, customer, user, report
from src.settings.settings import OPENAPI_URL, ROOT_PATH

app = FastAPI(
    openapi_url=OPENAPI_URL,
    root_path=ROOT_PATH,
)


# register routes
app.include_router(authentication.router)
app.include_router(coffee_shop.router)
app.include_router(user.router)
app.include_router(customer.router)
app.include_router(report.router)
