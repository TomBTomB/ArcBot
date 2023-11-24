FROM python:3.10.5-slim-buster

WORKDIR /app

COPY . .
RUN pip install ./dist/*.whl

CMD ["python", "main.py"]
