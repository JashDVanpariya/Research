pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp:latest' // Docker Hub image
        EKS_CONTEXT = 'arn:aws:eks:eu-west-1:920373010296:cluster/eks-cluster' // EKS cluster context
        GKE_CONTEXT = 'gke_gold-circlet-439215-k9_europe-west1-b_gke-cluster' // GKE cluster context
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml' // EKS deployment file
        GKE_DEPLOYMENT_FILE = 'gke-deployment.yaml' // GKE deployment file
    }
    triggers {
        pollSCM('* * * * *') // Check for changes every minute
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
        stage('Deploy to EKS') {
            steps {
                script {
                    echo "Deploying to EKS..."
                    sh '''
                    kubectl config use-context ${EKS_CONTEXT}
                    kubectl apply -f ${EKS_DEPLOYMENT_FILE}
                    kubectl rollout status deployment/webapp --timeout=60s || kubectl describe deployment/webapp
                    '''
                }
            }
        }
        stage('Deploy to GKE') {
            steps {
                script {
                    echo "Deploying to GKE..."
                    sh '''
                    kubectl config use-context ${GKE_CONTEXT}
                    kubectl apply -f ${GKE_DEPLOYMENT_FILE}
                    kubectl rollout status deployment/my-app --timeout=60s || kubectl describe deployment/my-app
                    '''
                }
            }
        }
        stage('End Timer and Calculate Time') {
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
