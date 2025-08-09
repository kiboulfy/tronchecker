from decimal import Decimal

from sqlalchemy.orm import Session

from src.schemas import WalletChecked

from .models import WalletInfo


def create_wallet_record(
    db: Session,
    wallet_data: str,
    balance: Decimal,
    energy: int,
    bandwidth: int,
) -> WalletChecked:
    db_wallet = WalletInfo(
        address=wallet_data,
        balance=balance,
        energy=energy,
        bandwidth=bandwidth,
    )
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return WalletChecked.model_validate(db_wallet)
