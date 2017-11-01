FROM prom/statsd-exporter
ADD statsd_mapping.conf /tmp/statsd_mapping.conf
#CMD [ "./statsd_bridge", "-statsd.listen-address=\":8125\"", "-statsd.mapping-config=\"\""", "-web.listen-address=\"127.0.0.1:9090\"", "-web.telemetry-path=\"/metrics\"" ]
CMD ["tail", "-f", "/dev/null"]
