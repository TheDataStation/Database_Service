# Database_Service

Database Operation Microservice using [grpc](https://grpc.io/)

Decouple database services from individul components. Database operations are achieved through rpc calls to this repo.

## Usage
```shell
# generate proto code
python3 -m grpc_tools.protoc -I ./protos --python_out=. --grpc_python_out=. ./protos/database.proto

# run database server
python3 DatabaseServer.py
```
