pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp:latest'
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml'
        GKE_DEPLOYMENT_FILE = 'gke-deployment.yaml'
        KUBECTL_PATH = './kubectl'
        AWS_CLI_PATH = './aws-cli/bin/aws'
    }
    stages {
        stage('Install Required Tools') {
            steps {
                script {
                    echo "Installing kubectl, GKE auth plugin, and AWS CLI..."
                    sh '''
                        # Install kubectl
                        curl -LO "https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubectl"
                        chmod +x kubectl

                        # Install GKE auth plugin
                        curl -LO https://storage.googleapis.com/artifacts.k8s.io/binaries/kubernetes-client-go-auth-gcp/release/latest/gke-gcloud-auth-plugin
                        chmod +x gke-gcloud-auth-plugin

                        # Install AWS CLI in a local directory
                        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
                        unzip -o awscliv2.zip
                        ./aws/install --install-dir ./aws-cli --bin-dir ./aws-cli/bin
                    '''

                    echo "Verifying AWS CLI installation..."
                    sh './aws-cli/bin/aws --version'
                }
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/JashDVanpariya/Research.git'
            }
        }

        stage('Deploy to EKS') {
            steps {
                withCredentials([[ 
                    $class: 'AmazonWebServicesCredentialsBinding', 
                    credentialsId: 'aws-credentials-id' // Replace with your credentialsId
                ]]) {
                    script {
                        echo "Configuring AWS CLI and Deploying to EKS..."
                        sh '''
                            # Configure AWS CLI to access EKS
                            ${AWS_CLI_PATH} eks update-kubeconfig --region your-region --name your-cluster-name

                            # Deploy application
                            sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}|g' ${EKS_DEPLOYMENT_FILE}
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
                            sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}|g' ${GKE_DEPLOYMENT_FILE}
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
