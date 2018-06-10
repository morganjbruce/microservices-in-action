Listing A.4 Installing Jenkins

```
helm install
  --name jenkins
  --namespace jenkins
  --values values.yml
  stable/jenkins
```

Listing A.5 Retrieving an admin password

```
printf $(kubectl get secret --namespace jenkins jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo
```

Listing A.6 Opening the Jenkins login page

```
minikube --namespace=jenkins service jenkins
```
Listing A.7 Test pipeline script

```
podTemplate(label: 'build', containers: [
    containerTemplate(name: 'docker', image: 'docker', command: 'cat', ttyEnabled: true)
  ],
  volumes: [
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
  ]
  ) {
    node('build') {
      container('docker') {
        sh 'docker version'
      }        
    }  
  }
```
