from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserSchema, hashed_password: str):
    db_user = models.User(username=user.username, hashed_password=hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def is_username_exists(db: Session, username: str) -> bool:
    return True if db.query(models.User).filter(models.User.username == username).scalar() is not None else False


def is_email_exists(db: Session, email: str) -> bool:
    return True if db.query(models.User).filter(models.User.email == email).scalar() is not None else False


def create_user_energy_meter(db: Session, user_energy_meter: schemas.UsersEnergyMetersCreateSchema) -> models.UsersEnergyMeters:
    db_user_energy_meter = models.UsersEnergyMeters(user_energy_meter)
    db.add(db_user_energy_meter)
    db.commit()
    db.refresh(db_user_energy_meter)
    return db_user_energy_meter
