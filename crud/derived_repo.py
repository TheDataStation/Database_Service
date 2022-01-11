from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.derived import Derived

from schemas.derived import DerivedCreate


def create_derived(db: Session, derived: DerivedCreate):
    db_derived = Derived(id=derived.id,
                         caller_id=derived.caller_id,
                         api=derived.api,)

    try:
        db.add(db_derived)
        db.commit()
        db.refresh(db_derived)
    except SQLAlchemyError as e:
        db.rollback()
        return None
    return db_derived.to_pb_derived()