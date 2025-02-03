from typing import List

from sqlmodel import SQLModel


# Pydantic Models
class PayloadCreate(SQLModel):
    list_1: List[str]
    list_2: List[str]
