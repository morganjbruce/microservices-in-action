package build.stages

class BuildStageRunner implements Serializable {
  def script
  def config = [:]

  BuildStageRunner(script, config) {
    this.script = script
    this.config = config
  }

  void run(ServiceConfig service) {
    script.stage('Build') {
      script.sh("docker build -t ${service.tag()} .")
    }
  }
}
