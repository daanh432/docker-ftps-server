FROM python:2-slim

COPY entrypoint.py /app/
COPY requirements.txt /app/
WORKDIR /app/
RUN pip install -r requirements.txt
RUN mkdir /ftp_root

EXPOSE 21

ENTRYPOINT python -u entrypoint.py
