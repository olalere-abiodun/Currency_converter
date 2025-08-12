from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from typing import Optional
from sqlalchemy import or_

# CRUD 
# CREATE USER 
def sign_up(db:Session, user:schemas.UserRegister, hashed_password:str):
    db_user = models.Users (
        fullname = user.fullname,
        email = user.email,
        hashed_password = hashed_password,
        preferences = user.preferences
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# CHECK_EMAIL AND USERNAME

def check_user(db: Session, email: str = None, username: str = None, use_or: bool = False):
    query = db.query(models.Users)
    
    if email and username:
        if use_or:
            query = query.filter(or_(models.Users.email == email, models.Users.username == username))
        else:
            query = query.filter(models.Users.email == email, models.Users.username == username)
    elif email:
        query = query.filter(models.Users.email == email)
    elif username:
        query = query.filter(models.Users.username == username)
    
    return query.first()

# Get  User rate hsitory from DB 
def get_user_rate_history(db: Session, user_id: int):
    query = db.query(models.HistoricalRate).filter(models.HistoricalRate.user_id == user_id).order_by(models.HistoricalRate.date.desc()).all()
    if not query:
        raise HTTPException(status_code=404, detail="No historical rates found for this user")
    return query

# Save favorite pair
def save_favorite_pair(db: Session, user_id: int, base_currency: str, target_currency: str):
    existing = db.query(models.FavoritePair).filter(models.FavoritePair.user_id == user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already has a favorite pair")
    favorite = models.FavoritePair(
        base_currency=base_currency.upper(),
        target_currency=target_currency.upper(),
        user_id=user_id
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

# get user favorite pair 
def get_user_favorite_pairs(db: Session, user_id: int):
    favorites = db.query(models.FavoritePair).filter(models.FavoritePair.user_id == user_id).all()
    if not favorites:
        raise HTTPException(status_code=404, detail="No favorite pairs found for this user")
    return favorites




