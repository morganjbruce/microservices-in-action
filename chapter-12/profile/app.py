from urlparse import urljoin

import opentracing
import requests
from flask import Flask, jsonify, request
from opentracing.ext import tags
from opentracing.propagation import Format
from opentracing_instrumentation.request_context import (get_current_span,
                                                         span_in_context)

from simplebank.chassis import init_logger, init_statsd, init_tracer

app = Flask(__name__)
tracer = init_tracer('simplebank-profile')
statsd = init_statsd('simplebank.profile', 'statsd')
logger = init_logger()


@app.route('/profile/<uuid:uuid>')
@statsd.timer('profile')
def profile(uuid):
    logger.debug("this is a debug message from profile", extra={"uuid": uuid})

    with tracer.start_span('settings') as span:
        span.set_tag('uuid', uuid)
        with span_in_context(span):
            ip = get_ip(uuid)
            settings = get_user_settings(uuid)
            return jsonify({'ip': ip, 'settings': settings})


@statsd.timer('get_ip')
def get_ip(uuid):
    logger.info("getting ip", extra={"uuid": uuid})
    with tracer.start_span('get_ip', child_of=get_current_span()) as span:
        span.set_tag('uuid', uuid)
        with span_in_context(span):
            jsontest_url = "http://ip.jsontest.com/"
            r = requests.get(jsontest_url)
            return r.json()


@statsd.timer('get_user_settings')
def get_user_settings(uuid):
    logger.info("getting user settings", extra={"uuid": uuid})
    settings_url = urljoin("http://settings:5000/settings/", "{}".format(uuid))

    span = get_current_span()
    span.set_tag(tags.HTTP_METHOD, 'GET')
    span.set_tag(tags.HTTP_URL, settings_url)
    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
    span.set_tag('uuid', uuid)
    headers = {}
    tracer.inject(span, Format.HTTP_HEADERS, headers)

    r = requests.get(settings_url, headers=headers)
    return r.json()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
