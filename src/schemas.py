from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class WalletChecked(BaseModel):
    id: int
    address: str
    balance: Decimal
    energy: int
    bandwidth: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
