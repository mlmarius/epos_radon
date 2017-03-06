FROM ubuntu:16.04
MAINTAINER mlmarius@yahoo.com
RUN apt update -y
RUN apt install -y python-mysql.connector
RUN apt install -y git
RUN apt install -y python-pip
RUN pip install --upgrade pip
RUN mkdir -p /opt/epos/radon
RUN git clone https://github.com/mlmarius/epos_radon.git /opt/epos/radon
WORKDIR /opt/epos/radon
RUN pip install -r requirements.txt
ENTRYPOINT ["/usr/bin/python", "/opt/epos/radon/radon.py"]
