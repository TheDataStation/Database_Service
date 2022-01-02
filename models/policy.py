from sqlalchemy import Column, String, Integer

import database_pb2
from database import Base


class Policy(Base):
    __tablename__ = "Policy"

    user_id = Column(Integer, primary_key=True)
    api = Column(String, primary_key=True)
    data_id = Column(Integer, primary_key=True)

    def to_pb_policy(self):
        return database_pb2.Policy(user_id=self.user_id,
                                   api=self.api,
                                   data_id=self.data_id,)
