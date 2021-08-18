from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.user import User

from schemas.user import UserRegister


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first().to_pb_user()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first().to_pb_user()


def get_users(db: Session, limit: int = 100):
    return db.query(User).limit(limit).all()


def create_user(db: Session, user: UserRegister):
    db_user = User(user_name=user.user_name, first_name=user.first_name, last_name=user.last_name,
                   password=user.password, email=user.email, institution=user.institution,
                   country=user.country)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as e:
        db.rollback()
        return None

    return db_user.to_pb_user()
