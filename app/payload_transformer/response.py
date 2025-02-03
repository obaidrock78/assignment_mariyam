from sqlmodel import SQLModel
import uuid


class PayloadRead(SQLModel):
    id: uuid.UUID
    output: str
