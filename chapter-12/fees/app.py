import datetime
import json
import logging

from logstash_formatter import LogstashFormatterV1
from nameko.events import EventDispatcher, event_handler
from statsd import StatsClient


class FeesService:
    name = "fees_service"
    statsd = StatsClient('statsd', 8125,
                         prefix='simplebank-demo.fees')

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = LogstashFormatterV1()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    @event_handler("market_service", "order_placed")
    @statsd.timer('charge_fee')
    def charge_fee(self, payload):
        self.logger.debug(
            "this is a debug message from fees service", extra={"uuid": payload})
        self.logger.info("charging fees", extra={
            "uuid": payload})

        return payload
