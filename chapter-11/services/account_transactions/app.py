import json
import datetime
from nameko.rpc import rpc
from statsd import StatsClient


class AccountTransactionsService:
    name = "account_transactions_service"
    statsd = StatsClient('statsd-agent', 8125,
                         prefix='simplebank-demo.account-transactions')

    @rpc
    @statsd.timer('request_reservation')
    def request_reservation(self, payload):
        print("[{}] {} received request to reserve stocks... reserving".format(
            payload, self.name))

    @rpc
    @statsd.timer('health')
    def health(self, _request):
        return json.dumps({'ok': datetime.datetime.utcnow().__str__()})
