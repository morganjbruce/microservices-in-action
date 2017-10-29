import build.*

def call(Closure closure) {
  def config = new ServiceConfig(this, env)
  ContextHelper.executeInContext(closure, config)

  new ServiceRunner().run(config)
}
