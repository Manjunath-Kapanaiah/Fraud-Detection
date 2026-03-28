pipeline {
    agent { label 'K8s' }   // match your label EXACTLY

    environment {
        PIP_CACHE_DIR = "${WORKSPACE}/.pip-cache"
    }

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --cache-dir="$PIP_CACHE_DIR" -r requirements.txt
                '''
            }
        }

        stage('Parallel Tests') {
            parallel {

                stage('Unit Tests') {
                    steps {
                        sh '''
                        . venv/bin/activate
                        pytest test_unit.py
                        '''
                    }
                }

                stage('Integration Tests') {
                    steps {
                        sh '''
                        . venv/bin/activate
                        pytest test_integration.py
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                kubectl apply -f deployment.yaml
                '''
            }
        }
    }

    post {
        failure {
            echo "Rolling back deployment..."
            sh '''
            kubectl rollout undo deployment/fraud-app
            '''
        }
    }
}
