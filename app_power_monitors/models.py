from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database_clients.postgres_client import Base


class MonitorRoom(Base):
    __tablename__ = "monitors_rooms"
    id = Column(Integer, primary_key=True, index=True)
    device_serial = Column(String, unique=True)
    room = Column(String)

    monitor = relationship("Monitor", back_populates="monitor_room")


class Monitor(Base):
    __tablename__ = "monitors"
    id = Column(Integer, primary_key=True, index=True)
    device_eui = Column(String, unique=True)
    device_id = Column(Integer, ForeignKey("monitors_rooms.id"), default=None)
    is_active = Column(Boolean, default=True)

    monitor_room = relationship("MonitorRoom", back_populates="monitor")
