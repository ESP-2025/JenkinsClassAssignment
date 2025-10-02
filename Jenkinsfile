pipeline {
    agent any
    stages {
        stage('No-op') {
            steps {
                sh 'lsa'
            }
        }
    }
    post {
        always {
            echo 'One way or another, I have finished'
            deleteDir() /* clean up our workspace */
        }
        success {
            echo 'I succeeded!'
        }
        unstable {
            echo 'I am unstable :/'
        }
        failure {
        mail to: 'akshatamadavi@gmail.com',
             subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
             body: "Something is wrong with ${env.BUILD_URL}"
    }
        changed {
            echo 'Things were different before...'
        }
    }
}