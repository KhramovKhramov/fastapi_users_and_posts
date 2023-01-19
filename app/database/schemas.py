from pydantic import BaseModel, Field
from typing import Optional

class CorrectPost(BaseModel):
    title: str = Field(min_length=2)
    body: Optional[str]

    class Config:
        orm_mode = True