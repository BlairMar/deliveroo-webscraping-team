FROM python:3.8-slim-buster
COPY . .
RUN pip install -r requirements2.txt