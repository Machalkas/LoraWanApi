from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app_users.models import User

from database_clients.postgres_client import Base


class EnergyMeterRoom(Base):
    __tablename__ = "energy_meter_rooms"
    id = Column(Integer, primary_key=True, index=True)
    device_serial = Column(String(100), unique=True)
    room = Column(String(20))

    energy_meters_access_relation = relationship("EnergyMetersAccess", back_populates="energy_meter_relation")


class EnergyMeter(Base):
    __tablename__ = "energy_meters"
    id = Column(Integer, primary_key=True, index=True)
    device_eui = Column(String, unique=True)
    device = Column(String(100), unique=True)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class EnergyMetersAccess(Base):
    __tablename__ = "energy_meters_access"
    __table_args__ = (UniqueConstraint("user", "energy_meter", name="user_energy_meter_uniq"),)

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False)
    energy_meter = Column(Integer, ForeignKey("energy_meter_rooms.id", ondelete="CASCADE"), nullable=False)

    energy_meter_relation = relationship("EnergyMeterRoom", back_populates="energy_meters_access_relation")
    user_relation = relationship("User", back_populates="energy_meters_access_relation")
