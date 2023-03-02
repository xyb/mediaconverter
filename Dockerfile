FROM python:3

ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install \
    --trusted-host mirrors.aliyun.com \
    -i http://mirrors.aliyun.com/pypi/simple/ \
    poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry export -f requirements.txt -o requirements.txt \
    && pip install \
    --trusted-host mirrors.aliyun.com \
    -i http://mirrors.aliyun.com/pypi/simple/ \
    -r requirements.txt

ADD . /app

EXPOSE 8000

CMD /app/entrypoint.sh
