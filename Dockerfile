FROM tiangolo/uwsgi-nginx:python3.6-alpine3.7
MAINTAINER Aleksandr Kirilyuk <alx@nsbill.ru>

RUN pip install flask && pip install flask-sqlalchemy flask_migrate flask_script
RUN apk update && apk add py-mysqldb openssh-client postgresql-client && pip install mysql-connector-python &&\
apk add py3-psycopg2 && mkdir /root/.ssh
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
      && pip install psycopg2 \
      && apk del build-deps

# By default, allow unlimited file sizes, modify it to limit the file sizes
# To have a maximum of 1 MB (Nginx's default) change the line to:
# ENV NGINX_MAX_UPLOAD 1m
ENV NGINX_MAX_UPLOAD 0

# By default, Nginx listens on port 80.
# To modify this, change LISTEN_PORT environment variable.
# (in a Dockerfile or with an option for `docker run`)
ENV LISTEN_PORT 80

# Which uWSGI .ini file should be used, to make it customizable
ENV UWSGI_INI /app/uwsgi.ini

# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /app/static

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
# ENV STATIC_INDEX 1
ENV STATIC_INDEX 0

#Add ssh key
COPY ./app/ssh /root/.ssh
# Add conf app
COPY ./app /app

WORKDIR /app

# Make /app/* available to be imported by Python globally to better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app

# Copy start.sh script that will check for a /app/prestart.sh script and run it before starting the app
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Supervisor, which in turn will start Nginx and uWSGI
CMD ["/start.sh"]
