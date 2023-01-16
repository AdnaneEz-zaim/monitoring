FROM python:3:11.1-slim
WORKDIR /app

COPY requirements.txt requirements.txt

COPY . .

RUN pip3 install --prefer-binary --no-cache --no-cache-dir -r requirements.txt \
    && addgroup --gid 1001 dashboard \ 
    && adduser --uid 1001 --disabled-password --no-create-home --ingroup dashboard dashboard \
    && chown -R dashboard /app

USER dashboard

EXPOSE 8050

ENTRYPOINT python3 main.py
