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


class StatisticSchema(BaseModel):
    labels: list[str]
    from_db: list[list]
    from_buffer: list[list]

    class Config:
        title = "Example for 'power' metric"
        schema_extra = {
            "example": {
                "labels": ["datetime", "counter", "phase_a", "phase_b", "phase_c", "total"],
                "from_db": [["2022-05-18T09:39:50", 4101469, 1056, 1911, 3871, 6838]],
                "from_buffer": [["2023-01-05T00:21:00.620792", 4101469, 123, 456, 789, 123456789]],
            }
        }
