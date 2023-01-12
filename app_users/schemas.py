from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class RoleSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    username: str
    email: str | None
    role: str

    class Config:
        orm_mode = True


class UserRegistrationSchema(BaseModel):
    username: str
    email: str | None
    password: str

    class Config:
        orm_mode = True
