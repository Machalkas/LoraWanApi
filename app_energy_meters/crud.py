from sqlalchemy.orm import Session
from . import models, schemas


def create_energy_meter_rooms(db: Session, energy_meter_rooms: list[schemas.EnergyMeterRoomCreateSchema]):
    db_energy_meter_rooms = [models.EnergyMeterRoom(device_serial=emr.device_serial, room=emr.room) for emr in energy_meter_rooms]
    db.bulk_save_objects(db_energy_meter_rooms)
    db.commit()
    # db.refresh(db_energy_meter_rooms)
    return get_energy_meter_room_list(db)


def get_energy_meter_room(db: Session, id: int):
    return db.query(models.EnergyMeterRoom).filter(models.EnergyMeterRoom.id == id).first()


def is_energy_meter_room_exists(db: Session, id: int) -> bool:
    energy_meter_room = db.query(models.EnergyMeterRoom).filter(models.EnergyMeterRoom.id == id).scalar()
    return True if energy_meter_room is not None else False


def get_energy_meter_room_by_device_serial(db: Session, device_serial: str) -> models.EnergyMeterRoom:
    return db.query(models.EnergyMeterRoom).filter(models.EnergyMeterRoom.device_serial == device_serial).first()


def get_energy_meter_room_list(db: Session):
    return db.query(models.EnergyMeterRoom).all()


def get_energy_meter_list(db: Session) -> list[models.EnergyMeter]:
    return db.query(models.EnergyMeter).order_by(models.EnergyMeter.id).all()


def update_energy_meter_list(db: Session, topical_devices_list: list[schemas.EnergyMeterCreateSchema]) -> list[models.EnergyMeter]:
    topical_devices_eui = {device.device_eui for device in topical_devices_list}
    current_devices = get_energy_meter_list(db)
    already_exist_eui = set()
    for device in current_devices:
        if device.device_eui not in topical_devices_eui:
            device.is_active = False
        else:
            already_exist_eui.add(device.device_eui)
            device.is_active = True
    new_devices_eui = topical_devices_eui - already_exist_eui
    new_devices = [
        models.EnergyMeter(device_eui=device.device_eui, is_active=True, device=device.device)
        for device in topical_devices_list if device.device_eui in new_devices_eui
    ]
    db.bulk_save_objects(new_devices)
    db.commit()
    return get_energy_meter_list(db)


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
