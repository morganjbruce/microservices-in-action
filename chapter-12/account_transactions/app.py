import datetime
import json
import logging
import time
from random import randint

from logstash_formatter import LogstashFormatterV1
from nameko.rpc import rpc
from statsd import StatsClient


class AccountTransactionsService:
    name = "account_transactions_service"
    statsd = StatsClient('statsd', 8125,
                         prefix='simplebank-demo.account-transactions')

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = LogstashFormatterV1()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    @rpc
    @statsd.timer('request_reservation')
    def request_reservation(self, payload):
        # introduce random sleep time to simulate processing
        time.sleep(randint(0, 9))

        self.logger.info("reserving position", extra={
            "uuid": payload})

        return payload

    @rpc
    @statsd.timer('health')
    def health(self, _request):
        return json.dumps({'ok': datetime.datetime.utcnow().__str__()})
