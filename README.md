# Serverless PoC with Minikube and Docker

This project sets up a serverless compute platform using Minikube, Kubernetes CLI, and Docker. It demonstrates deploying
and invoking serverless functions.

## Prerequisites

- Python 3.11
- Docker
- Minikube
- Kubernetes CLI (kubectl)

## Setup

1. **Navigate to the base directory:**

```sh
unzip Serverless-V4.zip -d ./Serverless
cd Serverless
```

2. **Set Docker platform for ARM64 (if needed):**

```sh
export DOCKER_DEFAULT_PLATFORM=linux/arm64
```

3. **Start Minikube:**

```sh
minikube start
minikube status
```

4. **Enable Ingress Addon:**

```sh
minikube addons enable ingress
```

5. **Set Namespace Context:**

```sh
kubectl config set-context --current --namespace=serverless-poc
```

6. **Configure Docker Environment:**

```sh
eval $(minikube docker-env)
```

## Build Docker Images

```sh
docker build -t serverless-python-function-base:latest funcation-base-images/python
docker build -t serverless-poc-api-gateway:latest serverless-poc/api-gateway
docker build -t serverless-poc-function-manager:latest serverless-poc/function-manager
```

## Deploy Kubernetes Resources

```sh
kubectl apply -f kube-config/serverless-namespace.yaml
kubectl apply -f kube-config/serverless-storage.yaml
kubectl apply -f kube-config/serverless-api-gateway.yaml
kubectl apply -f kube-config/serverless-function-manager.yaml
kubectl apply -f kube-config/serverless-ingress.yaml
```

## Prepare Storage

```sh
mkdir -p minikube-data
minikube ssh "sudo mkdir -p /mnt/logs"
minikube ssh "sudo mkdir -p /mnt/functions"
```

## Verify Deployment

```sh
kubectl get pods
```

## Mount Local Data to Minikube

```sh
nohup minikube mount minikube-data:/mnt > minikube-mount.log 2>&1 &
```

## Restart Deployments

```sh
kubectl rollout restart deployment api-gateway function-manager
kubectl get pods
```

## Port Forwarding

```sh
nohup kubectl port-forward svc/api-gateway 8080:80 > port-forward.log 2>&1 &
```

## Test Function Registration

```sh
curl -s -w '\nTotal Time: %{time_total}s\n' -X POST -F "function_name=text_pipeline" -F "file=@test-functions/text_pipeline.zip" http://127.0.0.1:8080/register

curl -s -w '\nTotal Time: %{time_total}s\n' -X POST -F "function_name=currency_converter" -F "file=@test-functions/currency_converter.zip" http://127.0.0.1:8080/register
```

## Test Function Execution

```sh
curl -s -w '\nTotal Time: %{time_total}s\n' -X POST http://127.0.0.1:8080/execute \
-H "Content-Type: application/json" \
-d '{
  "function_name": "text_pipeline",
  "payload": {"text": "Vinod is learning serverless architecture with Python. Python is amazing!"}
}'

curl -s -w '\nTotal Time: %{time_total}s\n' -X POST http://127.0.0.1:8080/execute \
-H "Content-Type: application/json" \
-d '{
  "function_name": "currency_converter",
  "payload": {"base_currency": "USD", "target_currency": "SGD", "amount": 100}
}'
```

## Cleanup

```sh
kubectl delete -f kube-config/serverless-ingress.yaml
kubectl delete -f kube-config/serverless-function-manager.yaml
kubectl delete -f kube-config/serverless-api-gateway.yaml
kubectl delete -f kube-config/serverless-storage.yaml
kubectl delete -f kube-config/serverless-namespace.yaml

minikube stop
minikube delete
```

## Debugging and Reset Commands

```sh
# Check running commands in back-end
ps aux | grep "command-name"
# Docker desktop credentials key update (to fix - error getting credentials - err: exec: "docker-credential-desktop")
vim ~/.docker/config.json

# Docker images cleanup and restart
docker system prune -f
pkill Docker
open /Applications/Docker.app

# minikube containers cleanup
docker ps -a | grep minikube
docker rm -f -v minikube
minikube delete --all --purge
```
