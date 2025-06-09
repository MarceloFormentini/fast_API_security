from pydantic import BaseModel
from typing import Optional

# # region User Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
# # endregion

# # region Team Schemas
class TeamCreate(BaseModel):
    code: str
    name: str

class TeamRead(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        orm_mode = True
# # endregion