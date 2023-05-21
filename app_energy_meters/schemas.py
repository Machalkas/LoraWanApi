from pydantic import BaseModel

from app_energy_meters.enums import LoraClientClass


class ABP(BaseModel):
    dev_address: int
    apps_key: str
    nwks_key: str


class OTAA(BaseModel):
    app_eui: str
    app_key: str


class NewDeviceDeserializer(BaseModel):
    dev_eui: str
    dev_class: LoraClientClass
    dev_name: str
    otaa: OTAA | None


class EnergyMeterRoomSchema(BaseModel):
    id: int
    device_serial: str
    room: str

    class Config:
        orm_mode = True


class EnergyMeterRoomCreateSchema(BaseModel):
    device_serial: str
    room: str

    class Config:
        orm_mode = True


class EnergyMeterSchema(BaseModel):
    id: int
    device_eui: str
    device: str
    is_active: bool

    class Config:
        orm_mode = True


class EnergyMeterCreateSchema(BaseModel):
    device_eui: str
    device: str

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


class EnergyMetersAccessSchema(BaseModel):
    id: int
    user: str
    energy_meter: int

    class Config:
        orm_mode = True


class EnergyMetersAccessCreateSchema(BaseModel):
    user: str
    energy_meter_room_id: int

    class Config:
        orm_mode = True
