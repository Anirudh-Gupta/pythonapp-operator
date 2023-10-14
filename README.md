Project structure -
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
│   ├── with_upadate.py(Core operator logic)
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

Build operator -

```
  # cd operator && docker build -t <repo>:tag .
  cd operator && docker build -t anirudhg47/pythonapp-operator:v1 .

  # docker push <repo>:<tag>
  docker push anirudhg47/pythonapp-operator:v1
```

-------------------------------------------------------------------------------
Apply CRD first before installing helm chart using the below command

```
kubectl apply -f crds/crd.yaml

```


-------------------------------------------------------------------------------

Helm Chart

```
Install helm chart using below command
helm install [NAME] [CHART]
Example: helm install python-operator python-operator
```

-------------------------------------------------------------------------------

Dependencies for python app -
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