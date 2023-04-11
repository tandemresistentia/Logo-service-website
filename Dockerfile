FROM ubuntu:latest

RUN apt-get update && apt-get install -y openssh-server apache2 supervisor
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 22 80
CMD ["/usr/bin/supervisord"]
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/* 

WORKDIR /app
#COPY . /app
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip install --no-cache --upgrade pip setuptools

RUN pip --version  # just for test
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

