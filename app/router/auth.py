from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.dependencies import get_db
from app.router import auth_utils

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup")
def signup(user: schemas.UserRegister, db: Session = Depends(get_db)):
    # Check if email or username already exists
    if crud.check_user(db, email=user.email, username=user.username, use_or=True):
        raise HTTPException(status_code=400, detail="Email or username already taken")

    # Hash password
    hashed_password = auth_utils.pwd_context.hash(user.password)
    new_user = models.Users(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        fullname=user.fullname,
        preferences=user.preferences
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "username": new_user.username}


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth_utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_utils.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}
