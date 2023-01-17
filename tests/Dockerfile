FROM python:3.11.1-slim-buster as final
WORKDIR /app
COPY requirements_test.txt requirements.txt
RUN pip install -r requirements.txt
