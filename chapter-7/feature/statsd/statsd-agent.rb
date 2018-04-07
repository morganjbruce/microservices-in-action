#!/usr/bin/env ruby
#
# This script is found in this post by Lee Hambley
# http://lee.hambley.name/2013/01/26/dirt-simple-statsd-server-for-local-development.html
#
require 'socket'
require 'term/ansicolor'

include Term::ANSIColor

$stdout.sync = true

c = Term::ANSIColor
s = UDPSocket.new
s.bind("0.0.0.0", 8125)
while blob = s.recvfrom(1024)
  metric, value = blob.first.split(':')
  puts "StatsD Metric: #{c.blue(metric)} #{c.green(value)}"
end
