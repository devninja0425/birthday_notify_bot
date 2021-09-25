from typing import Optional
from sqlmodel import Field, SQLModel


class Birthday(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    month: int
    day: int

    
