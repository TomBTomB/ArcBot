## Build and Run

```bash
poetry build-project
docker build --tag arcbot .
docker compose down
docker image prune -f
docker compose up -d
```

## Kubernetes
    
```bash
cd projects/bot

minikube start

kubectl create secret generic arcbot-secret --from-env-file=.env

kubectl create -f kubernetes.yaml

minikube dashboard
```