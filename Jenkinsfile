pipeline {
    agent { label 'K8s' }

    environment {
        PIP_CACHE_DIR = "${WORKSPACE}/.pip-cache"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/your-repo/fraud-detection.git'
            }
        }

        stage('Install Dependencies (with caching)') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --cache-dir $PIP_CACHE_DIR -r requirements.txt
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

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f deployment.yaml
                '''
            }
        }
    }

    post {
        failure {
            echo "Deployment failed! Rolling back..."

            sh '''
            kubectl rollout undo deployment/fraud-app
            '''
        }
    }
}
