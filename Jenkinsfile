// Jenkinsfile (Unix)
pipeline {
  agent any
  environment { PYTHONPATH = 'src' }   // so tests can import from src
  options { timestamps() }

  stages {
    stage('Checkout') {
      steps { checkout scm }   // works when job is "Pipeline from SCM" or Multibranch
    }

    stage('Setup Python') {
      steps {
        sh '''
          set -eux
          PY=python3; command -v python3 >/dev/null 2>&1 || PY=python
          $PY -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Test') {
      steps {
        sh '''
          set -eux
          . .venv/bin/activate
          mkdir -p test-results
          pytest -q --junitxml=test-results/pytest.xml
        '''
      }
      post {
        always {
          junit 'test-results/*.xml'   // shows up in Jenkins "Test Result" & trend
        }
      }
    }

    stage('Package artifact') {
      steps {
        sh '''
          set -eux
          . .venv/bin/activate
          mkdir -p dist
          python - <<'PY'
from pathlib import Path
Path("dist").mkdir(exist_ok=True)
Path("dist/app-output.txt").write_text("built by Jenkins")
PY
          tar -czf dist/example-artifact.tgz -C dist app-output.txt
        '''
        archiveArtifacts artifacts: 'dist/**', fingerprint: true
      }
    }
  }

  post {
    always { echo 'Pipeline finished.' }
  }
}
