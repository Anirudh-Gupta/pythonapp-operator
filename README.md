## Project structure -
```
├── app
│   ├── index.js
│   ├── Dockerfile(For building python CRUD app)
│   ├── requirements.txt
├── crds
│   ├── crd.yaml
├── operator(k8s-operator)
│   ├── k8s
│   │   ├── db-pvc.yaml
│   │   ├── postgres-deployment.yaml
│   │   ├── postgres-service.yaml
│   │   ├── web-deployment.yaml
│   │   ├── web-service.yaml
│   ├── Dockerfile(FOr building the operator image)
│   ├── requirements.txt
│   ├── with_update.py(Core operator logic)
├── python-operator
│   ├── charts
│   ├── templates(operator deployment, namespace, pv, rbac, sa, secret, pythonapp)
│   ├── Chart.yaml
│   ├── values.yaml
└── .gitignore
├── README.md
```
-------------------------------------------------------------------------------

Basic CRUD application in app/ folder:

Users entity: username, email

Endpoints:
- POST /users
- GET /users
- PUT /users
- DELETE /users

Build an image of this app using -
```
  # cd app && docker build -t <repo>:tag .
  cd app && docker build -t anirudhg47/users-app:latest .

  # docker push <repo>:<tag>
  docker push anirudhg47/users-app:latest
```
-------------------------------------------------------------------------------

## Build operator -

```
  # cd operator && docker build -t <repo>:tag .
  cd operator && docker build -t anirudhg47/pythonapp-operator:v1 .

  # docker push <repo>:<tag>
  docker push anirudhg47/pythonapp-operator:v1
```

-------------------------------------------------------------------------------
## Apply CRD first before installing helm chart using the below command

```
kubectl apply -f crds/crd.yaml

```


-------------------------------------------------------------------------------

## Install Helm Chart

```
Install helm chart using below command
helm install [NAME] [CHART]
Example: helm install python-operator python-operator
```

-------------------------------------------------------------------------------

## How to use the application deployed on K8s (Tested on docker-desktop v1.21.4) -

```
# Port Forward the web service port on the host port.
# kubectl get svc -n <namespace>
# kubectl port-forward --namespace=<namespace> service/<service-name> <host-port>:<web-service-port>
kubectl port-forward --namespace=pythonapp service/users-web-service 8080:80

# Access the application on your host using localhost:8080/users
```
-------------------------------------------------------------------------------

## Dependencies for python app -
```
flask
psycopg2-binary
Flask-SQLAlchemy
```

Dependencies for operator -
```
kopf==1.35.0
kubernetes==21.7.0
```
-------------------------------------------------------------------------------

## Pending Improvements and Known Issues

1. Use Statefulset for database(datastore). It currently uses deployment object.
2. Currently exposes only db volume, password (db username is hardcoded as of now) and name of the app. Expose more parameters depending on need.
3. crd has to be applied to the K8s cluster as a separate step. Can be automated by making it part of the helm chart.
