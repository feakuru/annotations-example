# annotations-example
This project is a demonstration of my skills with Django and DRF. This README describes the design of this project.

## Pipenv

This project's virtual environment is set up using [pipenv](https://github.com/pypa/pipenv), a really cool tool to manage Python dependencies and version them.

## Project settings

The project is set up following a [manual](https://medium.com/@feakuru/dockerizing-django-7246ccda9fb3) on Dockerizing Django projects written by me. The docker-compose setup features three containers: the app itself, the Postgres DB which is not exposed to the outer world and a nginx proxy. Static files and Postgres data are kept on volumes which are preserved between restarts.

When launched with `docker-compose up`, the project will set itself up and be available on port 1337.

I have included a prefill script that runs as part of `docker-compose up` and generates two example images hust to demonstrate how I would handle prefilling some test data into the database if needed.


## Implementation

The code is briefly documented via docstrings. This section describes only the endpoint structure of the implementation. All of the described endpoints make use of the `format` query parameter which distinguishes between two formats of annotation representation:

- internal, like this:
```json
  {
    "labels": [
      {
        "meta": {
          "confirmed": false,
          "confidence_percent": 0.0
        },
        "id": "3063e37d-e4e4-49e8-9621-bc3a37bb70fc",
        "class_id": "tooth",
        "surface": [
          "l",
          "o",
          "l"
        ],
        "shape": null
      }
    ]
  }
```

- external (will only show labels with `meta.confirmed == true`), like this:
```json
  {
    "labels": [
      {
        "id": "ed2993ab-bc3b-44de-9d94-99efa169b318",
        "class_id": "tooth",
        "surface": "lol"
      }
    ]
  }
```

The URLs of the images, as well as the endpoints itself, are deliberately NOT auth-protected and can be accessed from the outside world, as well as used in browser.

### `/images/` endpoint

This endpoint can be queried:
- via GET to retrieve all images in this format:
```json
{
    "id": 9,
    "image": "http://localhost/media/bac18e3e-2fe5-4c1f-8c94-c2e7fc4baf26.jpeg",
    "annotation": {
      ...
    }
  }
```
- via POST to create an image with or without an annotation with the body in this format:
```json
  {
    "image": "IMAGE_AS_BASE64",
    "annotation": {
      ...
    }
  }
```

### `/images/{id}/` endpoint

Fetches one image. Just like in the list, but a single object.

### `/images/{id}/annotation/` endpoint

This endpoint allows to fetch the image's annotation via GET or update it via POST. The format is as described above.