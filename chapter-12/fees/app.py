import datetime
import json

from nameko.events import EventDispatcher, event_handler

from simplebank.chassis import init_logger, init_statsd


class FeesService:
    name = "fees_service"
    statsd = init_statsd('simplebank-demo.fees', 'statsd')
    logger = init_logger()

    @event_handler("market_service", "order_placed")
    @statsd.timer('charge_fee')
    def charge_fee(self, payload):
        self.logger.debug(
            "this is a debug message from fees service", extra={"uuid": payload})
        self.logger.info("charging fees", extra={
            "uuid": payload})

        return payload
