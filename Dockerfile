FROM debian:bullseye

RUN apt-get update && apt-get install -y python3-pip
ADD . /database_service/

RUN pip3 install -r /database_service/requirements.txt

WORKDIR /database_service
CMD ["python3", "DatabaseServer.py"]
