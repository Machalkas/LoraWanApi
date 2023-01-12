from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserSchema, hashed_password: str) -> models.User:
    db_user = models.User(username=user.username, hashed_password=hashed_password, email=user.email, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def is_user_username_exists(db: Session, username: str) -> bool:
    return True if db.query(models.User).filter(models.User.username == username).scalar() is not None else False


def is_user_email_exists(db: Session, email: str) -> bool:
    return True if db.query(models.User).filter(models.User.email == email).scalar() is not None else False


def get_or_create_role(db: Session, name: str) -> models.Role:
    role = db.query(models.Role).filter(models.Role.name == name).first()
    if role is None:
        role = models.Role(name=name)
        db.add(role)
        db.commit()
        db.refresh(role)
    return role


def create_role(db: Session, role: str) -> models.Role:
    db_role = models.Role(name=role)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def is_role_exists(db: Session, name: str) -> bool:
    return True if db.query(models.Role).filter(models.Role.name == name).scalar() is not None else False
