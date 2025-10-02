pipeline {
  agent any
  environment { PYTHONPATH = 'src' }
  options { timestamps() }

  stages {
    stage('Node info') {
      steps { echo "Node: ${env.NODE_NAME} | isUnix=${isUnix()}" }
    }

    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup Python') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              set -eux
              (command -v python3 >/dev/null && python3 -m venv .venv) || python -m venv .venv
              . .venv/bin/activate
              python --version
              pip install --upgrade pip
              pip install -r requirements.txt
            '''
          } else {
            bat '''
              setlocal enabledelayedexpansion
              py -3 -m venv .venv || python -m venv .venv
              call .venv\\Scripts\\activate
              python --version
              python -m pip install --upgrade pip
              pip install -r requirements.txt
            '''
          }
        }
      }
    }

    stage('Test') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              . .venv/bin/activate
              mkdir -p test-results
              pytest -q --junitxml=test-results/pytest.xml
            '''
          } else {
            bat '''
              call .venv\\Scripts\\activate
              if not exist test-results mkdir test-results
              pytest -q --junitxml=test-results\\pytest.xml
            '''
          }
        }
      }
      post {
        always { junit 'test-results/*.xml' }
      }
    }

    stage('Package artifact') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              . .venv/bin/activate
              mkdir -p dist
              echo "built by Jenkins" > dist/app-output.txt
              tar -czf dist/example-artifact.tgz -C dist app-output.txt
            '''
            archiveArtifacts artifacts: 'dist/**', fingerprint: true
          } else {
            bat '''
              call .venv\\Scripts\\activate
              if not exist dist mkdir dist
              > dist\\app-output.txt echo built by Jenkins
              powershell -Command "Compress-Archive -Path dist\\app-output.txt -DestinationPath dist\\example-artifact.zip -Force"
            '''
            archiveArtifacts artifacts: 'dist\\**\\*', fingerprint: true
          }
        }
      }
    }
  }

  post { always { echo 'Pipeline finished.' } }
}
