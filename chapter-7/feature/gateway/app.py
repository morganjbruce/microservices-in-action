import datetime
import uuid
import json
from nameko.web.handlers import http
from nameko.rpc import rpc, RpcProxy
from werkzeug.wrappers import Request, Response
from statsd import StatsClient


class Gateway:

    name = "gateway"
    orders = RpcProxy("orders_service")
    statsd = StatsClient('statsd-agent', 8125,
                         prefix='simplebank-demo.gateway')

    @http('POST', '/shares/sell')
    @statsd.timer('sell_shares')
    def sell_shares(self, request):
        req_id = uuid.uuid4()
        res = u"{}".format(req_id)
        req = self.__sell_shares(res)
        return Response(json.dumps(
            {"ok": "sell order {} placed".format(req_id)}),
            mimetype='application/json')

    @rpc
    def __sell_shares(self, payload):
        print("[{}] rpc to orders service : sell_shares".format(payload))
        res = u"{}".format(payload)
        return self.orders.sell_shares(res)

    @http('GET', '/health')
    @statsd.timer('health')
    def health(self, _request):
        return json.dumps({'ok': datetime.datetime.utcnow().__str__()})
