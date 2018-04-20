from kubernetes import client,config

# To run this locally, load your local kubeconfig with
#config.load_kube_config()

# Inside a cluster load the service account default kubeconfig with
config.load_incluster_config()

v1=client.CoreV1Api()

body = client.V1DeleteOptions()

def delete_pod(event, context):
    name = event['data']['name']
    namespace = event['data']['namespace']
    v1.delete_namespaced_pod(name=name, namespace=namespace, body=body)
