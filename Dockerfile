FROM python:3.8.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

RUN mkdir /code
WORKDIR /code
EXPOSE 8069

COPY . /code

RUN apk update \
    && apk add --virtual build-deps  musl-dev postgresql-dev \
    && apk add jpeg-dev zlib-dev libjpeg gcc python3-dev libffi-dev linux-headers postgresql-client \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del build-deps

RUN sed -i 's/\r$//g' /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["sh", "/code/entrypoint.sh"]