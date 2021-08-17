import grpc

import database_pb2
import database_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = database_pb2_grpc.DatabaseStub(channel)

new_user = database_pb2.UserRegister(user_name="yuegong9", first_name="yue", last_name="gong", password="123", email="xx",
                             institution="xx", country="xx")

print("begin calling create_user")
user = stub.CreateUser(new_user)
print("finished")
