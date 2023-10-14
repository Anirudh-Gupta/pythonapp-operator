import kopf
import kubernetes.client
from kubernetes.client.rest import ApiException
import yaml
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@kopf.on.login()
def login_fn(**kwargs):
    return kopf.login_with_service_account(**kwargs)

@kopf.on.create('anirudh.io', 'v1', 'pythonapps')
def create_fn(spec, name, **kwargs):
    create_pvc_claim(spec, name)
    db_deployment_name = create_db_deployment(spec, name)
    create_db_service(spec, name)
    print("db_deployment_name ----->", db_deployment_name)
    create_web_deployment(spec, name)
    create_web_service(spec, name)


def create_db_deployment(spec, name):
  path = os.path.join(ROOT_DIR, 'k8s', 'postgres-deployment.yaml')
  db_tmpl = open(path, 'rt').read()
  db_tmpl_text = db_tmpl.format(name=name)
  db_depl = yaml.safe_load(db_tmpl_text)
  kopf.adopt(db_depl)

  # Create a postgres deployment object by requesting the Kubernetes API.
  api = kubernetes.client.AppsV1Api()
  try:
    depl = api.create_namespaced_deployment(namespace=db_depl['metadata']['namespace'], body=db_depl)
    # Update the parent's status.
    return { 'children': [ depl.metadata.name ] }
  except ApiException as e:
    print("Exception when calling AppsV1Api->db->create_namespaced_deployment: %s\n" % e)


def create_db_service(spec, name):
  path = os.path.join(ROOT_DIR, 'k8s', 'postgres-service.yaml')
  db_tmpl = open(path, 'rt').read()
  db_tmpl_text = db_tmpl.format(name=name)
  db_service = yaml.safe_load(db_tmpl_text)
  kopf.adopt(db_service)

  # Create a postgres service object by requesting the Kubernetes API.
  api = kubernetes.client.CoreV1Api()
  try:
    service = api.create_namespaced_service(namespace=db_service['metadata']['namespace'], body=db_service)
    # Update the parent's status.
    return { 'children': [ service.metadata.name ] }
  except ApiException as e:
    print("Exception when calling CoreV1Api->db->create_namespaced_service: %s\n" % e)


def create_web_service(spec, name):
  path = os.path.join(ROOT_DIR, 'k8s', 'web-service.yaml')
  web_tmpl = open(path, 'rt').read()
  web_tmpl_text = web_tmpl.format(name=name)
  web_service = yaml.safe_load(web_tmpl_text)
  kopf.adopt(web_service)

  # Create a web service object by requesting the Kubernetes API.
  api = kubernetes.client.CoreV1Api()
  try:
    service = api.create_namespaced_service(namespace=web_service['metadata']['namespace'], body=web_service)
    # Update the parent's status.
    return { 'children': [ service.metadata.name ] }
  except ApiException as e:
    print("Exception when calling CoreV1Api->web->create_namespaced_service: %s\n" % e)


def create_web_deployment(spec, name):
  path = os.path.join(ROOT_DIR, 'k8s', 'web-deployment.yaml')
  web_tmpl = open(path, 'rt').read()
  web_templ_text = web_tmpl.format(name=name)
  web_depl = yaml.safe_load(web_templ_text)
  kopf.adopt(web_depl)

  # Create a web deployment object by requesting the Kubernetes API.
  api = kubernetes.client.AppsV1Api()
  try:
    depl = api.create_namespaced_deployment(namespace=web_depl['metadata']['namespace'], body=web_depl)
    # Update the parent's status.
    return { 'children': [ depl.metadata.uid ] }
  except ApiException as e:
    print("Exception when calling AppsV1Api->web->create_namespaced_deployment: %s\n" % e)


def create_pvc_claim(spec, name):
  size = spec.get('db_size')
  pvc_path = os.path.join(ROOT_DIR, 'k8s', 'db-pvc.yaml')
  pvc_tmpl = open(pvc_path, 'rt').read()
  pvc_text = pvc_tmpl.format(size=size, name=name)
  pvc = yaml.safe_load(pvc_text)

  kopf.adopt(pvc)

  api = kubernetes.client.CoreV1Api()
  try:
    api.create_namespaced_persistent_volume_claim(
        namespace=pvc['metadata']['namespace'],
        body=pvc,
    )
  except ApiException as e:
    print("Exception when calling CoreV1Api->create_namespaced_persistent_volume_claim: %s\n" % e)


@kopf.on.update('anirudh.io', 'v1', 'pythonapps')
def update_fn(spec, name, **kwargs):
  size = spec.get('db_size')
  pvc_path = os.path.join(ROOT_DIR, 'k8s', 'db-pvc.yaml')
  pvc_tmpl = open(pvc_path, 'rt').read()
  pvc_text = pvc_tmpl.format(size=size, name=name)
  pvc = yaml.safe_load(pvc_text)

  kopf.adopt(pvc)

  # Actually patch an object by requesting the Kubernetes API.
  api = kubernetes.client.CoreV1Api()
  try:
    api.patch_namespaced_persistent_volume_claim(namespace=pvc['metadata']['namespace'], body=pvc)
  except ApiException as e:
    print("Exception when calling AppsV1Api->update_namespaced_deployment: %s\n" % e)
