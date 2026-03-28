pipeline {
    agent { label 'K8s' }

    environment {
        PIP_CACHE_DIR = "${WORKSPACE}/.pip-cache"
    }

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                mkdir -p "$PIP_CACHE_DIR"
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
                kubectl apply -f deployment.yaml || echo "Skipping deploy"
                '''
            }
        }
    }

    post {
        failure {
            echo "Safe rollback..."

            sh '''
            kubectl get nodes || exit 0
            kubectl rollout undo deployment/fraud-app || true
            '''
        }
    }
}
