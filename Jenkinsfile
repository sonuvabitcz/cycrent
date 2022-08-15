pipeline {
    agent any

    stages {
        stage('Run docker-compose') {
            steps {
                echo 'Building stage'
				sh "docker-compose up -d docker-compose.prod.yml"
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
