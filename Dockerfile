FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /annotations
WORKDIR /annotations

COPY Pipfile Pipfile.lock /annotations/

RUN pip install pipenv
RUN pipenv install --deploy --system

COPY . /annotations/
