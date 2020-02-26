FROM python:3.7

COPY requirements.txt /
RUN pip install -r requirements.txt

#RUN mkdir -p /root/db , "sqlite3"

COPY ./userservice /app

ENTRYPOINT ["python", "app"]