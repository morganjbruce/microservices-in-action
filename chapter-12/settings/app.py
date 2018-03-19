import time
from random import randint

import requests
from flask import Flask, jsonify, request
from opentracing.ext import tags
from opentracing.propagation import Format
from opentracing_instrumentation.request_context import (get_current_span,
                                                         span_in_context)

from simplebank.chassis import init_logger, init_statsd, init_tracer

app = Flask(__name__)
tracer = init_tracer('simplebank-settings')
statsd = init_statsd('simplebank.settings', 'statsd')
logger = init_logger()


@app.route('/settings/<uuid:uuid>')
@statsd.timer('settings')
def settings(uuid):
    logger.info("fetching user settings", extra={"uuid": uuid})
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER, 'uuid': uuid}

    with tracer.start_span('settings', child_of=span_ctx, tags=span_tags):
        time.sleep(randint(0, 2))
        return jsonify({'settings': {'name': 'demo user', 'uuid': uuid}})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
