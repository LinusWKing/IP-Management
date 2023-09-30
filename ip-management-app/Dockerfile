FROM python:slim

ENV FLASK_APP = app.py

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD [ "flask", "run" ]