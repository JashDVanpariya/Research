pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp:latest'
        KUBECTL_PATH = './kubectl'
        GKE_AUTH_PLUGIN = './gke-gcloud-auth-plugin'
        AWS_REGION = 'us-west-2'
        EKS_CLUSTER_NAME = 'your-eks-cluster'
    }
    stages {
        stage('Install Required Tools') {
            steps {
                script {
                    echo "Installing required tools..."
                    sh '''
                        # Install kubectl
                        curl -LO "https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubectl"
                        chmod +x kubectl

                        # Install gke-gcloud-auth-plugin
                        curl -LO https://storage.googleapis.com/artifacts.k8s.io/binaries/kubernetes-client-go-auth-gcp/release/latest/gke-gcloud-auth-plugin
                        chmod +x gke-gcloud-auth-plugin

                        # Install gcloud SDK
                        curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-419.0.0-linux-x86_64.tar.gz
                        tar -xvf google-cloud-cli-419.0.0-linux-x86_64.tar.gz
                        ./google-cloud-sdk/install.sh --quiet

                        # Install AWS CLI
                        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                        unzip awscliv2.zip
                        ./aws/install
                    '''
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                script {
                    echo "Configuring AWS CLI..."
                    sh '''
                        aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME} --region ${AWS_REGION}
                        ./kubectl apply -f eks-deployment.yaml
                        ./kubectl rollout status deployment/webapp
                    '''
                }
            }
        }
        stage('Deploy to GKE') {
            steps {
                script {
                    echo "Deploying to GKE..."
                    sh '''
                        export PATH=$PATH:$(pwd)
                        ./kubectl apply -f gke-deployment.yaml
                        ./kubectl rollout status deployment/my-app
                    '''
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
