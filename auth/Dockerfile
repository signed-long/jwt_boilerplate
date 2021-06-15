# pull base image
FROM python:3.9.5-slim-buster

WORKDIR /usr/src/app

# don't create pycache
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip && pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --deploy --ignore-pipfile

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
