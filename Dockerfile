FROM python:3

WORKDIR /code

RUN pip install poetry

COPY . /code

RUN poetry export -f requirements.txt --without-hashes > requirements.txt
RUN pip install -r requirements.txt

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]