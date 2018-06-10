# simplebank
App for the Microservices In Action book (https://www.manning.com/books/microservices-in-action)

### Starting the services

```
cd chapter-7/feature

docker-compose up --build
```

### Figure 7.15 processing a request to the _shares/sell_ endpoint on the gateway

```
# pass a uuid on the POST request
curl -X POST -d '{"uuid": "65c2da7e-70e4-4195-a7e8-86e23d019161"}' http://localhost:5001/shares/sell

```

#### sample output  (`docker-compose logs -ft`)
```
simplebank-gateway      | 2018-06-10T12:54:07.669111816Z 192.168.64.1 - - [10/Jun/2018 12:54:07] "POST /shares/sell HTTP/1.1" 200 172 0.105845
simplebank-statsd-agent | 2018-06-10T12:54:07.816958709Z StatsD Metric: simplebank-demo.market.place_order_stock_exchange 243.629415|ms
simplebank-statsd-agent | 2018-06-10T12:54:07.824003919Z StatsD Metric: simplebank-demo.orders.place_order 0.019284|ms
simplebank-statsd-agent | 2018-06-10T12:54:07.827028091Z StatsD Metric: simplebank-demo.fees.charge_fee 0.020383|ms
simplebank-statsd-agent | 2018-06-10T12:54:07.846512401Z StatsD Metric: simplebank-demo.market.create_event 30.894470|ms
simplebank-statsd-agent | 2018-06-10T12:54:07.847059544Z StatsD Metric: simplebank-demo.market.request_reservation 275.100105|ms
simplebank-statsd-agent | 2018-06-10T12:54:18.140824320Z StatsD Metric: simplebank-demo.orders.create_event 55.777257|ms
simplebank-statsd-agent | 2018-06-10T12:54:18.145772952Z StatsD Metric: simplebank-demo.account-transactions.request_reservation 0.018784|ms
simplebank-statsd-agent | 2018-06-10T12:54:18.165861941Z StatsD Metric: simplebank-demo.orders.request_reservation 24.388455|ms
simplebank-statsd-agent | 2018-06-10T12:54:18.166518802Z StatsD Metric: simplebank-demo.orders.sell_shares 80.703471|ms
simplebank-statsd-agent | 2018-06-10T12:54:18.170951159Z StatsD Metric: simplebank-demo.gateway.sell_shares 88.776036|ms
```
