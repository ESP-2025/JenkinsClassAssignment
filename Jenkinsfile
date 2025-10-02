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
        echo "Starting test stage"
        timeout(time: 5, unit: 'MINUTES') {
          retry(2) {
            script {
              echo "Attempt to run tests"
              sh '''
                echo "=== Tests ==="
                echo "Running tests with RUN_SLOW_TESTS=${RUN_SLOW_TESTS}"
                mkdir -p test-results
                cat > test-results/sample.xml <<EOF
                <testsuite tests="1"><testcase classname="demo" name="ok"/></testsuite>
                EOF
              '''
            }
          }
        }
      }
      post {
        always {
          echo "Processing test results"
          junit allowEmptyResults: true, testResults: 'test-results/*.xml'
        }
      }
    }

    stage('Use credentials safely') {
      steps {
        // 1) Create a secret/text credential in Jenkins (e.g., ID: GITHUB_TOKEN)
        // 2) Jenkins will expose it as an env var only inside this block and mask it in logs
        withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GH_TOKEN')]) {
          sh '''
            echo "=== Using a token safely ==="
            # value is available as $GH_TOKEN (masked in logs)
            test -n "$GH_TOKEN" && echo "Token is set (masked)"
            # Example: curl -H "Authorization: Bearer $GH_TOKEN" https://api.github.com/user
          '''
        }
      }
    }

    stage('Deploy') {
      when { branch 'main' }
      environment {
        // compute from parameter; keeps deploy config in env
        TARGET_ENV = "${params.DEPLOY_ENV}"
      }
      steps {
        timeout(time: 5, unit: 'MINUTES') {
          retry(3) {
            sh '''
              echo "=== Deploy ==="
              echo "Deploying to $TARGET_ENV (APP_ENV=$APP_ENV)"
              # ./scripts/deploy.sh "$TARGET_ENV"
            '''
          }
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
