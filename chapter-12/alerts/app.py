import datetime
import json
import logging
import uuid

from nameko.extensions import DependencyProvider
from nameko.web.handlers import http
from statsd import StatsClient
from werkzeug.wrappers import Request, Response

logger = logging.getLogger(__name__)


class Logger(DependencyProvider):

    def get_dependency(self, worker_ctx):
        def log(msg):
            logger.info("%s: %s" % (worker_ctx.call_id, msg))
        return log


class Alerts:

    name = "alerts"
    statsd = StatsClient('statsd', 8125,
                         prefix='simplebank-demo.alerts')
    log = Logger()

    @http('POST', '/')
    @statsd.timer('alert')
    def alert(self, request):
        self.log(request.get_data(as_text=True))
        return Response(request.get_data(), mimetype='application/json')

    @http('GET', '/health')
    @statsd.timer('health')
    def health(self, _request):
        return json.dumps({'ok': datetime.datetime.utcnow().__str__()})
