from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import models, crud, schemas, utils
from database_clients.postgres_client import SessionLocal, engine
import config

router = APIRouter()
models.Base.metadata.create_all(bind=engine)


@router.post("/token", response_model=schemas.TokenSchema)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(utils.get_db)):
    user = utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/registration", response_model=schemas.UserSchema)
async def user_registration(new_user: schemas.UserRegistrationSchema, db: Session = Depends(utils.get_db)):
    hashed_pass = utils.get_password_hash(new_user.password)
    return crud.create_user(db, schemas.UserSchema(username=new_user.username, email=new_user.email),
                            hashed_password=hashed_pass)


@router.get("/users/me/", response_model=schemas.UserSchema)
async def read_users_me(current_user: models.User = Depends(utils.get_current_user)):
    return current_user
