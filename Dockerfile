FROM python:2
COPY ./requirements.txt /usr/src/app/
WORKDIR /usr/src/app/
RUN pip install -r requirements.txt
