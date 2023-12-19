## Kubernetes + Minikube + Microservice

1. Build Images for each project
2.

```bash
minikube start
kubectl apply -f arcbot-data-persistentvolumeclaim.yaml,bot-remote--env-configmap.yaml,bot-remote-deployment.yaml,db-service--env-configmap.yaml,db-service-deployment.yaml,db-service-service.yaml,messaging-service--env-configmap.yaml,messaging-service-deployment.yaml,messaging-service-service.yaml,postgres-deployment.yaml,postgres-service.yaml,postgres-service--env-configmap.yaml
minikube dashboard
kubectl delete -f arcbot-data-persistentvolumeclaim.yaml,bot-remote--env-configmap.yaml,bot-remote-deployment.yaml,db-service--env-configmap.yaml,db-service-deployment.yaml,db-service-service.yaml,messaging-service--env-configmap.yaml,messaging-service-deployment.yaml,messaging-service-service.yaml,postgres-deployment.yaml,postgres-service.yaml,postgres-service--env-configmap.yaml
```

