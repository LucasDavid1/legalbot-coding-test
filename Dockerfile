FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /django_project

WORKDIR /django_project

COPY . /django_project/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]
