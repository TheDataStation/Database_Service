from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

import database_pb2
from database import Base


from models.dataset import Dataset


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    password = Column(String)

    datasets = relationship("Dataset", back_populates="owner")

    def to_pb_user(self):
        return database_pb2.User(id=self.id,
                                 user_name=self.user_name,
                                 password=self.password,)

