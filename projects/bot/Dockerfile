#FROM python:3.10.5-slim-buster
#
#WORKDIR /app
#
#COPY ../.. .
#
#WORKDIR /app/projects/bot
#RUN pip install poetry
#RUN poetry config virtualenvs.create false
#RUN  poetry install --no-interaction --no-ansi
#
#ENV PYTHONPATH "${PYTHONPATH}:/app"
#
#CMD ["python", "main.py"]

FROM python:3.10.5-slim-buster

WORKDIR /app

COPY . .
RUN pip install ./dist/*.whl

CMD ["python", "main.py"]
