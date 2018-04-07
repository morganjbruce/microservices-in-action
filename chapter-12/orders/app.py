import datetime
import json
import time
from random import randint

from nameko.events import EventDispatcher, event_handler
from nameko.rpc import RpcProxy, rpc

from simplebank.chassis import init_logger, init_statsd


class OrdersService:
    name = "orders_service"
    dispatch = EventDispatcher()
    accounts = RpcProxy("account_transactions_service")
    statsd = init_statsd('simplebank-demo.orders', 'statsd')
    logger = init_logger()

    @rpc
    @statsd.timer('sell_shares')
    def sell_shares(self, request):
        payload = request

        # introduce random sleep time to simulate processing
        time.sleep(randint(0, 9))

        self.logger.info("sell request received", extra={
            "uuid": payload})

        # event: emit order created event
        self.__create_event("order_created", payload)

        # rpc to accounts: reservation of x units of y shares against account z
        self.__request_reservation(payload)

        return json.dumps({"ok": "sell order placed"})

    @statsd.timer('create_event')
    def __create_event(self, event, payload):
        self.logger.info("order created", extra={
            "uuid": payload})

        return self.dispatch(event, payload)

    @rpc
    @statsd.timer('request_reservation')
    def __request_reservation(self, payload):
        self.logger.info("requesting reservation to accounts service", extra={
            "uuid": payload})

        res = u"{}".format(payload)
        return self.accounts.request_reservation(res)

    @event_handler("market_service", "order_placed")
    @statsd.timer('place_order')
    def handle_place_order(self, payload):
        self.logger.info("updating the order status", extra={
            "uuid": payload, "status": "placed"})

        return payload

    @rpc
    @statsd.timer('health')
    def health(self, _request):
        return json.dumps({'ok': datetime.datetime.utcnow().__str__()})
