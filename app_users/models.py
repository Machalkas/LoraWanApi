from fastapi import APIRouter, Depends
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database_clients.postgres_client import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String(100), primary_key=True, unique=True)
    email = Column(String(100), unique=True, nullable=True)
    hashed_password = Column(String(200), nullable=False)
    role = Column(String, ForeignKey("roles.name", ondelete="RESTRICT"), nullable=False)

    energy_meters_access_relation = relationship("EnergyMetersAccess", back_populates="user_relation")
    role_relation = relationship("Role", back_populates="user_relation")


class Role(Base):
    __tablename__ = "roles"

    name = Column(String, primary_key=True, unique=True)

    user_relation = relationship("User", back_populates="role_relation")
