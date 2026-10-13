pipeline {
    agent any
    options {
        disableConcurrentBuilds()
        timeout(time: 10, unit: 'MINUTES')
    }
    stages {
        stage('Build') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                sh '''
                    python3 --version
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    if .venv/bin/python -m unittest discover -s . -p test_app.py -v > unit-test-output.txt 2>&1; then
                        cat unit-test-output.txt
                    else
                        cat unit-test-output.txt
                        exit 1
                    fi
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Copying the application to the mock deployment directory...'
                sh '''
                    mkdir -p python-app-deploy
                    cp app.py requirements.txt python-app-deploy/
                    cmp app.py python-app-deploy/app.py
                    cmp requirements.txt python-app-deploy/requirements.txt
                    ls -l python-app-deploy
                '''
            }
        }
        stage('Run Application') {
            steps {
                sh '.venv/bin/python application_check.py start'
            }
        }
        stage('Test Application') {
            steps {
                sh '.venv/bin/python application_check.py test'
            }
        }
    }
    post {
        always {
            script {
                sh returnStatus: true, script: '''
                    if [ -x .venv/bin/python ]; then
                        .venv/bin/python application_check.py stop
                    fi
                '''
            }
            archiveArtifacts artifacts: 'unit-test-output.txt,http-test-output.txt,python-app-deploy/app.py,python-app-deploy/requirements.txt,python-app-deploy/app.log', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for more details.'
        }
    }
}
