from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

import database_pb2
from database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    upload = Column(Boolean)
    url = Column(String)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Newly added attributes (to keep track of some derived data info)
    derived = Column(Boolean)  # True -> is a derived data product
    derived_type = Column(String)  # Currently, it will have one value "metadata", to support CatalogReader
    origin_data_id = Column(Integer)  # Id of the original dataset

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="datasets")

    def to_pb_dataset(self):
        return database_pb2.Dataset(id=self.id,
                                    name=self.name,
                                    description=self.description,
                                    upload=self.upload,
                                    url=self.url,
                                    owner_id=self.owner_id,
                                    derived=self.derived,
                                    derived_type=self.derived_type,
                                    origin_data_id=self.origin_data_id
                                    )
