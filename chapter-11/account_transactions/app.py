import json
import datetime
from nameko.rpc import rpc
from simplebank.chassis import init_logger, init_statsd


class AccountTransactionsService:
    name = "account_transactions_service"
    statsd = init_statsd('simplebank-demo.account-transactions', 'statsd')

    @rpc
    @statsd.timer('request_reservation')
    def request_reservation(self, payload):
        print("[{}] {} received request to reserve stocks... reserving".format(
            payload, self.name))

    @rpc
    @statsd.timer('health')
    def health(self, _request):
        return json.dumps({'ok': datetime.datetime.utcnow().__str__()})
