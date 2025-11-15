pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'
        IMAGE_NAME = 'docker26ak/flask-ecommerce'
        KUBECONFIG_PATH = '/var/lib/jenkins/.kube/config'
        MINIKUBE_IP = '192.168.49.2'   // <-- replace with your Minikube IP
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checkout from GitHub..."
                 git branch: 'main', url: 'https://github.com/Akashgithub90/proj.git'
            }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "Building Docker image..."
                docker build -t $IMAGE_NAME:$BUILD_NUMBER .
                docker images | grep flask-ecommerce
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKERHUB_CREDENTIALS,
                                                  usernameVariable: 'DOCKER_USER',
                                                  passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo "Logging in to Docker Hub..."
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push $IMAGE_NAME:$BUILD_NUMBER
                    docker logout
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                echo "Using kubeconfig..."
                export KUBECONFIG=/var/lib/jenkins/.kube/config}

                echo "Updating image in deployment file..."
                sed -i "s|image: .*|image: ${IMAGE_NAME}:${BUILD_NUMBER}|g" deployment.yaml

                echo "Applying Kubernetes YAML..."
                kubectl apply -f deployment.yaml --validate=false --insecure-skip-tls-verify

                echo "Waiting for rollout..."
                kubectl rollout status deployment/flask-app --timeout=90s

                echo "Application URL: http://${MINIKUBE_IP}:30007"
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed! Check logs."
        }
    }
}}
