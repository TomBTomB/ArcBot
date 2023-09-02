# ArcBot

Discord bot used as a case study for our thesis based on architecture complexity

## Requirements

- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/get-docker/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) (optional)

## Build and Deploy

On the project root run:

```shell
poetry build-project --directory projects/bot
cd projects/bot
docker build . -t arcbot
cd ../..
docker compose -f projects/bot/docker-compose.yml --project-directory . up --force-recreate --build  
```

## Run tests

```shell
poetry poly sync
pip uninstall arcbot
poetry build-project
pip install dist/arcbot-0.1.0-py3-none-any.whl
poetry run python -m pytest
```
