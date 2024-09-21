# BUILDER

FROM python:3.12-slim-bookworm as builder

RUN apt-get update \
  && apt-get -y install g++ \
  && apt-get clean

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# FINAL

FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get upgrade -y && apt-get clean

RUN mkdir -p /home/app

RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME

WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0
ENV PYTHONPATH $APP_HOME

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME

RUN python manage.py collectstatic --noinput

RUN chown -R app:app $HOME

USER app

CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT