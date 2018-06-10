Listing 10.1 A basic Jenkinsfile

```
stage("Build Info") {
  node {
    def commit = checkout scm
    echo "Latest commit id: ${commit.GIT_COMMIT}"
  }
}
```

Listing 10.3 Jenkinsfile for build step

```
def withPod(body) {
  podTemplate(label: 'pod', serviceAccount: 'jenkins', containers: [
      containerTemplate(name: 'docker', image: 'docker', command: 'cat', ttyEnabled: true),
      containerTemplate(name: 'kubectl', image: 'lachlanevenson/k8s-kubectl', command: 'cat', ttyEnabled: true)
    ],
    volumes: [
      hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
    ]
 ) { body() }
}

withPod {
  node('pod') {
    def tag = "${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
    def service = "market-data:${tag}"

    checkout scm

    container('docker') {
      stage('Build') {
        sh("docker build -t ${service} .")
      }
    }
  }
}
```

Listing 10.4 Test stage

```
stage('Test') {
  sh("docker run --rm ${service} python setup.py test")
}
```

Listing 10.5 Archiving results from test stage

```
stage('Test') {
  try {
    sh("docker run -v `pwd`:/workspace --rm ${service} python setup.py test")
  } finally {
    step([$class: 'JUnitResultArchiver', testResults: 'results.xml'])
  }
}
```

Listing 10.6 Publishing artifacts

```
def tagToDeploy = "[your-account]/${service}"

stage('Publish') {
  withDockerRegistry(registry: [credentialsId: 'dockerhub']) {
    sh("docker tag ${service} ${tagToDeploy}")
    sh("docker push ${tagToDeploy}")
  }
}
```

Listing 10.7 Deployment specification for market-data

```
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: market-data
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 50%
      maxSurge: 50%
  template:
    metadata:
      labels:
        app: market-data
        tier: backend
        track: stable
    spec:
      containers:
      - name: market-data
        image: BUILD_TAG
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /ping
            port: 8000
          initialDelaySeconds: 10
          timeoutSeconds: 15
        readinessProbe:
          httpGet:
            path: /ping
            port: 8000
          initialDelaySeconds: 10
          timeoutSeconds: 15
```

Listing 10.8 Market data service definition

```
---
apiVersion: v1
kind: Service
metadata:
  name: market-data
spec:
  type: NodePort
  selector:
    app: market-data
    tier: backend
  ports:
    - protocol: TCP
      port: 8000
      nodePort: 30623
```

Listing 10.9 Deployment to staging

```
stage('Deploy') {
  sh("sed -i.bak 's#BUILD_TAG#${tagToDeploy}#' ./deploy/staging/*.yml")

  container('kubectl') {
    sh("kubectl --namespace=staging apply -f deploy/staging/")
  }
}
```

Listing 10.10 Deployment status

```
kubectl rollout status –n staging deployment/market-data
```

Listing 10.12 Approving a production release

```
stage('Approve release?') {
  input message: "Release ${tagToDeploy} to production?"
}
```

Listing 10.13 Production release stage

```
stage('Deploy to production') {

  sh("sed -i.bak 's#BUILD_TAG#${tagToDeploy}#' ./deploy/production/*.yml")

  container('kubectl') {
    sh("kubectl --namespace=production apply -f deploy/production/")
  }
}
```

Listing 10.14 deploy.groovy

```
def toKubernetes(tagToDeploy, namespace, deploymentName) {
  sh("sed -i.bak 's#BUILD_TAG#${tagToDeploy}#' ./deploy/${namespace}/*.yml")

  kubectl("apply -f deploy/${namespace}/")
}

def kubectl(namespace, command) {
  container('kubectl') {
    sh("kubectl --namespace=${namespace} ${command}")
  }
}

def rollback(deploymentName) {
  kubectl("rollout undo deployment/${deploymentName}")
}

return this;
```

Listing 10.15 Using deploy.groovy in your Jenkinsfile

```
def deploy = load('deploy.groovy')

stage('Deploy to staging') {
  deploy.toKubernetes(tagToDeploy, 'staging', 'market-data')
}

stage('Approve release?') {
  input "Release ${tagToDeploy} to production?"
}

stage('Deploy to production') {
  deploy.toKubernetes(tagToDeploy, 'production', 'market-data')
}
```

Listing 10.16 Canary release stage

```
stage('Deploy canary') {
  deploy.toKubernetes(tagToDeploy, 'canary', 'market-data-canary')

  try {
    input message: "Continue releasing ${tagToDeploy} to production?" #A
  } catch (Exception e) {
    deploy.rollback('market-data-canary') #B
  }
}
```

Listing 10.17 Example declarative build pipeline

```
service {
  name('market-data')

  stages {
    build()
    test(command: 'python setup.py test', results: 'results.xml')
    publish()
    deploy()
  }
}
```
