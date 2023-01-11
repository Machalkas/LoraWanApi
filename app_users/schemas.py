from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    username: str
    email: str | None

    class Config:
        orm_mode = True


class UserRegistrationSchema(UserSchema):
    password: str
