export DOCKER_DEFAULT_PLATFORM=linux/arm64

minikube start --memory 4096 --cpus 2 --driver=docker

minikube addons enable storage-provisioner
minikube addons enable ingress
minikube addons enable registry


kubectl port-forward --namespace kube-system svc/registry 5000:80 &

curl http://localhost:5000/v2/_catalog


eval $(minikube docker-env)

kubectl apply -f namespace.yaml
kubectl config set-context --current --namespace=serverless

kubectl get nodes
kubectl get pods

=========

helm repo add minio https://charts.min.io/
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
vim minio-values.yaml
helm install minio minio/minio -f minio-values.yaml


helm upgrade --install minio minio/minio  -f minio-values.yaml


nohup kubectl port-forward svc/minio 9000:9000 > minio-port-forward.log 2>&1 &

curl http://127.0.0.1:9000

kill $(ps aux | grep "kubectl port-forward svc/minio" | grep -v grep | awk '{print $2}')

============

helm repo add nuclio https://nuclio.github.io/nuclio/charts
helm repo update
vim nuclio-values.yaml
helm install nuclio nuclio/nuclio -f nuclio-values.yaml
helm upgrade --install nuclio nuclio/nuclio -f nuclio-values.yaml

nohup kubectl port-forward svc/nuclio-dashboard 8070:8070 > nuclio-dashboard-port-forward.log 2>&1 &

curl http://127.0.0.1:8070

kill $(ps aux | grep "kubectl port-forward svc/nuclio-dashboard" | grep -v grep | awk '{print $2}')

=========

helm repo add apisix https://charts.apiseven.com
helm repo update
vim apisix-values.yaml
helm install apisix apisix/apisix -f apisix-values.yaml
helm upgrade --install apisix apisix/apisix -f apisix-values.yaml

nohup kubectl port-forward svc/apisix-gateway 8080:80 > apisix-gateway-port-forward.log 2>&1 &

curl http://127.0.0.1:8080

kill $(ps aux | grep "kubectl port-forward svc/apisix-gateway" | grep -v grep | awk '{print $2}')

=========

vim apisix-routes.yaml
kubectl apply -f apisix-routes.yaml

============


helm uninstall apisix -n apisix
kubectl delete namespace apisix
helm install apisix apisix/apisix -f apisix-values.yaml
kubectl apply -f apisix-routes.yaml




curl -X POST --data-binary @my_new_function.zip http://127.0.0.1:8080/upload-function/my-new-function





kubectl port-forward svc/nuclio-my-new-function 8081:8080 &
curl -X POST http://127.0.0.1:8081







kubectl port-forward svc/minio-console 9001:9001 &


kubectl port-forward svc/apisix-admin -n serverless 9180:9180 &
curl http://127.0.0.1:9180/apisix/admin/routes -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1"


curl http://127.0.0.1:9180/apisix/admin/upstreams -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1"

helm repo add bitnami https://charts.bitnami.com/bitnami




rm apisix-routes.yaml 
vim apisix-routes.yaml 
kubectl apply -f apisix-routes.yaml 




curl -O https://dl.min.io/client/mc/release/darwin-arm64/mc
chmod +x mc
./mc --version

./mc alias set myminio http://127.0.0.1:9000 minioadmin minioadmin123



QdoJ8ouPfe9K91IVFjXd
PdNyRsfm9ogweRZND5zHYgFrrKhEA0c1MwySGVOu




curl -X POST http://127.0.0.1:8070/api/functions \
  -H "Content-Type: application/json" \
  -d '{"metadata":{"name":"test-function"},"spec":{"runtime":"python:3.9","handler":"function:handler","build":{"path":"http://minio.serverless.svc.cluster.local:9000/functions/my_new_function.zip"}},"namespace":"serverless"}'


kubectl port-forward svc/nuclio-test-function 8081:8080 &
curl http://localhost:8081







