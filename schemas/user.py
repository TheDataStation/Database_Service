from pydantic import BaseModel
from typing import List

from schemas.dataset import Dataset


class User(BaseModel):
    id: int
    user_name: str
    first_name: str
    last_name: str
    email: str
    institution: str
    country: str
    datasets: List[Dataset] = []

    class Config:
        orm_mode = True


class UserRegister(BaseModel):
    user_name: str
    first_name: str
    last_name: str
    password: str
    email: str
    institution: str
    country: str


class UserLogin(BaseModel):
    user_name: str
    password: str
