import opentracing
import requests
from flask import Flask, jsonify, request
from opentracing.ext import tags
from opentracing.propagation import Format

from lib.tracing import init_tracer

app = Flask(__name__)
tracer = init_tracer('simplebank-profile')


@app.route('/profile')
def pull_requests():
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
    # Fetch a list of pull requests on the opentracing repository
    # Fetch a list of pull requests on the opentracing repository
    jsontest_url = "http://ip.jsontest.com/"

    with tracer.start_span('settings', child_of=span_ctx, tags=span_tags):
        with tracer.start_span('jsontest', child_of=span_ctx) as span:
            span.set_tag("http.url", jsontest_url)
            r = requests.get(jsontest_url)
            span.set_tag("http.status_code", r.status_code)

        with tracer.start_span('parse-json', child_of=span_ctx) as span:
            json = r.json()
            span.set_tag("ip", len(json))

    return jsonify(json)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
