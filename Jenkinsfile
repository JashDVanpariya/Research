pipeline {
    agent any
    environment {
        GKE_CONTEXT = 'gke-cluster'
        EKS_CONTEXT = 'eks-cluster'
        GKE_DEPLOYMENT_NAME = 'my-app'
        EKS_DEPLOYMENT_NAME = 'webapp'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/JashDVanpariya/Research.git'
                echo "Code checked out successfully."
            }
        }
        stage('Build Application') {
            steps {
                script {
                    echo "Simulating application build..."
                    sh '''
                    echo "Building application..."
                    sleep 15 # Simulates a 15-second build time
                    echo "Build completed."
                    '''
                }
            }
        }
        stage('Deploy to GKE') {
            steps {
                script {
                    echo "Simulating deployment to GKE..."
                    sh '''
                    echo "Deploying to GKE cluster: ${GKE_CONTEXT}"
                    sleep 10 # Simulates a 10-second deploy time
                    echo "Deployment to GKE completed."
                    '''
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                script {
                    echo "Simulating deployment to EKS..."
                    sh '''
                    echo "Deploying to EKS cluster: ${EKS_CONTEXT}"
                    sleep 12 # Simulates a 12-second deploy time
                    echo "Deployment to EKS completed."
                    '''
                }
            }
        }
        stage('Report Success') {
            steps {
                echo "Pipeline automation completed successfully!"
            }
        }
    }
    post {
        always {
            echo "Pipeline completed."
        }
    }
}
