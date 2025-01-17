from typing import Optional

from pydantic import BaseModel, Field


class ApplicationCreate(BaseModel):
    user_name: str = Field(...)
    description: str = Field(...)

    class Config:
        json_schema_extra = {
            'example': {
                'user_name': 'John',
                'description': 'Hello, I am John. This is my example description.',
            }
        }


class ApplicationsListGet(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)
    user_name: Optional[str] = None
