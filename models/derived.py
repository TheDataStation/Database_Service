from sqlalchemy import Column, String, Integer, ForeignKey

import database_pb2
from database import Base


class Derived(Base):
    __tablename__ = "Derived"

    id = Column(Integer, primary_key=True)
    caller_id = Column(Integer, ForeignKey("users.id"))
    api = Column(String, ForeignKey("APIs.api_name"))

    def to_pb_derived(self):
        return database_pb2.Derived(id=self.id,
                                    caller_id=self.caller_id,
                                    api=self.api,)
