import datetime
import json
import time
from random import randint

from nameko.rpc import rpc

from simplebank.chassis import init_logger, init_statsd


class AccountTransactionsService:
    name = "account_transactions_service"
    statsd = init_statsd('simplebank-demo.account-transactions', 'statsd')
    logger = init_logger()

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
