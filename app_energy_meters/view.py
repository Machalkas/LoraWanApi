from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from utils.db_dependency import get_db
from app_energy_meters import models, schemas, crud
from app_users import crud as user_crud
from app_users import utils as user_utils
from app_users.utils import check_permissions
from database_clients.postgres_client import engine
from utils.globals import globals

router = APIRouter(prefix="/energy_meters")
models.Base.metadata.create_all(bind=engine)


def get_clickhouse_writer_or_raise(metric):
    ch_writer = globals.clickhouse_writers.get(metric)
    if ch_writer is None:
        raise HTTPException(404, f"Metric {metric} not found")
    return ch_writer


@router.get("/get_statistic/{counter_id}", response_model=schemas.StatisticSchema,
            dependencies=[Depends(check_permissions())])
async def get_statistic(counter_id: str, metric: str, from_dt: datetime = None, to_dt: datetime = None,
                        columns: str = None, limit: int = None, db: Session = Depends(get_db),
                        current_user: models.User = Depends(user_utils.get_current_user)):
    counter = crud.get_energy_meter_room_by_device_serial(db, counter_id)
    if counter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counter not found in EnergyMeterRoom"
        )
    if not crud.is_energy_meters_access_exists(db, current_user.username, counter.id) and current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    ch_writer = get_clickhouse_writer_or_raise(metric)
    filter_query = f"`counter` = {counter_id}"
    if from_dt:
        filter_query += f" and `datetime` > '{from_dt}'"
    if to_dt:
        filter_query += f" and `datetime` <= '{to_dt}'"
    if columns is not None:
        columns = columns.split(",")
        columns = [col.strip() for col in columns]
    response = ch_writer.get(filter_sql_query=filter_query, order_by="datetime", columns=columns,  limit=limit)
    return schemas.StatisticSchema(**response)


# @router.get("/get_last_statistic/{counter_id}")
# async def get_last_statistic(counter_id: int, metric: str, rows_number: int = 1):
#     ch_writer = get_clickhouse_writer_or_raise(metric)


@router.post("/add_energy_meter_rooms", response_model=list[schemas.EnergyMeterRoomSchema],
             dependencies=[Depends(check_permissions("manager"))])
async def create_energy_meter_room(energy_meter_rooms: list[schemas.EnergyMeterRoomCreateSchema], db: Session = Depends(get_db)):
    for emr in energy_meter_rooms:
        db_energy_meter_room = crud.get_energy_meter_room_by_device_serial(db, device_serial=emr.device_serial)
        if db_energy_meter_room:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"EnergyMeter with this device_serial {emr.device_serial} already exist")

    return crud.create_energy_meter_rooms(db, energy_meter_rooms)


@router.get("/get_energy_meters_rooms_list", response_model=list[schemas.EnergyMeterRoomSchema],
            dependencies=[Depends(check_permissions())])
async def get_energy_meters_rooms_list(db: Session = Depends(get_db)):
    return crud.get_energy_meter_room_list(db)


@router.get("/get_energy_meters", response_model=list[schemas.EnergyMeterSchema],
            dependencies=[Depends(check_permissions())])
async def get_energy_meters_list(db: Session = Depends(get_db)):
    return crud.get_energy_meter_list(db)


# @router.post("/test", response_model=list[schemas.EnergyMeterSchema])
# async def update_energy_meters(new_dev: list[schemas.EnergyMeterCreateSchema], db: Session = Depends(get_db)):
#     return crud.update_energy_meter_list(db, new_dev)


@router.post("/energy_meter_access", response_model=schemas.EnergyMetersAccessSchema,
             dependencies=[Depends(check_permissions("admin"))])
async def create_energy_meter_access(energy_meter_access: schemas.EnergyMetersAccessCreateSchema,
                                     db: Session = Depends(get_db)):
    """
    Use this endpoint to provide access to energy counters for user
    """
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
