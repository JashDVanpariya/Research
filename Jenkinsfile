pipeline {
    agent any
    environment {
        // Docker image from Docker Hub
        DOCKER_IMAGE = 'sledgy/webapp:latest'
        
        // Kubernetes contexts as defined in kubeconfig
        EKS_CONTEXT = 'arn:aws:eks:eu-west-1:920373010296:cluster/eks-cluster'
        GKE_CONTEXT = 'gke_gold-circlet-439215-k9_europe-west1-b_gke-cluster'
        
        // Deployment YAML files
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml'
        GKE_DEPLOYMENT_FILE = 'gke-deployment.yaml'
    }
    triggers {
        pollSCM('* * * * *') // Poll SCM every minute
    }
    stages {
        stage('Start Timer') {
            steps {
                script {
                    env.START_TIME = System.currentTimeMillis()
                }
            }
        }
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Install AWS CLI and kubectl') {
            steps {
                sh '''
                    echo "Installing AWS CLI..."
                    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                    unzip -o awscliv2.zip
                    ./aws/install --install-dir=$HOME/aws-cli --binary-dir=$HOME/bin
                    export PATH=$HOME/bin:$PATH
                    aws --version

                    echo "Installing kubectl..."
                    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    chmod +x kubectl
                    mv kubectl $HOME/bin/
                    export PATH=$HOME/bin:$PATH
                    kubectl version --client
                '''
            }
        }
        stage('Setup Kubeconfig and AWS Credentials') {
            steps {
                withCredentials([
                    file(credentialsId: 'MY_KUBECONFIG_FILE', variable: 'KUBECONFIG_FILE'),
                    usernamePassword(credentialsId: 'AWS_CREDENTIALS', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        # Configure AWS CLI with credentials
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                        aws configure set default.region eu-west-1

                        # Copy kubeconfig to workspace
                        cp $KUBECONFIG_FILE kubeconfig

                        # Verify kubeconfig
                        kubectl --kubeconfig=kubeconfig config get-contexts
                    '''
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                script {
                    echo "Deploying to EKS..."
                    sh '''
                        START_DEPLOY_EKS=$(date +%s)
                        
                        # Switch to EKS context
                        kubectl --kubeconfig=kubeconfig config use-context ${EKS_CONTEXT}
                        
                        # Update the deployment with the new image
                        kubectl --kubeconfig=kubeconfig set image deployment/webapp webapp=${DOCKER_IMAGE} --record
                        
                        # Monitor the rollout status
                        kubectl --kubeconfig=kubeconfig rollout status deployment/webapp --timeout=60s || kubectl --kubeconfig=kubeconfig describe deployment/webapp
                        
                        END_DEPLOY_EKS=$(date +%s)
                        echo "EKS Deployment Time: $((END_DEPLOY_EKS - START_DEPLOY_EKS)) seconds"
                    '''
                }
            }
        }
        stage('Deploy to GKE') {
            steps {
                script {
                    echo "Deploying to GKE..."
                    sh '''
                        START_DEPLOY_GKE=$(date +%s)
                        
                        # Switch to GKE context
                        kubectl --kubeconfig=kubeconfig config use-context ${GKE_CONTEXT}
                        
                        # Update the deployment with the new image
                        kubectl --kubeconfig=kubeconfig set image deployment/my-app my-app=${DOCKER_IMAGE} --record
                        
                        # Monitor the rollout status
                        kubectl --kubeconfig=kubeconfig rollout status deployment/my-app --timeout=60s || kubectl --kubeconfig=kubeconfig describe deployment/my-app
                        
                        END_DEPLOY_GKE=$(date +%s)
                        echo "GKE Deployment Time: $((END_DEPLOY_GKE - START_DEPLOY_GKE)) seconds"
                    '''
                }
            }
        }
        stage('End Timer and Calculate Total Time') {
            steps {
                script {
                    def END_TIME = System.currentTimeMillis()
                    def TOTAL_TIME = (END_TIME - START_TIME) / 1000
                    echo "Total Build and Deployment Time: ${TOTAL_TIME} seconds"
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline Completed!"
        }
    }
}
