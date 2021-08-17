from sqlalchemy.orm import Session

import database_pb2
from models.user import User

from schemas.user import UserRegister

from sqlalchemy.exc import SQLAlchemyError


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, limit: int = 100):
    return db.query(User).limit(limit).all()


def create_user(db: Session, user: UserRegister):
    # print(user)
    db_user = User(user_name=user.user_name, first_name=user.first_name, last_name=user.last_name,
                   password=user.password, email=user.email, institution=user.institution,
                   country=user.country)
    # try:
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # except SQLAlchemyError as e:
    #     sourceFile = open('demo.txt', 'w')
    #     print(str(e.__dict__['orig']), file=sourceFile)
    #     sourceFile.close()
    #     return None
    sourceFile = open('demo.txt', 'a')
    print(db_user.id, file=sourceFile)
    sourceFile.close()
    return database_pb2.User(id=db_user.id, user_name=db_user.user_name, first_name=db_user.first_name,
                             last_name=db_user.last_name, email=db_user.email, institution=db_user.institution,
                             country=db_user.country)


