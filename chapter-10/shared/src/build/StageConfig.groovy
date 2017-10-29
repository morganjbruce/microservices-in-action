package build

class StageConfig implements Serializable {
  def script
  def stages = []

  StageConfig(script) {
    this.script = script
  }

  void build(Map config = [:]) {
    stages.add(new BuildStageRunner(script, config))
  }

  void test(Map config = [:]) {
    stages.add(new TestStageRunner(script, config))
  }

  void publish(Map config = [:]) {
    stages.add(new PublishStageRunner(script, config))
  }

  void deploy(Map config = [:]) {
    stages.add(new DeployStageRunner(script, config))
  }
}
