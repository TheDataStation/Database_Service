from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.api import API
from schemas.api import API

def create_api(db: Session, api: API):
    db_api = API(api_name=api.api_name,)
    try:
        db.add(db_api)
        db.commit()
        db.refresh(db_api)
    except SQLAlchemyError as e:
        db.rollback()
        return None
    return db_api.to_pb_api()
