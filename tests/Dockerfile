FROM python:3.11.1-slim-buster as final
WORKDIR /app
COPY requirements_test.txt requirements.txt
COPY . .
RUN pip3 install --prefer-binary --no-cache --no-cache-dir -r requirements.txt

ENTRYPOINT /app/tests
