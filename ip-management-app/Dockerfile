FROM python:3.11.5-slim


RUN apt-get update && apt-get install -y \
    python3-mysqldb libmariadb-dev-compat libmariadb-dev

WORKDIR /app

COPY . /app


RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD [ "python", "app.py" ]