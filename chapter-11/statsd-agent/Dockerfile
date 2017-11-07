FROM alpine:3.6

MAINTAINER simplebank <engineering@simplebenak.book>

ARG port="8125"
ARG home="/root/"
ARG app_root="/var/code/simplebank/"
ARG app_name="statsd-agent"

ENV TERM xterm
ENV LANG=en_GB.UTF-8
ENV HOME $home

ENV REFRESHED_AT 2016-11-25

COPY . $app_root$app_name

RUN apk update && apk --update add \
      ruby \
      ruby-irb \
      ruby-json \
      ruby-rake \
      ruby-bigdecimal \
      ruby-io-console \
      libstdc++ \
      tzdata \
      ca-certificates \
      bash

RUN gem install bundler --no-ri --no-rdoc \
    && cd $app_root$app_name ; bundle install \
    && rm -rf /var/cache/apk/*

RUN chown -R nobody:nogroup $app_root$app_name
RUN chmod +x $app_root$app_name/statsd-agent.rb

USER nobody

EXPOSE $port/udp

WORKDIR $app_root$app_name

CMD ./$app_root$app_name/statsd-agent.rb
