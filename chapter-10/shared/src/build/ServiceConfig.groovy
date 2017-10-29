package build

class ServiceConfig implements Serializable {
  def script
  def env
  def name
  def registry
  def stages

  ServiceConfig(script, env) {
    this.env = env
    this.script = script
  }

  void name(name) {
    this.name = name
  }

  void registry(name) {
    this.registry = name
  }

  void stages(Closure closure) {
    this.stages = new StageConfig(this.script)
    ContextHelper.executeInContext(closure, this.stages)
  }

  String tag() {
    def tag = "${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
    return "${registry}/${name}:${tag}"
  }
}
