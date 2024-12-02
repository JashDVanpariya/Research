pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp'
        IMAGE_TAG = 'latest'
        GKE_CONTEXT = 'gke-cluster'
        EKS_CONTEXT = 'eks-cluster'
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml'
        GKE_DEPLOYMENT_FILE = 'gke-deployment.yaml'
        GKE_DEPLOYMENT_NAME = 'my-app'
        EKS_DEPLOYMENT_NAME = 'webapp'
        PATH = "${env.HOME}/bin:${env.PATH}"
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
                mkdir -p $HOME/bin
                mv kubectl $HOME/bin/
                echo $PATH
                kubectl version --client
                '''
            }
        }
        stage('Authenticate with GKE') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'gcp-credentials', variable: 'GKE_KEY')]) {
                        sh '''
                        echo "Authenticating with GKE..."
                        gcloud auth activate-service-account --key-file=$GKE_KEY
                        gcloud container clusters get-credentials ${GKE_CONTEXT} --zone=europe-west1-b --project=gold-circlet-439215
                        '''
                    }
                }
            }
        }
        stage('Authenticate with EKS') {
            steps {
                withCredentials([string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY'),
                                 string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_KEY')]) {
                    sh '''
                    echo "Authenticating with EKS..."
                    export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY
                    export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_KEY
                    aws eks update-kubeconfig --region eu-west-1 --name aws-cluster
                    '''
                }
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
                    sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|g' ${EKS_DEPLOYMENT_FILE}
                    kubectl config use-context ${EKS_CONTEXT}
                    kubectl apply -f ${EKS_DEPLOYMENT_FILE}
                    kubectl rollout status deployment/${EKS_DEPLOYMENT_NAME} || kubectl describe deployment/${EKS_DEPLOYMENT_NAME}
                    """
                }
            }
        }
        stage('Deploy to GKE') {
            steps {
                script {
                    echo "Deploying prebuilt image to GKE..."
                    sh """
                    sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|g' ${GKE_DEPLOYMENT_FILE}
                    kubectl config use-context ${GKE_CONTEXT}
                    kubectl apply -f ${GKE_DEPLOYMENT_FILE}
                    kubectl rollout status deployment/${GKE_DEPLOYMENT_NAME} || kubectl describe deployment/${GKE_DEPLOYMENT_NAME}
                    """
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline completed!"
        }
        failure {
            echo "Pipeline failed!"
        }        
    }
}
     