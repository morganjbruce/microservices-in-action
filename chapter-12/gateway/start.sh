#!/usr/bin/env sh
AGENT_HOST=${AGENT_HOST:=jaeger-agent}
AGENT_PORT=${AGENT_PORT:=6831}

socat UDP4-RECVFROM:6831,fork UDP4-SENDTO:${AGENT_HOST}:${AGENT_PORT} &
nameko run --config config.yml app
