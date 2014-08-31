FROM texastribune/base
MAINTAINER cchang@texastribune.org

ADD . /app
WORKDIR /app
ENV PYTHONPATH /app
RUN pip install --quiet -r requirements.txt
# needed to keep manage.py from trying to import too much
ENV DEBUG 0
RUN python example_project/manage.py collectstatic --noinput
