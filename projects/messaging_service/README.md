## Build and Run

```bash
poetry build-project
docker build --tag messaging_service .
docker compose down
docker image prune -f
docker compose up -d
```
