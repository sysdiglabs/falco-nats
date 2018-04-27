from kubernetes import client,config

# To run this locally, load your local kubeconfig with
#config.load_kube_config()

# Inside a cluster load the service account default kubeconfig with
config.load_incluster_config()

v1=client.CoreV1Api()

body = client.V1DeleteOptions()


def find_pod_ns(podname=None):
    ns=None
    response=v1.list_pod_for_all_namespaces(watch=False)
    for i in response.items:
        if i.metadata.name == podname:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
            ns=i.metadata.namespace
            break

    return ns        

def delete_pod(event, context):
    priority = event['data']['priority'] or None
    output_fields = event['data']['output_fields'] or None

    if priority and priority == "Critical"  and output_fields and output_fields['container.id'] != "host":
        name = output_fields['k8s.pod.name']
        print 'Critcal Falco alert for pod: {} '.format(name)

        ns=find_pod_ns(name)
        print 'Deleting POD {} in NameSpace {}'.format(name, ns)
        v1.delete_namespaced_pod(name=name, namespace=ns, body=body)