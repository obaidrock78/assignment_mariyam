from sqlmodel import SQLModel, Field, Column, JSON
from typing import List, Optional
from datetime import datetime
import uuid


class TransformerCache(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    original_string: str = Field(unique=True)
    transformed_string: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Payload(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hash: str = Field(unique=True, index=True)
    list_1: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    list_2: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    output: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
