FROM python:3.11.1-slim-buster as final

USER root

WORKDIR /app

COPY requirements.txt requirements.txt

ADD . /app

RUN pip3 install --prefer-binary --no-cache --no-cache-dir -r requirements.txt \

EXPOSE 8050

CMD ["python", "main.py"]

