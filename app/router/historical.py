import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.router import auth_utils
from app.dependencies import get_db
from typing import Optional, List
import httpx

load_dotenv()

router = APIRouter(prefix="/historical", tags=["Historical Operations"])

# Base URL for the exchange rate API
BASE_URL = os.getenv("XCHANGE_BASE_URL")
API_KEY = os.getenv("XCHANGE_API_KEY")


@router.get("/historical")
def get_historical_rates(
    base_currency: str,
    target_currency: str,
    start_date: str,
    end_date: str,
    current_user: schemas.UserBase = Depends(auth_utils.get_current_user)
):
    base_currency = base_currency.upper()
    target_currency = target_currency.upper()

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if end < start:
        raise HTTPException(status_code=400, detail="End date must be after start date")

    rates = {}
    current = start

    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        response = httpx.get(f"{BASE_URL}/{date_str}", params={
            "from": base_currency,
            "to": target_currency,
            "access_key": API_KEY
        })

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Could not fetch rates for {date_str}")

        data = response.json()

        if not data.get("success", True):
            raise HTTPException(status_code=404, detail=data.get("error", {}).get("info", "Unknown error"))

        rates[date_str] = data["rates"][target_currency]
        current += timedelta(days=1)

    return {
        "base_currency": base_currency,
        "target_currency": target_currency,
        "rates": rates
    }




@router.get("/get-rate/{base_currency}/{target_currency}")
def get_exchange_rate(
    base_currency: str,
    target_currency: str,
    
):
    response = httpx.get(f"{BASE_URL}/convert", params={
        "from": base_currency.upper(),
        "to": target_currency.upper(),
        "amount": 1,
        "access_key": API_KEY
    })

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exchange rate not found")

    data = response.json()
    rate = data.get("info", {}).get("quote")
    converted_amount = data.get("result")
    
   

    # return only the converted amount
    return {
    "rate": rate
}

# Get History of user from database
@router.get("/user-history", response_model=List[schemas.UserHistoryResponse])
def get_user_history(
    current_user: schemas.UserBase = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    history = crud.get_user_rate_history(db, user_id)

    if not history:
        raise HTTPException(status_code=404, detail="No historical rates found for this user")

    return history


