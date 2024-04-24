FROM python:latest

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


RUN mkdir "/fastapi_tz"

WORKDIR /fastapi_tz

COPY . /fastapi_tz

EXPOSE 8000

RUN pip install -r requirements.txt