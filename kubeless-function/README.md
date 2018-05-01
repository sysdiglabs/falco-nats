# Kubeless Function to Delete Kubernetes Pod

This Kubeless function will delete a pod when a Falco alert is recieved from the NATS server topic `FALCO`. The Pod will only be deleted if the Falco alert is of `Critical` priority. Follow the [quick start instructions](http://kubeless.io/docs/quick-start/) on the Kubeless site to deploy Kubeless.

Deploy the function as below.

```
kubeless function deploy --from-file delete-pod.py --dependencies requirements.txt --runtime python2.7 --handler delete-pod.delete_pod falco-pod-delete
INFO[0000] Deploying function...                        
INFO[0000] Function falco-pod-delete submitted for deployment 
INFO[0000] Check the deployment status executing 'kubeless function ls falco-pod-delete'
```

Follow the instructions in the Kubeless quick start to create a NATS trigger controller and a trigger for our delete pod function. 

```
$ kubectl create -f https://github.com/kubeless/kubeless/releases/download/$RELEASE/nats-$RELEASE.yaml
customresourcedefinition "natstriggers.kubeless.io" created
deployment "nats-trigger-controller" created
clusterrole "nats-controller-deployer" created
clusterrolebinding "nats-controller-deployer" created

$ kubeless trigger nats create falco-delete-pod-trigger --function-selector created-by=kubeless,function=falco-pod-delete --trigger-topic FALCO
INFO[0000] NATS trigger falco-delete-pod-trigger created in namespace default successfully!

```

WARNING:

For the function to work you need to change the default service account used by kubeless.

First create a service account with the proper privileges:

```
kubectl create -f falco-pod-delete-account.yaml
```


Kubeless doesn't support specifying a `serviceAccountName` for a deployed function. As a workaround, edit the kubeless deployment to specific a `serviceAccountName` in the deployment object:

```
$ kubectl edit deployment falco-pod-delete
      securityContext:
        fsGroup: 1000
        runAsUser: 1000
 +    serviceAccountName: falco-pod-delete
      terminationGracePeriodSeconds: 30
      volumes:

```

Kubernetes should start a new Pod running with the new `serviceAccount`. Else delete the pod associated with the kubeless deployment.

```
$ kubectl delete pod falco-pod-delete-<pod_id>
```

Confirm the new service account on the new Pod.
```
$ kubectl get pod falco-pod-delete-<pod_id> -o yaml |grep serviceAccount
  serviceAccount: falco-pod-delete
  serviceAccountName: falco-pod-delete
```

When a Pod is deleted, the action is logged to the `stdout` of the `falco-pod-delete` Pod.