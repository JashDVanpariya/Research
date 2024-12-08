pipeline {
    agent any

    environment {
        AWS_REGION = 'eu-west-1'
        EKS_CLUSTER_NAME = 'eks-cluster'
        DOCKER_IMAGE = 'sledgy/webapp:latest'
        KUBECONFIG_PATH = '/root/.kube/config'  // Update path if needed
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/JashDVanpariya/Research.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                script {
                    sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    sh "aws eks update-kubeconfig --region $AWS_REGION --name $EKS_CLUSTER_NAME --kubeconfig $KUBECONFIG_PATH"
                    sh "kubectl apply -f k8s/eks-deployment.yaml --kubeconfig $KUBECONFIG_PATH"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
