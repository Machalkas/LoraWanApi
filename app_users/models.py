from fastapi import APIRouter, Depends
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database_clients.postgres_client import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String(100), primary_key=True, unique=True)
    email = Column(String(100), unique=True, nullable=True)
    hashed_password = Column(String(200), nullable=False)

    user_energy_meter = relationship("UsersEnergyMeters", back_populates="user")


class UsersEnergyMeters(Base):
    __tablename__ = "users_energy_meters"

    id = Column(Integer, primary_key=True, index=True)
    user_username = Column(String, ForeignKey("users.username"))
    energy_meter_id = Column(Integer, ForeignKey("energy_meters.id"))

    energy_meter = relationship("EnergyMeter", back_populates="user_energy_meter")
    user = relationship("User", back_populates="user_energy_meter")
