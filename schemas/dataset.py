from pydantic import BaseModel


class Dataset(BaseModel):
    id: int
    owner_id: int  # pk user.id
    name: str
    desc: str
    upload: bool
    url: str
    created_time: str
    updated_time: str
    derived: bool
    derived_type: str
    origin_data_id: int

    class Config:
        orm_mode = True


class DatasetCreate(BaseModel):
    id: int
    owner_id: int  # pk user.id
    name: str
    description: str
    upload: bool
    url: str
    derived: bool
    derived_type: str
    origin_data_id: int
