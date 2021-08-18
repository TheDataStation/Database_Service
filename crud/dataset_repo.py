from sqlalchemy.orm import Session

from models.dataset import Dataset

from schemas.dataset import DatasetCreate

from sqlalchemy.exc import SQLAlchemyError


def get_datasets(db: Session, limit: int = 100):
    return db.query(Dataset).limit(limit).all()


def create_dataset(db: Session, dataset: DatasetCreate):
    db_dataset = Dataset(**dataset.dict())
    try:
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
    except SQLAlchemyError as e:
        return None
    return db_dataset

