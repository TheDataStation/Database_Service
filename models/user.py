from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

import database_pb2

from models.dataset import Dataset


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    email = Column(String)
    institution = Column(String)
    country = Column(String)

    datasets = relationship("Dataset", back_populates="owner")

    def to_pb_user(self):
        return database_pb2.User(id=self.id, user_name=self.user_name, first_name=self.first_name,
                                 last_name=self.last_name, email=self.email, institution=self.institution,
                                 country=self.country)
