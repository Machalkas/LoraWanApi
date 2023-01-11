from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from . import models, schemas, crud
from database_clients.postgres_client import SessionLocal, engine
from utils.globals import globals

router = APIRouter()
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_clickhouse_writer_or_raise(metric):
    ch_writer = globals.clickhouse_writers.get(metric)
    if ch_writer is None:
        raise HTTPException(404, f"Metric {metric} not found")
    return ch_writer


@router.get("/energy_meter/get_statistic/{counter_id}", response_model=schemas.StatisticSchema)
async def get_statistic(counter_id: int, metric: str, from_dt: datetime = None, to_dt: datetime = None,
                        columns: str = None, limit: int = None):
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


@router.get("/energy_meter/get_last_statistic/{counter_id}")
async def get_last_statistic(counter_id: int, metric: str, rows_number: int = 1):
    ch_writer = get_clickhouse_writer_or_raise(metric)


@router.post("/energy_meter/add_energy_meter_room", response_model=schemas.EnergyMeterRoomSchema)
async def create_energy_meter_room(energy_meter_room: schemas.EnergyMeterRoomCreateSchema, db: Session = Depends(get_db)):
    db_energy_meter_room = crud.get_energy_meter_room_by_device_serial(db, device_serial=energy_meter_room.device_serial)
    if db_energy_meter_room:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="EnergyMeter with this device_serial already exist")
    return crud.create_energy_meter_room(db, energy_meter_room)


@router.get("/energy_meter/get_energy_meters_rooms_list", response_model=list[schemas.EnergyMeterRoomSchema])
async def get_energy_meters_rooms_list(db: Session = Depends(get_db)):
    return crud.get_energy_meter_room_list(db)


@router.get("/energy_meter/get_energy_meters", response_model=list[schemas.EnergyMeterSchema])
async def get_energy_meters_list(db: Session = Depends(get_db)):
    return crud.get_energy_meter_list(db)
