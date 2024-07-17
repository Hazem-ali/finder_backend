FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED 1

CMD python manage.py runserver 0.0.0.0:8000 




    