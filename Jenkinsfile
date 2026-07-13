pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')   // set up in Jenkins > Credentials
        IMAGE_NAME  = "eshwarapragadasaianurath7779/devops-demo-app"
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        DEPLOY_HOST = "3.94.132.134"                   // EC2 / cloud VM public IP
    }

    stages {

        stage('Checkout') {
            steps {
                // Pulls the latest code from GitHub (triggered by webhook on push)
                git branch: 'main', url: 'https://github.com/ESaiAnurath/devops_CICD_pipeline_flask.git'
            }
        }

       /* stage('Install Dependencies') {
            steps {
                dir('app') {
                    sh 'pip install -r requirements.txt'
                }
            }
        } */

       /* stage('Run Tests') {
            steps {
                dir('app') {
                    // Pipeline stops here automatically if any test fails
                    sh 'pytest --junitxml=test-results.xml'
                }
            }
            post {
                always {
                    junit 'app/test-results.xml'
                }
            }
        }*/

        stage('Build Docker Image') {
            steps {
                dir('app') {
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

       stage('Deploy') {
            steps {
                // SSH into the deploy server and restart the container with the new image
                sshagent(['deploy-server-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@${DEPLOY_HOST} '
                           sudo  docker pull ${IMAGE_NAME}:latest &&
                           sudo docker stop devops-demo-app || true &&
                            sudo docker rm devops-demo-app || true &&
                            sudo docker run -d --name devops-demo-app -p 5000:5000 ${IMAGE_NAME}:latest
                        '
                    """
                }
            }
        }
    }
      /*  stage('Deploy') {
    steps {
        sshagent(['deploy-server-ssh-key']) {
            sh """
                ssh -o StrictHostKeyChecking=no ubuntu@${DEPLOY_HOST} "
                    hostname
                    docker --version
                "
            """
        }
    }*/

    /*    stage('Deploy') {
    steps {
        echo "Docker image successfully pushed to DockerHub."
        echo "Deployment stage skipped for demo project."
    }
}
    }*/

    post {
        success {
            echo "Pipeline succeeded! Build #${env.BUILD_NUMBER} deployed."
        }
        failure {
            echo "Pipeline failed. Check the logs above."
        }
        always {
            sh "docker logout || true"  // Logout from DockerHub to clean up credentials
        }
    }
}
