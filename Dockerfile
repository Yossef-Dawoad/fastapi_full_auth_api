FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.prod.txt requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --target=/app --no-cache-dir

# copy the application to the /app directory
COPY ./auth /app

EXPOSE 8080
