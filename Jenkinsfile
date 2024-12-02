pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp:latest' // Pre-built public Docker image
        GKE_CONTEXT = 'gke_gold-circlet-439215-k9_europe-west1-b_gke-cluster'
        EKS_CONTEXT = 'arn:aws:eks:eu-west-1:920373010296:cluster/aws-cluster'
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml'
        GKE_DEPLOYMENT_FILE = 'gke-deployment.yaml'
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/JashDVanpariya/Research.git'
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    def startTime = System.currentTimeMillis()
                    echo "Skipping Docker push because the image is public."
                    def endTime = System.currentTimeMillis()
                    def duration = (endTime - startTime) / 1000
                    echo "Docker image push time: ${duration} seconds (skipped)"
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                script {
                    def startTime = System.currentTimeMillis()
                    echo "Deploying to EKS..."
                    sh """
                    sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}|g' ${EKS_DEPLOYMENT_FILE}
                    kubectl config use-context ${EKS_CONTEXT}
                    kubectl apply -f ${EKS_DEPLOYMENT_FILE}
                    kubectl rollout status deployment/webapp
                    """
                    def endTime = System.currentTimeMillis()
                    def duration = (endTime - startTime) / 1000
                    echo "EKS deployment time: ${duration} seconds"
                }
            }
        }
        stage('Deploy to GKE') {
            steps {
                script {
                    def startTime = System.currentTimeMillis()
                    echo "Deploying to GKE..."
                    sh """
                    sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}|g' ${GKE_DEPLOYMENT_FILE}
                    kubectl config use-context ${GKE_CONTEXT}
                    kubectl apply -f ${GKE_DEPLOYMENT_FILE}
                    kubectl rollout status deployment/my-app
                    """
                    def endTime = System.currentTimeMillis()
                    def duration = (endTime - startTime) / 1000
                    echo "GKE deployment time: ${duration} seconds"
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline execution completed!"
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }
}
