# Function to kill pod

```
kubeless function deploy --from-file killer.py --dependencies requirements.txt --runtime python2.7 --handler killer.delete_pod killerpod
```

Delete a Pod by calling the function

```
kubeless function call killerpod --data '{"name":"foo-87555cb4c-lr6rw","namespace":"default"}'
```

WARNING:

For the function to work you need to change the default service account used by kubeless.

First create a service account with the proper privileges:

```
kubectl create serviceaccount falco
kubectl create role falco --verb=get,list,delete --resource=pods
kubectl create rolebinding falco --role=falco --serviceaccount=default:falco
```


Edit the kubeless configmap to specific a serviceAccountName in the deployment object:

```
$ kubectl get cm -n kubeless -o yaml
apiVersion: v1
items:
- apiVersion: v1
  data:
    builder-image: kubeless/function-image-builder:v0.6.0
    deployment: |-
      spec:
        template:
          serviceAccountName: falco
    enable-build-step: "false"
    function-registry-tls-verify: "true"
    ingress-enabled: "false"
    runtime-images: |-

```

Delete the controller pods in the kubeless namespac so that a new controller starts with this new configuration.

Recreate your function with the `kubeless` CLI. it should now run with the _falco_ service account and should be able to delete Pods.

You can hot fix this, by editing the deployment corresponding to your function and adding a `serviceAccountName` in the spec directly, then killing hte pod of the function. A new pod will get restarted running under the _falco_ service account.

