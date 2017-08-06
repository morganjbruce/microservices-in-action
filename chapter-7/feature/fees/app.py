import json
import datetime
from nameko.events import EventDispatcher, event_handler
from statsd import StatsClient


class FeesService:
    name = "fees_service"
    statsd = StatsClient('statsd-agent', 8125,
                         prefix='simplebank-demo.fees')

    @event_handler("market_service", "order_placed")
    @statsd.timer('charge_fee')
    def charge_fee(self, payload):
        print("[{}] {} received order_placed event ... charging fee".format(
            payload, self.name))
