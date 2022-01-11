from sqlalchemy import Column, Integer, ForeignKey

import database_pb2
from database import Base


class Provenance(Base):
    __tablename__ = "provenance"

    child_id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, primary_key=True)

    def to_pb_provenance(self):
        return database_pb2.Provenance(child_id=self.child_id,
                                       parent_id=self.parent_id,)
