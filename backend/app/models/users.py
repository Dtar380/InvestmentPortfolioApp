from datetime import datetime, timezone
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, nullable=False)
    full_name: str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    phone: Optional[str] = None


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    investments: List["Investment"] = Relationship(back_populates="owner")  # type: ignore
