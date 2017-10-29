package build

def run(ServiceConfig config) {
  node {
    checkout scm

    config.stages.each { stage ->
      stage.run(config)
    }
  }
}
