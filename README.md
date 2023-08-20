# ArcBot
Discord bot used as a case study for our thesis based on architecture complexity

## Build and Deploy
On the project root run:
```shell
poetry build-project --directory projects/bot
cd projects/bot
docker build . -t arcbot
cd ../..
docker compose -f projects/bot/docker-compose.yml --project-directory . up --force-recreate --build  
```