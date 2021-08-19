import database_pb2_grpc
from database import SessionLocal, engine, Base
from crud import user_repo
import grpc
from concurrent import futures
import logging
import database_pb2

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
        user = user_repo.create_user(self.db, request)
        if user:
            return database_pb2.UserResponse(status=1, msg="success", data=[user])
        else:
            return database_pb2.UserResponse(status=-1, msg="internal database error", data=[])

    def GetUser(self, request, context):
        user = user_repo.get_user(self.db, request.id)
        if user:
            return database_pb2.UserResponse(status=1, msg="success", data=[user])
        else:
            return database_pb2.UserResponse(status=-1, msg="user does not exist", data=[])

    def GetAllUsers(self, request, context):
        users = user_repo.get_users(self.db, request.limit)
        if len(users):
            return database_pb2.UserResponse(status=1, msg="success", data=users)
        else:
            return database_pb2.UserResponse(status=-1, msg="no existing users", data=[])

    def GetUserByEmail(self, request, context):
        user = user_repo.get_user_by_email(self.db, request.email)
        if user:
            return database_pb2.UserResponse(status=1, msg="success", data=[user])
        else:
            return database_pb2.UserResponse(status=-1, msg="user does not exist", data=[])

    def GetUserByUserName(self, request, context):
        user = user_repo.get_user_by_user_name(self.db, request.user_name)
        if user:
            return database_pb2.UserResponse(status=1, msg="success", data=[user])
        else:
            return database_pb2.UserResponse(status=-1, msg="user does not exist", data=[])


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
