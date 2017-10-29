package build

class ContextHelper {
  private ContextHelper() {}

  static void executeInContext(Closure closure, freshContext) {
    if (closure) {
      closure.delegate = freshContext
      closure.resolveStrategy = Closure.DELEGATE_FIRST
      closure.call()
    }
  }
}
