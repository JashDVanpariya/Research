pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp:latest'
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml'
        KUBECTL_PATH = '/usr/local/bin/kubectl' // Path where kubectl will be installed
    }
    stages {
        stage('Install kubectl') {
            steps {
                script {
                    echo "Installing kubectl..."
                    sh '''
                        curl -LO "https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubectl"
                        chmod +x kubectl
                        sudo mv kubectl /usr/local/bin/kubectl
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
