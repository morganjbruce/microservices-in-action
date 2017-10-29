package build.stages

class PublishStageRunner implements Serializable {
  def script
  def config = [:]

  PublishStageRunner(script, config) {
    this.script = script
    this.config = config
  }

  void run(ServiceConfig service) {
    script.stage('Publish') {
      script.withDockerRegistry(registry: [credentialsId: 'dockerhub']) {
        script.sh("docker push ${service.tagToDeploy()}")
      }
    }
  }
}
