import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.router import auth_utils
from app.dependencies import get_db
from typing import Optional, List

router = APIRouter(prefix="/alert", tags=["Alert Operations"])

# Create alert 
@router.post("/create_alert", response_model=schemas.AlertResponse)
def create_alert(
    alert: schemas.AlertCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_utils.get_current_user)
):
    created_alert = crud.create_alert(db=db, alert=alert, user_id=current_user.id)
    return created_alert

# get all alert for a user
@router.get("/get_user_alerts", response_model=List[schemas.AlertResponse])
def get_user_alerts(
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_utils.get_current_user)
):
    alerts = crud.get_user_alerts(db=db, user_id=current_user.id)
    return alerts

#delete an alert
@router.delete("/delete_alert/{alert_id}", response_model=dict)
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_utils.get_current_user)
):
    return crud.delete_alert(db=db, alert_id=alert_id, user_id=current_user.id)
