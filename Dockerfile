FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code 


# install system dependencies
RUN apt-get update \
  && apt-get -y install gcc libpq-dev \
  && apt-get clean

# install python dependencies
RUN python -m pip install --upgrade pip
COPY requirements.prod.txt code/requirements.txt
RUN pip install -r code/requirements.txt --no-cache-dir

# copy the application to the /code directory
COPY . /code

EXPOSE 8000

# run the uvicorn server
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
