FROM python:3.9.18
WORKDIR /kgit

RUN apt-get update && apt-get install -y nano && apt-get clean

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

USER root
RUN mkdir /.cache
RUN chmod 777 /.cache

CMD /bin/bash run.sh