service {
  name('market-data')
  registry('morganjbruce')

  stages {
    build()
    test(command: 'py.test --junitxml results.xml', results: 'results.xml')
    publish()
    deploy()
  }
}
