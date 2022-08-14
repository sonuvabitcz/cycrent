pipeline {
    agent any

    stages {
        stage('Building') {
            steps {
                echo 'Building stage'
				sh "ls -lah"
            }
        }
        stage('Testing') {
            steps {
                echo 'Testing stage'
            }
        }
        stage('Deploying') {
            steps {
                echo 'Deploying stage'
            }
        }
    }
}
