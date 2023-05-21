from fastapi import APIRouter

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from utils.db_dependency import get_db
from app_energy_meters import schemas, crud
from app_users import crud as user_crud
from app_users import utils as user_utils
from app_users import models as user_models


router = APIRouter(prefix="/energy_meters/manage")


@router.post("/energy_meter_access", response_model=schemas.EnergyMetersAccessSchema)
async def create_energy_meter_access(energy_meter_access: schemas.EnergyMetersAccessCreateSchema,
                                     current_user: user_models.User = Depends(user_utils.check_permissions("manager")),
                                     db: Session = Depends(get_db)):
    """
    Use this endpoint to provide access to energy counters for user
    """
    if not crud.is_energy_meters_access_exists(db, current_user.username, energy_meter_access.energy_meter_room_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if not user_crud.is_user_username_exists(db, energy_meter_access.user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not crud.is_energy_meter_room_exists(db, energy_meter_access.energy_meter_room_id):
        if not user_crud.is_user_username_exists(db, energy_meter_access.user):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="EnergyMeterRoom not found"
            )
    if crud.is_energy_meters_access_exists(db, energy_meter_access.user,
                                           energy_meter_access.energy_meter_room_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Energy_meter_access already exists"
        )
    return crud.add_energy_meters_access(db, energy_meter_access)


@router.post("/add_energy_meter_rooms", response_model=list[schemas.EnergyMeterRoomSchema],
             dependencies=[Depends(user_utils.check_permissions("manager"))])
async def create_energy_meter_room(energy_meter_rooms: list[schemas.EnergyMeterRoomCreateSchema], db: Session = Depends(get_db)):
    for emr in energy_meter_rooms:
        db_energy_meter_room = crud.get_energy_meter_room_by_device_serial(db, device_serial=emr.device_serial)
        if db_energy_meter_room:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"EnergyMeter with this device_serial {emr.device_serial} already exist")

    return crud.create_energy_meter_rooms(db, energy_meter_rooms)
