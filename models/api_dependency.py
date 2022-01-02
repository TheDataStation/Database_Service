from sqlalchemy import Column, String

import database_pb2
from database import Base


class APIDependency(Base):
    __tablename__ = "APIDependency"

    from_api = Column(String)
    to_api = Column(String)

    def to_pb_api_depend(self):
        return database_pb2.API(from_api=self.from_api,
                                to_api=self.to_api,
                                )
