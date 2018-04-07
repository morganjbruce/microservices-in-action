import datetime
import json
import time
from random import randint

import requests
from circuitbreaker import circuit
from nameko.events import EventDispatcher, event_handler
from nameko.rpc import rpc

from simplebank.chassis import init_logger, init_statsd


class MarketService:
    name = "market_service"
    statsd = init_statsd('simplebank-demo.market', 'statsd')
    logger = init_logger()
    dispatch = EventDispatcher()

    @event_handler("orders_service", "order_created")
    @statsd.timer('request_reservation')
    def place_order(self, uuid):
        self.logger.info("requesting reservation", extra={
            "uuid": uuid})

        # place order in stock exchange
        exchange_resp = self.__place_order_exchange(uuid)
        # event: emit order placed event
        self.__create_event("order_placed", uuid)

        return json.dumps({'exchange_response': exchange_resp})

    @rpc
    @statsd.timer('create_event')
    def __create_event(self, event, uuid):
        # introduce random sleep time to simulate processing
        time.sleep(randint(0, 9))

        return self.dispatch(event, uuid)

    @statsd.timer('place_order_stock_exchange')
    @circuit(failure_threshold=5, expected_exception=ConnectionError)
    def __place_order_exchange(self, uuid):
        self.logger.info("placing order in the exchange", extra={
            "uuid": uuid})

        response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
        return json.dumps({'code': response.status_code, 'body': response.text})
