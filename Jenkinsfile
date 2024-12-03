pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp:latest'
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml'
        GKE_DEPLOYMENT_FILE = 'gke-deployment.yaml'
        KUBECTL_PATH = './kubectl' // Install kubectl in the workspace
    }
    stages {
        stage('Install kubectl') {
            steps {
                script {
                    echo "Installing kubectl..."
                    sh '''
                        curl -LO "https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubectl"
                        chmod +x kubectl
                        mv kubectl ${KUBECTL_PATH}
                    '''
                    sh '${KUBECTL_PATH} version --client'
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
