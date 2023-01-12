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


def add_energy_meters_access(db: Session, user_energy_meter: schemas.EnergyMetersAccessCreateSchema) -> models.EnergyMetersAccess:
    db_user_energy_meter = models.EnergyMetersAccess(user=user_energy_meter.user,
                                                     energy_meter=user_energy_meter.energy_meter)
    db.add(db_user_energy_meter)
    db.commit()
    db.refresh(db_user_energy_meter)
    return db_user_energy_meter


def remove_energy_meters_access(db: Session, username: str, energy_meter_id: int):
    energy_meter = db.query(models.EnergyMetersAccess).filter(
        models.EnergyMetersAccess.user == username,
        models.EnergyMetersAccess.energy_meter == energy_meter_id
    ).scalar()
    db.delete(energy_meter)


def is_energy_meters_access_exists(db: Session, username: str, energy_meter_id: int) -> bool:
    energy_meter = db.query(models.EnergyMetersAccess).filter(
        models.EnergyMetersAccess.user == username,
        models.EnergyMetersAccess.energy_meter == energy_meter_id
    ).scalar()
    return True if energy_meter is not None else False


def get_energy_meters_access_by_username(db: Session, username: str) -> list[models.EnergyMetersAccess]:
    return db.query(models.EnergyMetersAccess.user == username).all()


def get_energy_meters_access_by_energy_meter_id(db: Session, energy_meter_id: int) -> list[models.EnergyMetersAccess]:
    return db.query(models.EnergyMetersAccess.energy_meter == energy_meter_id).all()
