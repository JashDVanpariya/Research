pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp:latest'
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml'
        GKE_DEPLOYMENT_FILE = 'gke-deployment.yaml'
        KUBECTL_PATH = './kubectl' // Path to the locally installed kubectl
        GKE_AUTH_PLUGIN = './gke-gcloud-auth-plugin' // Path to the locally installed GKE Auth Plugin
    }
    stages {
        stage('Install kubectl') {
            steps {
                script {
                    echo "Installing kubectl..."
                    sh '''
                        curl -LO "https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubectl"
                        chmod +x kubectl
                    '''
                    sh '${KUBECTL_PATH} version --client'
                }
            }
        }
        stage('Install GKE Auth Plugin') {
            steps {
                script {
                    echo "Installing GKE Auth Plugin..."
                    sh '''
                        curl -LO https://storage.googleapis.com/artifacts.k8s.io/binaries/kubernetes-client-go-auth-gcp/release/latest/gke-gcloud-auth-plugin
                        chmod +x gke-gcloud-auth-plugin
                    '''
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
                withKubeConfig(credentialsId: 'eks-kubeconfig') {
                    script {
                        def startTime = System.currentTimeMillis()
                        echo "Deploying to EKS..."
                        sh '''
                        sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}|g' ${EKS_DEPLOYMENT_FILE}
                        ${KUBECTL_PATH} apply -f ${EKS_DEPLOYMENT_FILE}
                        ${KUBECTL_PATH} rollout status deployment/webapp
                        '''
                        def endTime = System.currentTimeMillis()
                        def duration = (endTime - startTime) / 1000
                        echo "EKS deployment time: ${duration} seconds"
                    }
                }
            }
        }
        stage('Deploy to GKE') {
            steps {
                withKubeConfig(credentialsId: 'gke-kubeconfig') {
                    script {
                        def startTime = System.currentTimeMillis()
                        echo "Deploying to GKE..."
                        sh '''
                        export PATH=$PATH:$(pwd) # Add local directory to PATH
                        sed -i 's|sledgy/webapp:latest|${DOCKER_IMAGE}|g' ${GKE_DEPLOYMENT_FILE}
                        ${KUBECTL_PATH} apply -f ${GKE_DEPLOYMENT_FILE}
                        ${KUBECTL_PATH} rollout status deployment/my-app
                        '''
                        def endTime = System.currentTimeMillis()
                        def duration = (endTime - startTime) / 1000
                        echo "GKE deployment time: ${duration} seconds"
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
