pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp:latest'
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml'
        GKE_DEPLOYMENT_FILE = 'gke-deployment.yaml'
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/JashDVanpariya/Research.git'
            }
        }
        stage('Install Required Tools') {
            steps {
                script {
                    echo "Installing kubectl and other tools..."
                    sh '''
                        # Install kubectl
                        curl -LO "https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubectl"
                        chmod +x kubectl
                        
                        # Install gke-gcloud-auth-plugin
                        curl -LO https://storage.googleapis.com/artifacts.k8s.io/binaries/kubernetes-client-go-auth-gcp/release/latest/gke-gcloud-auth-plugin
                        chmod +x gke-gcloud-auth-plugin
                    '''
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                withKubeConfig(credentialsId: 'eks-kubeconfig') {
                    script {
                        echo "Deploying to EKS..."
                        sh '''
                        ./kubectl apply -f ${EKS_DEPLOYMENT_FILE}
                        ./kubectl rollout status deployment/webapp
                        '''
                    }
                }
            }
        }
        stage('Deploy to GKE') {
            steps {
                withKubeConfig(credentialsId: 'gke-kubeconfig') {
                    script {
                        echo "Deploying to GKE..."
                        sh '''
                        export PATH=$PATH:$(pwd) # Add local directory to PATH
                        ./kubectl apply -f ${GKE_DEPLOYMENT_FILE}
                        ./kubectl rollout status deployment/my-app
                        '''
                    }
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
