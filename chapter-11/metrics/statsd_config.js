(function() {
  return {
      // Configuration
      repeater:[
          {host: "statsd-exporter",
          port: 9125}
      ],
      backends: [ "./backends/repeater" ]
  };
})()
