ARG MI_VARIABLE="flask-app"

FROM public.ecr.aws/docker/library/python:3.10.17-alpine3.21

WORKDIR /usr/src/app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=application.py

ENV RDS_USERNAME=postgres
ENV RDS_PASSWORD=miso202512
ENV RDS_HOSTNAME='miso-database-rds.c4decwyyqfx4.us-east-1.rds.amazonaws.com'
ENV RDS_PORT=5432
ENV RDS_DB_NAME=blacklists_db
ENV SECRET_TOKEN=qwerty

ENV NEW_RELIC_APP_NAME="miso-app"
ENV NEW_RELIC_LICENSE_KEY="<REMOVED_TOKEN>"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_LOG_LEVEL=info
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true

CMD ["flask", "run"]

ENTRYPOINT [ "newrelic-admin", "run-program" ]
