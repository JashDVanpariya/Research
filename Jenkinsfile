pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sledgy/webapp:latest'
        EKS_CLUSTER_NAME = 'eks-cluster'
        GKE_CLUSTER_NAME = 'gke-cluster'
        AWS_REGION = 'eu-west-1'
        GCP_PROJECT_ID = 'gold-circlet-439215-k9'
        GCP_ZONE = 'europe-west1-b'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    def buildStart = System.currentTimeMillis()
                    
                    // Skipping actual Docker build since the image is pre-built
                    echo "Skipping build as we're using pre-built Docker image: $DOCKER_IMAGE"
                    
                    def buildEnd = System.currentTimeMillis()
                    def buildDuration = (buildEnd - buildStart) / 1000
                    echo "Build Time: ${buildDuration} seconds"
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    def deployStart = System.currentTimeMillis()
                    
                    // Configure kubectl for EKS and deploy
                    sh """
                        aws eks update-kubeconfig --region $AWS_REGION --name $EKS_CLUSTER_NAME
                        kubectl apply -f eks-deployment.yaml
                    """
                    
                    def deployEnd = System.currentTimeMillis()
                    def deployDuration = (deployEnd - deployStart) / 1000
                    echo "EKS Deployment Time: ${deployDuration} seconds"
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                script {
                    def deployStart = System.currentTimeMillis()
                    
                    // Configure kubectl for GKE and deploy
                    sh """
                        gcloud container clusters get-credentials $GKE_CLUSTER_NAME --zone $GCP_ZONE --project $GCP_PROJECT_ID
                        kubectl apply -f gke-deployment.yaml
                       
                    """
                    
                    def deployEnd = System.currentTimeMillis()
                    def deployDuration = (deployEnd - deployStart) / 1000
                    echo "GKE Deployment Time: ${deployDuration} seconds"
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
