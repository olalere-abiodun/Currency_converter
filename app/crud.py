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




