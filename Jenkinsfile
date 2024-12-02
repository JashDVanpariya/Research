pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp'
        IMAGE_TAG = 'latest'  // Specify the prebuilt image tag
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
                mv kubectl /usr/local/bin/
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
                    sh """
                    # Replace image in the EKS deployment file
                    sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|g' ${EKS_DEPLOYMENT_FILE}
                    
                    # Use EKS context and apply the deployment
                    kubectl config use-context ${EKS_CONTEXT}
                    kubectl apply -f ${EKS_DEPLOYMENT_FILE}
                    kubectl rollout status deployment/${EKS_DEPLOYMENT_NAME}
                    """
                }
            }
        }
        stage('Deploy to GKE') {
            steps {
                script {
                    echo "Deploying prebuilt image to GKE..."
                    sh """
                    # Replace image in the GKE deployment file
                    sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|g' ${GKE_DEPLOYMENT_FILE}
                    
                    # Use GKE context and apply the deployment
                    kubectl config use-context ${GKE_CONTEXT}
                    kubectl apply -f ${GKE_DEPLOYMENT_FILE}
                    kubectl rollout status deployment/${GKE_DEPLOYMENT_NAME}
                    """
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline completed successfully!"
        }
    }
}
