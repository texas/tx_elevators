FROM texastribune/base
MAINTAINER cchang@texastribune.org

ADD . /app
WORKDIR /app
ENV PYTHONPATH /app
RUN pip install -r requirements.txt
