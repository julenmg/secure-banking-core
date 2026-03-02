from pydantic import BaseModel, Field, validator

class TransferRequest(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(...)

    @validator('amount')
    def check_amount(cls, v):
        if v <= 0:
            raise ValueError('El monto debe ser positivo')
        return v
