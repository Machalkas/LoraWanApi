from sqlalchemy.orm import Session
from . import models, schemas


def create_energy_meter_room(db: Session, energy_meter_room: schemas.EnergyMeterRoomCreateSchema):
    db_energy_meter_room = models.EnergyMeterRoom(device_serial=energy_meter_room.device_serial,
                                                  room=energy_meter_room.room)
    db.add(db_energy_meter_room)
    db.commit()
    db.refresh(db_energy_meter_room)
    return db_energy_meter_room


def get_energy_meter_room(db: Session, id: int):
    return db.query(models.EnergyMeterRoom).filter(models.EnergyMeterRoom.id == id).first()


def get_energy_meter_room_by_device_serial(db: Session, device_serial: str):
    return db.query(models.EnergyMeterRoom).filter(models.EnergyMeterRoom.device_serial == device_serial).first()


def get_energy_meter_room_list(db: Session):
    return db.query(models.EnergyMeterRoom).all()

def get_energy_meter_list(db: Session):
    return db.query(models.EnergyMeter).all()
