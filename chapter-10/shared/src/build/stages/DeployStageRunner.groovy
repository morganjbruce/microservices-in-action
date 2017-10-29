package build.stages

class DeployStageRunner implements Serializable {
  def script
  def config = [:]

  DeployStageRunner(script, config) {
    this.script = script
    this.config = config
  }

  void run(ServiceConfig service) {

// TODO!!!

  stage('Deploy to staging') {
    deploy.toKubernetes(tagToDeploy, 'staging', 'market-data')
  }

  stage('Approve release?') {
    input message: "Release ${tagToDeploy} to production?"
  }

  stage('Deploy to production') {
    deploy.toKubernetes(tagToDeploy, 'production', 'market-data')
  }

  stage('Deploy canary') {
    deploy.toKubernetes(tagToDeploy, 'canary', 'market-data-canary')

    try {
      input message: "Continue releasing ${tagToDeploy} to production?"
    } catch (Exception e) {
      deploy.rollback('market-data-canary')
    }
  }



  }
}
