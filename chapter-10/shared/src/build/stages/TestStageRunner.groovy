package build.stages

class TestStageRunner implements Serializable {
  def script
  def config = [:]

  TestStageRunner(script, config) {
    this.script = script
    this.config = config
  }

  void run(ServiceConfig service) {
    script.stage('Test') {
      try {
        script.sh("""docker run \
            -v `pwd`:/workspace
            -w workspace --rm ${service.tag()} \
            ${config.command}""")
      } finally {
        script.step([$class: 'JUnitResultArchiver', testResults: config.results])
      }
    }
  }
}
