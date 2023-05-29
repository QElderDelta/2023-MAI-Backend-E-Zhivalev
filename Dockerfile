FROM ubuntu

RUN apt-get clean && apt-get update -y
RUN apt-get -y install python3 pip libpq-dev

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY autoru_ripoff autoru_ripoff

ENTRYPOINT python3 autoru_ripoff/manage.py migrate && python3 autoru_ripoff/manage.py runserver 0.0.0.0:${SERVICE_PORT}