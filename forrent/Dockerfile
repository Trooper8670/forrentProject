###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.8-slim as builder

# set work directory
WORKDIR /usr/src/forrent

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client gcc libpq-dev zlib1g-dev \
    libjpeg62-turbo-dev \
    netcat \
    netcat-openbsd

# lint
RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/forrent/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.8.8-slim

RUN mkdir -p /forrent
RUN mkdir /forrent/mediafiles
WORKDIR /forrent

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev
RUN apt-get update && apt-get install -y netcat netcat-openbsd
COPY --from=builder /usr/src/forrent/wheels /wheels
COPY --from=builder /usr/src/forrent/requirements.txt .
RUN pip install --no-cache /wheels/*

RUN useradd -ms /bin/bash forrent

# copy entrypoint.sh
ADD entrypoint.sh /forrent

# copy project
COPY . /forrent

# chown all the files to the app user
RUN chown -R forrent:forrent /forrent

# change to the app user
USER forrent

# run entrypoint.sh
ENTRYPOINT ["/forrent/entrypoint.sh"]