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
Edit the kubeless configmap to specific a serviceAccountName in the deployment object:

```
$ kubectl get cm -n kubeless -o yaml
apiVersion: v1
items:
- apiVersion: v1
  data:
    builder-image: kubeless/function-image-builder:v0.6.0
    deployment: '{}'
    enable-build-step: "false"
    function-registry-tls-verify: "true"
    ingress-enabled: "false"
    runtime-images: |-

```
