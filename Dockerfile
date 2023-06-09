FROM python:3.11.1-slim-buster as final

WORKDIR /app

COPY requirements.txt requirements.txt

COPY . .

RUN pip3 install --prefer-binary --no-cache --no-cache-dir -r requirements.txt \
    && addgroup --gid 1001 dashboard \ 
    && adduser --uid 1001 --disabled-password --no-create-home --ingroup dashboard dashboard \
    && chown -R dashboard /app

EXPOSE 8050

CMD ["python", "main.py"]

