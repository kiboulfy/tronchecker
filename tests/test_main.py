from http import HTTPStatus

from fastapi.testclient import TestClient

from src.main import app
from src.schemas import WalletChecked

client = TestClient(app=app)


# This way of asserting is required because data can change regardless
def test_check_wallet() -> None:
    response = client.post("/wallet/", params={"data": "THUE6WTLaEGytFyuGJQUcKc3r245UKypoi"})
    assert response.status_code == HTTPStatus.OK
    assert WalletChecked.model_validate(response.json())


# Mock is better but it's enough by now
def test_get_wallets() -> None:
    response = client.get("/wallets/")
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)


def test_check_wallet_bad_addr() -> None:
    response = client.post("/wallet/", params={"data": "THUE6WTLaEGytFyuGJQUcKc3r245Uypoi"})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Wallet address not found"}
