## Build and Run

```bash
poetry build-project
docker build --tag arcbot_remote .
docker compose down
docker image prune -f
docker compose up -d
```
