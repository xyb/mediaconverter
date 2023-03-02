# mediaconverter

**mediaconverter** is a Restful API service for convert media files.

Support convert audio files to mp3 format only right now.

## Usage

First, you should specify a `DATA_DIR` as your base directory and run the
service:
```sh
$ export DATA_DIR=$HOME/media
$ python3 manage.py migrate
$ python3 manage.py runserver &
$ python3 manage.py converter &
```

Then submit your conversion request:
```sh
$ curl -X POST -d "from_path=idea.wav&to_path=idea.mp3" localhost:8000/task/ | jq .
{
  "id": 1,
  "from_path": "idea.wav",
  "to_path": "idea.mp3",
  "status": "Inited",
  "created_at": "2023-03-02T08:35:31.584708Z",
  "started_at": null,
  "finished_at": null,
  "failed": false,
  "message": ""
}
```

After a few seconds, you can check if the conversion has finished:
```sh
$ curl -s localhost:8000/task/1/ | jq .
{
  "id": 1,
  "from_path": "idea.wav",
  "to_path": "idea.mp3",
  "status": "Inited",
  "created_at": "2023-03-02T08:35:31.584708Z",
  "started_at": null,
  "finished_at": null,
  "failed": false,
  "message": ""
}
```

or failed:
```sh
$ curl -s localhost:8000/task/2/ | jq .
{
  "id": 2,
  "from_path": "my.wav",
  "to_path": "../my.mp3",
  "status": "Finished",
  "created_at": "2023-03-02T08:45:26.454918Z",
  "started_at": "2023-03-02T08:45:26.466930Z",
  "finished_at": "2023-03-02T08:45:26.468876Z",
  "failed": true,
  "message": "PathNotSafe: '../my.mp3'"
}
```

You can also filter tasks by `to_path`:
```sh
$ curl -s 'localhost:8000/task/?to_path=idea.mp3' | jq .
[
  {
    "id": 1,
    "from_path": "idea.wav",
    "to_path": "idea.mp3",
    "status": "Inited",
    "created_at": "2023-03-02T08:35:31.584708Z",
    "started_at": null,
    "finished_at": null,
    "failed": false,
    "message": ""
  }
]
```

It uses [Django REST framework](https://www.django-rest-framework.org/),
so you can also access this interface through your browser.


# Docker

There are pre-built [docker images](https://hub.docker.com/r/xieyanbo/mediaconverter).

You can run it with docker:
```sh
$ docker run -d -p 8000:8000 -v $HOME/media:/data \
  -e DATA_DIR=/data -e DJANGO_DEBUG=0 --name mediaconverter \
  xieyanbo/mediaconverter
```

This is a template for `docker-compose.yml`, if you want to use
docker-compose:
```yaml
version: "3"

services:
  mediaconverter:
    image: xieyanbo/mediaconverter:latest
    container_name: mediaconverter
    restart: always
    environment:
      - DJANGO_SECRET_KEY=some-secret-string
      - DJANGO_DEBUG=0
      - DATA_DIR=/data
    ports:
      - 8000:8000
    volumes:
      - /my/media:/data:rw
```
