pipeline {
  agent any
  options { timestamps() }

  stages {
    stage('Test') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              set -eux
              (command -v python3 >/dev/null && python3 -m venv .venv) || python -m venv .venv
              . .venv/bin/activate
              pip install --upgrade pip
              if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
              mkdir -p test-results
              pytest test/test_hello.py
            '''
          } else {
            bat '''
              setlocal enabledelayedexpansion
              py -3 -m venv .venv || python -m venv .venv
              call .venv\\Scripts\\activate
              python -m pip install --upgrade pip
              if exist requirements.txt pip install -r requirements.txt
              if not exist test-results mkdir test-results
              pytest test/test_hello.py
            '''
          }
        }
      }
    }
  }

}