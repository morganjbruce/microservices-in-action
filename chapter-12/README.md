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