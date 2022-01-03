from sqlalchemy import Column, String, ForeignKey

import database_pb2
from database import Base


class APIDependency(Base):
    __tablename__ = "APIDependency"

    from_api = Column(String, ForeignKey("APIs.api_name"), primary_key=True,)
    to_api = Column(String, primary_key=True)


    def to_pb_api_depend(self):
        return database_pb2.APIDependency(from_api=self.from_api,
                                          to_api=self.to_api,)
