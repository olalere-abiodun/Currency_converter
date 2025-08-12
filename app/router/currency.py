import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_db
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.router import auth_utils
from typing import Optional
import httpx

load_dotenv()

router = APIRouter(prefix="/currency", tags=["Currency Operations"])


# Base URL for the exchange rate API
BASE_URL = os.getenv("XCHANGE_BASE_URL")
API_KEY = os.getenv("XCHANGE_API_KEY")


@router.get("/exchange-rate/{base_currency}/{target_currency}")
def get_exchange_rate(
    base_currency: str,
    target_currency: str,
    amount: float,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_utils.get_current_user)
):
    response = httpx.get(f"{BASE_URL}/convert", params={
        "from": base_currency.upper(),
        "to": target_currency.upper(),
        "amount": amount,
        "access_key": API_KEY
    })

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exchange rate not found")

    data = response.json()
    rate = data.get("info", {}).get("quote")
    converted_amount = data.get("result")
    
     # Save to database
    new_record = models.HistoricalRate(
        base_currency=base_currency.upper(),
        target_currency=target_currency.upper(),
        rate=rate,
        date=datetime.now(timezone.utc),
        user_id=current_user.id  # None if anonymous
    )
    db.add(new_record)
    db.commit()

    # return only the converted amount
    return {
    "converted_amount": f"{converted_amount} {target_currency.upper()}",
    "rate": rate
}

#Swap Currencies
@router.get("/reverse/{base_currency}/{target_currency}")
def reverse_exchange_rate(
    base_currency: str,
    target_currency: str,
    amount: float,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_utils.get_current_user)
):
    # Swap currencies
    swapped_base = target_currency.upper()
    swapped_target = base_currency.upper()

    response = httpx.get(f"{BASE_URL}/convert", params={
        "from": swapped_base,
        "to": swapped_target,
        "amount": amount,
        "access_key": API_KEY
    })

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exchange rate not found")

    data = response.json()
    rate = data.get("info", {}).get("quote")
    converted_amount = data.get("result")

    # Save to DB
    new_record = models.HistoricalRate(
        base_currency=swapped_base,
        target_currency=swapped_target,
        rate=rate,
        date=datetime.now(timezone.utc),
        user_id=current_user.id
    )
    db.add(new_record)
    db.commit()

    return {
        "converted_amount": f"{converted_amount} {swapped_target}"
    }



