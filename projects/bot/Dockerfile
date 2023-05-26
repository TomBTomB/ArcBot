FROM python:3.10.5-slim-buster

WORKDIR /app

COPY . .
RUN pip install ./dist/*.whl

# install opus lib
RUN apt-get update && apt-get install -y libopus0
# install ffmpeg and add to path
RUN apt-get install -y ffmpeg
ENV PATH="/usr/bin/ffmpeg:${PATH}"

CMD ["python", "main.py"]
