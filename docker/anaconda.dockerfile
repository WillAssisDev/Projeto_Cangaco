FROM continuumio/anaconda3:2020.11
MAINTAINER Wilson Assis

COPY requirements.txt .
COPY requirements-downloads.py .

RUN apt update
RUN apt-get update
RUN apt install wget
RUN apt install curl -y
RUN apt-get install apt-transport-https
RUN apt install libmariadb3 libmariadb-dev -y
RUN apt-get install gcc libc-dev g++ libffi-dev libxml2 libffi-dev unixodbc-dev -y
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN echo "b7519209546e1656e5514c04b4dcffdd9b4123201bcd1875a361ad79eb943bbe mariadb_repo_setup" | sha256sum -c -
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.5"

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN python requirements-downloads.py

EXPOSE 8888
