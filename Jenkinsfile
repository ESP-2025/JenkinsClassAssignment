pipeline {
  agent any

  options {
    timeout(time: 20, unit: 'MINUTES')
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timestamps()
  }

  // Global environment (available everywhere)
  environment {
    APP_ENV        = 'dev'
    DB_ENGINE      = 'sqlite'
    DISABLE_AUTH   = 'true'
  }

  // Optional job parameters (show up in “Build with Parameters”)
  parameters {
    string(name: 'DEPLOY_ENV', defaultValue: 'staging', description: 'Where to deploy?')
    booleanParam(name: 'RUN_SLOW_TESTS', defaultValue: false, description: 'Include slow tests')
  }

  stages {
    stage('Checkout') {
      steps {
        // Works since you’re using Pipeline from SCM/Multibranch
        checkout scm
        echo "Branch: ${env.BRANCH_NAME}, Build: #${env.BUILD_NUMBER}"
      }
    }

    stage('Build (uses globals)') {
      steps {
        sh '''
          set -e
          echo "=== Build ==="
          echo "Building for APP_ENV=$APP_ENV DB_ENGINE=$DB_ENGINE DISABLE_AUTH=$DISABLE_AUTH"
          # e.g., mvn -B -DskipTests package  OR  npm ci && npm run build
          echo "hello-build" > build.txt
        '''
        archiveArtifacts artifacts: 'build.txt', fingerprint: true
      }
    }

    stage('Stage-specific env') {
      environment {
        // Only visible inside this stage; overrides global if same key
        DB_ENGINE = 'postgres'
      }
      steps {
        sh 'echo "DB_ENGINE in this stage is $DB_ENGINE (overridden here)"'
      }
    }

    stage('Tests with retry/timeout') {
      steps {
        timeout(time: 5, unit: 'MINUTES') {
          retry(2) {
            sh '''
              echo "=== Tests ==="
              echo "RUN_SLOW_TESTS is: '"$RUN_SLOW_TESTS"'"
              mkdir -p test-results
              cat > test-results/sample.xml <<EOF
              <testsuite tests="1"><testcase classname="demo" name="ok"/></testsuite>
              EOF
            '''
          }
        }
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'test-results/*.xml'
        }
      }
    }

    

  }

  post {
    always  { echo 'Always runs (cleanup/notifications)' }
    success { echo 'Pipeline Succeeded 🎉' }
    failure { echo 'Pipeline Failed ❌' }
    unstable{ echo 'Pipeline Unstable ⚠️' }
    changed { echo "Result changed since last run: ${currentBuild.currentResult}" }
  }
}
