from sqlalchemy.orm import Session

from models.dataset import Dataset
from models.user import User

from schemas.dataset import DatasetCreate

from sqlalchemy.exc import SQLAlchemyError


def get_datasets(db: Session, limit: int = 100):
    return db.query(Dataset).limit(limit).all()


def get_dataset_by_id(db: Session, dataset_id: int):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if dataset:
        return dataset.to_pb_dataset()
    else:
        return None


def get_dataset_by_name(db: Session, name: str):
    dataset = db.query(Dataset).filter(Dataset.name == name).first()
    if dataset:
        return dataset.to_pb_dataset()
    else:
        return None


def create_dataset(db: Session, dataset: DatasetCreate):
    db_dataset = Dataset(id=dataset.id,
                         owner_id=dataset.owner_id,
                         name=dataset.name,
                         url=dataset.url,
                         description=dataset.description,
                         upload=dataset.upload,
                         derived=dataset.derived,
                         derived_type=dataset.derived_type,
                         origin_data_id=dataset.origin_data_id)

    try:
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
    except SQLAlchemyError as e:
        db.rollback()
        return None
    return db_dataset.to_pb_dataset()


# The following function returns all dataset ID whose derived_type == metadata
def get_all_metadata_ID(db: Session):
    dataset = db.query(Dataset).filter(Dataset.derived_type == "metadata")
    metadata_ID_array = []
    for data in dataset:
        metadata_ID_array.append(data.id)
    return metadata_ID_array


# The following function returns the owner, given a dataset ID.
def get_dataset_owner(db: Session, dataset_id: int):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if dataset:
        user = db.query(User).filter(User.id == dataset.owner_id).first()
        if user:
            return user.to_pb_user()
    return None



