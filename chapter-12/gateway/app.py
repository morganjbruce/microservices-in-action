import datetime
import json
import logging
import time
import uuid

from logstash_formatter import LogstashFormatterV1
from nameko.rpc import RpcProxy, rpc
from nameko.web.handlers import http

from statsd import StatsClient
from werkzeug.wrappers import Request, Response


class Gateway:

    name = "gateway"

    orders = RpcProxy("orders_service")
    statsd = StatsClient('statsd', 8125,
                         prefix='simplebank-demo.gateway')

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = LogstashFormatterV1()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    @http('POST', '/shares/sell')
    @statsd.timer('sell_shares')
    def sell_shares(self, request):
        req_id = uuid.uuid4()
        res = u"{}".format(req_id)

        self.logger.debug(
            "this is a debug message from gateway", extra={"uuid": res})
        self.logger.info("placing sell order", extra={"uuid": res})

        self.__sell_shares(res)

        return Response(json.dumps(
            {"ok": "sell order {} placed".format(req_id)}),
            mimetype='application/json')

    @rpc
    def __sell_shares(self, uuid):
        self.logger.info("contacting orders service", extra={
            "uuid": uuid})

        # import pdb
        # pdb.set_trace()

        res = u"{}".format(uuid)
        return self.orders.sell_shares(res)

    @http('GET', '/health')
    @statsd.timer('health')
    def health(self, _request):
        return json.dumps({'ok': datetime.datetime.utcnow().__str__()})
