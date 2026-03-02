from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(None, min_length=1, max_length=255)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
