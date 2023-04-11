FROM ubuntu:16.04

RUN apt-get update && apt-get install -y openssh-server apache2 supervisor
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 22 80
CMD ["/usr/bin/supervisord"]
RUN --rm -it stripe/stripe-cli:latest
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN gunicorn datamagnum.wsgi 
RUN celery -A datamagnum worker --pool=solo -l INFO 
RUN celery -A datamagnum beat -l INFO 