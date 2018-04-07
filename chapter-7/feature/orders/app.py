import json
import datetime
from nameko.events import EventDispatcher, event_handler
from nameko.rpc import rpc, RpcProxy
from statsd import StatsClient


class OrdersService:
    name = "orders_service"
    dispatch = EventDispatcher()

    accounts = RpcProxy("account_transactions_service")
    statsd = StatsClient('statsd-agent', 8125,
                         prefix='simplebank-demo.orders')

    @rpc
    @statsd.timer('sell_shares')
    def sell_shares(self, request):
        payload = request

        # event: emit order created event
        self.__create_event("order_created", payload)

        # rpc to accounts: reservation of x units of y shares against account z
        self.__request_reservation(payload)

        return json.dumps({"ok": "sell order placed"})

    @statsd.timer('create_event')
    def __create_event(self, event, payload):
        return self.dispatch(event, payload)

    @rpc
    @statsd.timer('request_reservation')
    def __request_reservation(self, payload):
        print("[{}] rpc to accounts service : request reservation".format(payload))
        res = u"{}".format(payload)
        return self.accounts.request_reservation(res)

    @event_handler("market_service", "order_placed")
    @statsd.timer('place_order')
    def handle_place_order(self, payload):
        print("[{}] {} received order_placed event ... updating order to placed".format(
            payload, self.name))

    @rpc
    @statsd.timer('health')
    def health(self, _request):
        return json.dumps({'ok': datetime.datetime.utcnow().__str__()})
