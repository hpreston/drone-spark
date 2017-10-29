# Docker image for a Drone notification plugin for Cisco Spark

FROM python:2.7-alpine3.6
MAINTAINER Hank Preston <hank.preston@gmail.com>

RUN mkdir -p /bin/drone-spark
WORKDIR /bin/drone-spark

COPY requirements.txt /bin/drone-spark/
RUN pip install -r requirements.txt

COPY send_message.py /bin/drone-spark/

ENTRYPOINT ["python", "/bin/drone-spark/send_message.py"]
