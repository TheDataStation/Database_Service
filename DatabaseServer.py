import database_pb2_grpc
from database import SessionLocal, engine, Base
from crud import user_repo, dataset_repo
import grpc
from concurrent import futures
import logging
import database_pb2
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

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

    def CreateDataset(self, request, context):

        # Before we create dataset, verify request.signature first (using pk_DR)

        try:
            with open("public_keys/pk_DR.pem", "rb") as key_file:
                pk_DR = serialization.load_pem_public_key(
                    key_file.read(),
                )

            expected_msg = str(request.owner_id) + ";" + str(request.name)
            msg_bytes = bytes(expected_msg.encode("utf-8"))

            pk_DR.verify(request.signature,
                         msg_bytes,
                         padding.PSS(
                             mgf=padding.MGF1(hashes.SHA256()),
                             salt_length=padding.PSS.MAX_LENGTH
                         ),
                         hashes.SHA256())
        except:
            return database_pb2.DatasetResp(status=-2,
                                            msg="Signature does not verify")

        # Actually creating the dataset

        dataset = dataset_repo.create_dataset(self.db, request)
        if dataset:
            return database_pb2.DatasetResp(status=1, msg="success", data=[dataset])
        else:
            return database_pb2.DatasetResp(status=-1, msg="fail", data=[])

    def GetDatasetByName(self, request, context):
        dataset = dataset_repo.get_dataset_by_name(self.db, request.name)
        if dataset:
            return database_pb2.DatasetResp(status=1, msg="success", data=[dataset])
        else:
            return database_pb2.DatasetResp(status=-1, msg="fail", data=[])

    def GetDatasetById(self, request, context):
        dataset = dataset_repo.get_dataset_by_id(self.db, request.id)
        if dataset:
            return database_pb2.DatasetResp(status=1, msg="success", data=[dataset])
        else:
            return database_pb2.DatasetResp(status=-1, msg="fail", data=[])

    def GetAllMetadataID(self, request, context):
        metadata_ID_array = dataset_repo.get_all_metadata_ID(self.db)
        # if metadataID:
        #     return database_pb2.MetadataResponse(status=0, message="success", metadataID=[metadataID])
        # else:
        # return database_pb2.MetadataResponse(status=1, message="fail", metadataID=[])
        return database_pb2.MetadataResponse(status=0, message="success", metadataID=metadata_ID_array)

    def GetDatasetOwner(self, request, context):
        user = dataset_repo.get_dataset_owner(self.db, request.id)
        if user:
            return database_pb2.UserResponse(status=1, msg="success", data=[user])
        else:
            return database_pb2.UserResponse(status=-1, msg="error checking dataset owner", data=[])


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
