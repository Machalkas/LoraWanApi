from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database_clients.postgres_client import Base


class EnergyMeterRoom(Base):
    __tablename__ = "energy_meter_rooms"
    id = Column(Integer, primary_key=True, index=True)
    device_serial = Column(String(100), unique=True)
    room = Column(String(20))

    energy_meter = relationship("EnergyMeter", back_populates="energy_meter_room")


class EnergyMeter(Base):
    __tablename__ = "energy_meters"
    id = Column(Integer, primary_key=True, index=True)
    device_eui = Column(String, unique=True)
    device_id = Column(Integer, ForeignKey("energy_meter_rooms.id"), default=None)
    is_active = Column(Boolean, default=True)

    energy_meter_room = relationship("EnergyMeterRoom", back_populates="energy_meter")
    user_energy_meter = relationship("UsersEnergyMeters", back_populates="energy_meter")
