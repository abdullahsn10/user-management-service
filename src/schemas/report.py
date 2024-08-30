from pydantic import BaseModel
from src.schemas.customer import CustomerResponse


class NewCustomersReport(BaseModel):
    """
    pydantic model for new customers report
    """

    number_of_new_customers: int
    new_customers: list[CustomerResponse]

    class Config:
        orm_mode = True
