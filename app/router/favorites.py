import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.router import auth_utils
from app.dependencies import get_db
from typing import Optional, List

router = APIRouter(prefix="/favorites", tags=["Favorite Operations"])

# add favorite pairs to db 
@router.post("/add_favorite", response_model=schemas.UserPreferencesResponse)
def add_favorite_pair(
    favorite: schemas.UserPreferences,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_utils.get_current_user)
):
    # Check if the user is authenticated
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    # Save favorite pair to database
    try:
        favorite_pair = crud.save_favorite_pair(
            db=db,
            user_id=current_user.id,
            base_currency=favorite.base_currency,
            target_currency=favorite.target_currency
        )
        return {"message": "Favorite pair added successfully", "favorites": [favorite_pair]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-favorites", response_model=schemas.UserPreferencesResponse)
def get_user_favorites(
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_utils.get_current_user)
):
    mypairs = crud.get_user_favorite_pairs(db, current_user.id)
    if not mypairs:
        raise HTTPException(status_code=404, detail="No favorite pairs found for this user")
    return {"message": "Favorite pairs retrieved successfully", "favorites": mypairs}
