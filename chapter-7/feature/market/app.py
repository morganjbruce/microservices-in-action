import json
import datetime
import requests
from nameko.rpc import rpc
from nameko.events import EventDispatcher, event_handler
from statsd import StatsClient
from circuitbreaker import circuit


class MarketService:
    name = "market_service"
    statsd = StatsClient('statsd-agent', 8125,
                         prefix='simplebank-demo.market')

    dispatch = EventDispatcher()

    @event_handler("orders_service", "order_created")
    @statsd.timer('request_reservation')
    def place_order(self, payload):
        print("service {} received: {} ... placing order to exchange".format(
            self.name, payload))

        # place order in stock exchange
        exchange_resp = self.__place_order_exchange(payload)
        # event: emit order placed event
        self.__create_event("order_placed", payload)

        return json.dumps({'exchange_response': exchange_resp})

    @rpc
    @statsd.timer('create_event')
    def __create_event(self, event, payload):
        print("[{}] {} emiting {} event".format(
            payload, self.name, event))
        return self.dispatch(event, payload)

    @statsd.timer('place_order_stock_exchange')
    @circuit(failure_threshold=5, expected_exception=ConnectionError)
    def __place_order_exchange(self, request):
        print("[{}] {} placing order to stock exchange".format(
            request, self.name))
        response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
        return json.dumps({'code': response.status_code, 'body': response.text})
