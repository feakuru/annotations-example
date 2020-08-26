# annotations-example
This project is a demonstration of my skills with Django and DRF. This README describes the design of this project.

## Pipenv

This project's virtual environment is set up using [pipenv](https://github.com/pypa/pipenv), a really cool tool to manage Python dependencies and version them.

## Project settings

The project is set up following a [manual](https://medium.com/@feakuru/dockerizing-django-7246ccda9fb3) on Dockerizing Django projects written by me. The docker-compose setup features three containers: the app itself, the Postgres DB which is not exposed to the outer world and a nginx proxy. Static files and Postgres data are kept on volumes which are preserved between restarts.

When launched with `docker-compose up`, the project will be available on port 1337.
