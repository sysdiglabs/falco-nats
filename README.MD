# Active Kubernetes Security with Falco, NATS, & kubeless 

This is a proof of concept that uses a Go NATS client to take alerts from Sysdig Falco and publish them to a NATS messaging server. Falco will detect abnormal behavior of the Kubernetes cluster in which it runs, then send an alert to the NATS client. This forwards the alert to the NATS Server. Subscribers can then subcribe to the subject `FALCO` on the NATS server to see Falco alerts, and take action on the alerts. A kubeless function is provided as an example to delete a Pod when a `CRITICAL` Falco alert is recieved. Multiple subscribers can take action on the same alert; for instance one archiving the alert, and another deleting the offending Pod.

## falco-config

This contains Falco rules and a Falco config file. The rules are the default rules for Falco. The configuration file has been modified from the original as follows.

```
json_output: true
```

This changes the default output format to use a JSON output format instead of a logging output format.

```
# line. If keep_alive is set to false, the file will be re-opened
# for each output message.
#
# Also, the file will be closed and reopened if falco is signaled with
# SIGUSR1.

file_output:
  enabled: true
  keep_alive: true
  filename: /var/run/falco/nats

stdout_output:
  enabled: true

```

This enables sending Falco alerts to a file. Set `enabled` and `keep_alive` to true, and change the `filename` to the value shown. `keep_alive` is set to `true` because `/var/run/falco/nats` is actually a [named pipe](https://www.linuxjournal.com/article/2156) that the NATS client will read from.

## falco-nats

This folder has a Go program that reads from the named pipe `/var/run/falco/nats` and publishes each Falco alert to the specified NATS server. Set your Docker org in the `Makefile`, then run `make` to build the Go program, and a container to run the client in. You'll need a [Go development environement](https://golang.org/doc/install) and the [Go NATS Client](https://github.com/nats-io/go-nats).

The resulting `nats-pub` executable takes the following options.

```
	-s  The NATS server to connect to. Default: nats://nats:4222
	-f  The named pipe to read from. Default: /var/run/falco/nats
```

For a NATS Server that can be deployed to Kubernetes, we leveraged [the example](http://kubeless.io/docs/quick-start/) in the Kubeless quick start. 

##  falco-daemonset-configmap.yaml

This deploys Falco and the falco-nats container as a Kubernetes daemonset. It also deploys an [Init Container](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) that creates a Linux named pipe on a shared volume. This volume is shared between the Falco container and the NATS client, and the named pipe is used to pass the Falco alerts between the two containers. This daemon set has the following changes from the [published version](https://github.com/draios/falco/tree/dev/examples/k8s-using-daemonset) for Falco.

```
    spec:
      serviceAccount: falco-account
      containers:
        - name: falco-nats
          image: sysdiglabs/falco-nats:latest
          imagePullPolicy: Always
          volumeMounts:
            - mountPath: /var/run/falco/
              name: shared-pipe
        - name: falco
          image: sysdig/falco:latest
```

Added the container for the NATS client. 

```
          args: [ "/usr/bin/falco", "-K", "/var/run/secrets/kubernetes.io/serviceaccount/token", "-k", "https://kubernetes", "-pk", "-U"]
          volumeMounts:
            - mountPath: /var/run/falco/
              name: shared-pipe
              readOnly: false
            - mountPath: /host/var/run/docker.sock
```
Added a `volumeMount` for our shared named pipe to the `falco` container.

```
              name: falco-config
      initContainers:
          - name: init-pipe
            image: busybox
            command: ['mkfifo','/var/run/falco/nats']
            volumeMounts:
            - mountPath: /var/run/falco/
              name: shared-pipe
              readOnly: false
      volumes:
        - name: shared-pipe
          emptyDir: {}
        - name: docker-socket
```
Added an Init Container to create the named pipe. This helps us ensure the pipe is available for either container, as the Init Container must finish before either application container starts.

To deploy the DaemonSet, run the below.

```
falco-nats$ kubectl create configmap falco-config --from-file=falco-config/
configmap "falco-config" created
falco-nats$ kubectl create -f falco-account.yaml
serviceaccount "falco-account" created
clusterrole "falco-cluster-role" created
clusterrolebinding "falco-cluster-role-binding" created
falco-nats$ kubectl create -f falco-daemonset-configmap.yaml
daemonset "falco" created
```

The daemonset can be verified by tailing the `falco-nat` container logs in one terminal, and shelling into the the `falco` container in another. This should send an alert that a shell was opened in a container.

```
# terminal 1
falcoless$ kubectl logs -f falco-75r25 falco-nats
Opened pipe /var/run/falco/nats
Scanning /var/run/falco/
Published [FALCO] : '{"output":"16:57:40.936641184: Notice A shell was spawned in a container with an attached terminal (user=root k8s.pod=falco-b5hk7 container=7f25ca3dfdd1 shell=bash parent=<NA> cmdline=bash  terminal=34816)","priority":"Notice","rule":"Terminal shell in container","time":"2018-04-19T16:57:40.936641184Z", "output_fields": {"container.id":"7f25ca3dfdd1","evt.time":1524157060936641184,"k8s.pod.name":"falco-b5hk7","proc.cmdline":"bash ","proc.name":"bash","proc.pname":null,"proc.tty":34816,"user.name":"root"}}'


# terminal 2
falco-nats$ kubectl exec -it falco-75r25 -c falco -- bash
```

## nodejs-app

This is an application that can be exploited via unsanitized data in a cookie. See the [README.MD](nodejs-app/README.MD) in the `nodejs-app` for more details.

## kubeless-function

This is a kubeless function that subscribes to the NATS `FALCO` subject on the NATS server and fires when an alert is recieved. See the [README.MD](kubeless-function/README.MD) for more details. 
