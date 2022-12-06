from sqlalchemy.orm import Session
from . import models, schemas


def create_monitor_room(db: Session, monitor_room: schemas.MonitorRoomCreateSchema):
    db_monitor_room = models.MonitorRoom(device_serial=monitor_room.device_serial, room=monitor_room.room)
    db.add(db_monitor_room)
    db.commit()
    db.refresh(db_monitor_room)
    return db_monitor_room


def get_monitor_room(db: Session, id: int):
    return db.query(models.MonitorRoom).filter(models.MonitorRoom.id == id).first()


def get_monitor_room_by_device_serial(db: Session, device_serial: str):
    return db.query(models.MonitorRoom).filter(models.MonitorRoom.device_serial == device_serial).first()


def get_monitor_room_list(db: Session):
    return db.query(models.MonitorRoom).all()
