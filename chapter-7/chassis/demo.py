import json
import datetime
import requests
from nameko.web.handlers import http
from nameko.timer import timer
from statsd import StatsClient
from circuitbreaker import circuit


class DemoChassisService:
    name = "demo_chassis_service"

    statsd = StatsClient('localhost', 8125, prefix='simplebank-demo')

    @http('GET', '/health')
    @statsd.timer('health')
    def health(self, _request):
        return json.dumps({'ok': datetime.datetime.utcnow().__str__()})

    @http('GET', '/external')
    @circuit(failure_threshold=5, expected_exception=ConnectionError)
    @statsd.timer('external')
    def external_request(self, _request):
        response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
        return json.dumps({'code': response.status_code, 'body': response.text})

    @http('GET', '/error')
    @circuit(failure_threshold=5, expected_exception=ZeroDivisionError)
    @statsd.timer('http_error')
    def error_http_request(self):
        return json.dumps({1 / 0})


class HealthCheckService:
    name = "health_check_service"

    statsd = StatsClient('localhost', 8125, prefix='simplebank-demo')

    @timer(interval=10)
    @statsd.timer('check_demo_service')
    def check_demo_service(self):
        response = requests.get('http://0.0.0.0:8000/health')
        print("DemoChassisService HEALTH CHECK: status_code {}, response: {}".format(
            response.status_code, response.text))
