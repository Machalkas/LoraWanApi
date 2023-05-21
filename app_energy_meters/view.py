from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app_energy_meters.utils import get_clickhouse_writer_or_raise
from utils.db_dependency import get_db
from app_energy_meters import models, schemas, crud
from app_users import utils as user_utils
from app_users.utils import check_permissions


router = APIRouter(prefix="/energy_meters")


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


@router.get("/get_energy_meters_rooms_list", response_model=list[schemas.EnergyMeterRoomSchema],
            dependencies=[Depends(check_permissions())])
async def get_energy_meters_rooms_list(db: Session = Depends(get_db)):
    return crud.get_energy_meter_room_list(db)


@router.get("/get_energy_meters", response_model=list[schemas.EnergyMeterSchema],
            dependencies=[Depends(check_permissions())])
async def get_energy_meters_list(db: Session = Depends(get_db)):
    return crud.get_energy_meter_list(db)
