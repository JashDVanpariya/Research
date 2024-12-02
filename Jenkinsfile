pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp'
        GKE_CONTEXT = 'gke_gold-circlet-439215-k9_europe-west1-b_gke-cluster'
        EKS_CONTEXT = 'arn:aws:eks:eu-west-1:920373010296:cluster/aws-cluster'
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml'
        GKE_DEPLOYMENT_FILE = 'gke-deployment.yaml'
        GKE_DEPLOYMENT_NAME = 'my-app'
        EKS_DEPLOYMENT_NAME = 'webapp'
    }
    stages {
        stage('Checkout')          
            steps {
                git branch: 'main', url: 'https://github.com/JashDVanpariya/Research.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    def startTime = System.currentTimeMillis()
                    echo "Building Docker image..."
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}", '.')
                    def endTime = System.currentTimeMillis()
                    def duration = (endTime - startTime) / 1000
                    echo "Docker image build time: ${duration} seconds"
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-creds') {
                        docker.image("${DOCKER_IMAGE}:${env.BUILD_NUMBER}").push()
                        docker.image("${DOCKER_IMAGE}:${env.BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                script {
                    def startTime = System.currentTimeMillis()
                    echo "Deploying to EKS..."
                    sh """
                    # Replace image in the EKS deployment file
                    sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}:${env.BUILD_NUMBER}|g' ${EKS_DEPLOYMENT_FILE}
                    
                    # Use EKS context and apply the deployment
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
                    # Replace image in the GKE deployment file
                    sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}:${env.BUILD_NUMBER}|g' ${GKE_DEPLOYMENT_FILE}
                    
                    # Use GKE context and apply the deployment
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
            echo "Pipeline completed successfully!"
        }
    }                  

