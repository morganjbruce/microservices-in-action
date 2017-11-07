(function() {
  return {
      // Configuration
      repeater:[
          {host: "statsd_exporter",
          port: 9125}
      ],
      backends: [ "./backends/repeater" ]
  };
})()
