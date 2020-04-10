# simplebank
App for the Microservices In Action book (https://www.manning.com/books/microservices-in-action)

#### Stop all simplebank containers running
```bash
docker stop $(docker ps | grep simplebank | awk '{print $1}')
```

#### Remove all simplebank containers to prevent any name clashes
```bash
docker rm $(docker ps -a | grep simplebank | awk '{print $1}')
```

#### Start all services
```bash
docker-compose up --build --remove-orphans
```

After following the described steps to configure Grafana you may use `siege` to
generate load on the services being monitored. This way you will be able to see
collected metrics on the `Place Order Dashboard`

To make requests for 5 minutes, with a concurrency setting of 50, issue the following
siege command on a terminal window in your host machine:

`siege -c50 -t300S --content-type "application/json" 'http://localhost:5001/shares/sell POST'`