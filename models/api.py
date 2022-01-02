from sqlalchemy import Column, String

import database_pb2
from database import Base


class API(Base):
    __tablename__ = "APIs"

    api_name = Column(String, primary_key=True, index=True)

    def to_pb_api(self):
        return database_pb2.API(api_name=self.api_name,
                                )
