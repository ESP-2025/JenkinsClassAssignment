// Jenkinsfile (Windows)
pipeline {
  agent { label 'windows' }
  environment { PYTHONPATH = 'src' }
  options { timestamps() }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup Python') {
      steps {
        bat '''
          setlocal enabledelayedexpansion
          py -3 -m venv .venv || python -m venv .venv
          call .venv\\Scripts\\activate
          python -m pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Test') {
      steps {
        bat '''
          call .venv\\Scripts\\activate
          if not exist test-results mkdir test-results
          pytest -q --junitxml=test-results\\pytest.xml
        '''
      }
      post {
        always {
          junit 'test-results\\*.xml'
        }
      }
    }

    stage('Package artifact') {
      steps {
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

  post {
    always { echo 'Pipeline finished.' }
  }
}
