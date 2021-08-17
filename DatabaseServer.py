import database_pb2_grpc
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from crud import dataset, user
import grpc
from concurrent import futures
import logging

Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DatabaseServicer(database_pb2_grpc.DatabaseServicer):
    def __init__(self):
        self.db = next(get_db())

    def CreateUser(self, request, context):
        db_user = user.create_user(self.db, request)
        # sourceFile = open('demo.txt', 'a')
        # print(db_user, file=sourceFile)
        # sourceFile.close()
        if db_user:
            return db_user


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    database_pb2_grpc.add_DatabaseServicer_to_server(
        DatabaseServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
