import grpc

import database_pb2_grpc
import database_pb2

channel = grpc.insecure_channel('localhost:50051')
stub = database_pb2_grpc.DatabaseStub(channel)

new_user = database_pb2.UserRegister(user_name="yuegong12", first_name="yue", last_name="gong", password="123", email="xx",
                                     institution="xx", country="xx")

query_user = database_pb2.User(id=2, user_name="yuegong12", first_name="yue", last_name="gong", email="xx",
                                     institution="xx", country="xx")
print("begin calling create_user")
# userResponse = stub.CreateUser(new_user)
userResponse = stub.GetUser(query_user)
print(userResponse)
print("finished")
