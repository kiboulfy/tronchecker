from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class WalletInfo(Base):
    __tablename__ = "wallet_info"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    balance = Column(Numeric(18, 6))
    energy = Column(Integer)
    bandwidth = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
