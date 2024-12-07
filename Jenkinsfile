pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'sledgy/webapp:latest' // Docker Hub image
        EKS_CONTEXT = 'arn:aws:eks:eu-west-1:920373010296:cluster/eks-cluster' // EKS cluster context
        GKE_CONTEXT = 'gke_gold-circlet-439215-k9_europe-west1-b_gke-cluster' // GKE cluster context
        EKS_DEPLOYMENT_FILE = 'eks-deployment.yaml' // EKS deployment file
        GKE_DEPLOYMENT_FILE = 'gke-deployment.yaml' // GKE deployment file        
        PATH = "/var/jenkins_home/bin:${env.PATH}" // Add kubectl directory to global PATH
    }
    triggers {
        pollSCM('* * * * *') // Check for changes every minute
    }
    stages {
        stage('Install kubectl') {
            steps {
                sh '''
                echo "Installing kubectl..."
                curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                chmod +x kubectl
                mkdir -p /var/jenkins_home/bin
                mv kubectl /var/jenkins_home/bin/
                kubectl version --client
                '''
            }
        }
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
        stage('Setup Kubeconfig') {
            steps {
                withCredentials([file(credentialsId: 'KUBE_CONFIG', variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                      cp $KUBECONFIG_FILE kubeconfig
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
                    kubectl --kubeconfig=kubeconfig config use-context ${EKS_CONTEXT}
                    kubectl --kubeconfig=kubeconfig apply -f ${EKS_DEPLOYMENT_FILE}
                    kubectl --kubeconfig=kubeconfig rollout status deployment/webapp --timeout=60s || kubectl --kubeconfig=kubeconfig describe deployment/webapp
                    '''
                }
            }
        }
        stage('Deploy to GKE') {
            steps {
                script {
                    echo "Deploying to GKE..."
                    sh '''
                    kubectl --kubeconfig=kubeconfig config use-context ${GKE_CONTEXT}
                    kubectl --kubeconfig=kubeconfig apply -f ${GKE_DEPLOYMENT_FILE}
                    kubectl --kubeconfig=kubeconfig rollout status deployment/my-app --timeout=60s || kubectl --kubeconfig=kubeconfig describe deployment/my-app
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
