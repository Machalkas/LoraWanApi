from pydantic import BaseModel


class MonitorRoomSchema(BaseModel):
    id: int
    device_serial: str
    room: str

    class Config:
        orm_mode = True


class MonitorRoomCreateSchema(BaseModel):
    device_serial: str
    room: str

    class Config:
        orm_mode = True


class MonitorSchema(BaseModel):
    id: int
    device_eui: str
    device_id: str
    is_active: bool

    class Config:
        orm_mode = True


class MonitorCreateSchema(BaseModel):
    device_eui: str
    device_id: str
    is_active: bool

    class Config:
        orm_mode = True
