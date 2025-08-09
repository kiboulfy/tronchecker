import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from tronpy.providers import HTTPProvider

from src.database.crud import create_wallet_record
from src.database.models import Base, WalletInfo
from src.database.session import engine, get_db
from src.schemas import WalletChecked

Base.metadata.create_all(bind=engine)

app = FastAPI(title="tronchecker")


load_dotenv()

api_key = os.getenv("TRON_API_KEY")

client = Tron(provider=HTTPProvider(api_key=api_key))


@app.post("/wallet", response_model=WalletChecked)
def check_wallet(data: str, db: Annotated[Session, Depends(get_db)]) -> WalletChecked:
    try:
        balance = client.get_account_balance(data)
        bandwidth = client.get_bandwidth(data)
        energy = client.get_energy(data)
    except AddressNotFound as err:
        raise HTTPException(status_code=404, detail="Wallet address not found") from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err

    return create_wallet_record(
        db=db,
        wallet_data=data,
        balance=balance,
        energy=energy,
        bandwidth=bandwidth,
    )


@app.get("/wallets", response_model=list[WalletChecked])
def get_wallets(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
) -> list[WalletChecked]:
    wallets = db.query(WalletInfo).offset(skip).limit(limit).all()
    return [WalletChecked.model_validate(w) for w in wallets]
