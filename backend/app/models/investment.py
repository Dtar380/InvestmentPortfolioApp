from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class InvestmentBase(SQLModel):
    ticker: str = Field(index=True, nullable=False)
    market: str = Field(nullable=False)
    quantity: float = Field(nullable=False)
    timestamp: datetime = Field(nullable=False)


class Investment(InvestmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id", nullable=False)
    owner: "User" = Relationship(back_populates="investments")  # type: ignore
