import logging

from jaeger_client import Config
from logstash_formatter import LogstashFormatterV1
from statsd import StatsClient


def init_statsd(prefix=None, host=None, port=8125):
    statsd = StatsClient(host, port, prefix=prefix)
    return statsd


def init_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = LogstashFormatterV1()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def init_tracer(service):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': "jaeger",
                'reporting_port': 5775,
            },
            'logging': True,
            'reporter_batch_size': 1,
        },

        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()
