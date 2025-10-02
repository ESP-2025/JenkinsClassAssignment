pipeline {
  agent any

  stages {
    stage('Prep') {
      steps {
        echo 'Prep running'
      }
    }
    stage('Build') {
      steps {
        echo 'Build running'
      }
    }
    stage('Test') {
      steps {
        echo 'Test running'
      }
    }
  }

  post {
    always { echo 'Done' }
  }
}
