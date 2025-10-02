pipeline {
  agent any

  options {
    timeout(time: 15, unit: 'MINUTES')           // whole pipeline guard
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        // Now this works, because Jenkins knows the repo
        checkout scm
      }
    }

    stage('Build') {
      steps {
        sh '''
          echo "=== Build stage ==="
          # put your build command here (e.g., mvn package, npm install)
        '''
      }
    }

    stage('Test') {
      steps {
        retry(2) {
          sh '''
            echo "=== Test stage ==="
            # put your test command here (e.g., mvn test, npm test)
          '''
        }
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'target/surefire-reports/*.xml'
        }
      }
    }

    stage('Deploy') {
      when { branch 'main' }  // only run on main branch
      steps {
        timeout(time: 5, unit: 'MINUTES') {
          sh '''
            echo "=== Deploy stage ==="
            # ./deploy.sh or kubectl apply -f ...
          '''
        }
      }
    }
  }

  post {
    always  { echo 'This runs no matter what' }
    success { echo 'Pipeline succeeded ✅' }
    failure { echo 'Pipeline failed ❌' }
  }
}
