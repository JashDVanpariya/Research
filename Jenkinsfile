pipeline {
    agent any
    environment {
        PATH = "/var/jenkins_home/bin:${env.PATH}"
        DOCKER_IMAGE = 'sledgy/webapp'
        IMAGE_TAG = 'latest'
        GKE_CONTEXT = 'gke_gold-circlet-439215-k9_europe-west1-b_gke-cluster'
        EKS_CONTEXT = 'arn:aws:eks:eu-west-1:920373010296:cluster/aws-cluster'
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml'
        GKE_DEPLOYMENT_FILE = 'gke-deployment.yaml'
        GKE_DEPLOYMENT_NAME = 'my-app'
        EKS_DEPLOYMENT_NAME = 'webapp'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/JashDVanpariya/Research.git'
            }
        }
        stage('Install kubectl') {
            steps {
                sh '''
                echo "Installing kubectl..."
                curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                chmod +x kubectl
                mkdir -p /var/jenkins_home/bin
                mv kubectl /var/jenkins_home/bin/
                export PATH=/var/jenkins_home/bin:$PATH
                echo $PATH
                kubectl version --client
                '''
            }
        }
        stage('Test kubectl') {
            steps {
                sh '''
                export PATH=/var/jenkins_home/bin:$PATH
                echo "Verifying kubectl installation..."
                which kubectl
                kubectl version --client
                '''
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    echo "Skipping Docker build. Using prebuilt image: ${DOCKER_IMAGE}:${IMAGE_TAG}."
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                script {
                    echo "Deploying prebuilt image to EKS..."
                    sh '''
                    export PATH=/var/jenkins_home/bin:$PATH
                    sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|g' ${EKS_DEPLOYMENT_FILE}
                    kubectl config use-context ${EKS_CONTEXT}
                    kubectl apply -f ${EKS_DEPLOYMENT_FILE}
                    kubectl rollout status deployment/${EKS_DEPLOYMENT_NAME}
                    '''
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline completed!"
        }
    }
}
