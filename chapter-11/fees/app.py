import datetime
import json

from nameko.events import EventDispatcher, event_handler

from simplebank.chassis import init_logger, init_statsd


class FeesService:
    name = "fees_service"
    statsd = init_statsd('simplebank-demo.fees', 'statsd')

    @event_handler("market_service", "order_placed")
    @statsd.timer('charge_fee')
    def charge_fee(self, payload):
        print("[{}] {} received order_placed event ... charging fee".format(
            payload, self.name))
