pipeline {
    agent any
    
    environment {
        // Docker and Git Configuration
        DOCKER_REGISTRY = 'your-dockerhub-username'
        DOCKER_IMAGE = 'your-app-name'
        GIT_REPO = 'your-git-repo-url'
        
        // EKS Cluster Configuration
        EKS_CLUSTER_NAME = 'your-eks-cluster-name'
        EKS_REGION = 'us-west-2'
        
        // GKE Cluster Configuration
        GKE_CLUSTER_NAME = 'your-gke-cluster-name'
        GKE_ZONE = 'us-central1-a'
        GKE_PROJECT = 'your-gcp-project-id'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    env.CHECKOUT_START = System.currentTimeMillis()
                }
                git branch: 'main', url: "${GIT_REPO}"
                script {
                    env.CHECKOUT_END = System.currentTimeMillis()
                    env.CHECKOUT_TIME = (env.CHECKOUT_END as long) - (env.CHECKOUT_START as long)
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    env.BUILD_START = System.currentTimeMillis()
                    dockerImage = docker.build("${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER}")
                    env.BUILD_END = System.currentTimeMillis()
                    env.BUILD_TIME = (env.BUILD_END as long) - (env.BUILD_START as long)
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    env.PUSH_START = System.currentTimeMillis()
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                    env.PUSH_END = System.currentTimeMillis()
                    env.PUSH_TIME = (env.PUSH_END as long) - (env.PUSH_START as long)
                }
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                script {
                    env.EKS_DEPLOY_START = System.currentTimeMillis()
                    withAWS(credentials: 'aws-credentials', region: "${EKS_REGION}") {
                        // Update EKS kubeconfig
                        sh "aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME} --region ${EKS_REGION}"
                        
                        // Deploy using EKS-specific deployment file
                        sh """
                            kubectl apply -f eks-deployment.yaml
                            kubectl set image deployment/your-eks-deployment ${DOCKER_IMAGE}=${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER}
                            kubectl rollout status deployment/your-eks-deployment
                        """
                    }
                    env.EKS_DEPLOY_END = System.currentTimeMillis()
                    env.EKS_DEPLOY_TIME = (env.EKS_DEPLOY_END as long) - (env.EKS_DEPLOY_START as long)
                }
            }
        }
        
        stage('Deploy to GKE') {
            steps {
                script {
                    env.GKE_DEPLOY_START = System.currentTimeMillis()
                    withCredentials([file(credentialsId: 'gke-credentials', variable: 'GKE_KEYFILE')]) {
                        // Authenticate with GKE
                        sh """
                            gcloud auth activate-service-account --key-file=${GKE_KEYFILE}
                            gcloud config set project ${GKE_PROJECT}
                            gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --zone ${GKE_ZONE}
                        """
                        
                        // Deploy using GKE-specific deployment file
                        sh """
                            kubectl apply -f gke-deployment.yaml
                            kubectl set image deployment/your-gke-deployment ${DOCKER_IMAGE}=${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER}
                            kubectl rollout status deployment/your-gke-deployment
                        """
                    }
                    env.GKE_DEPLOY_END = System.currentTimeMillis()
                    env.GKE_DEPLOY_TIME = (env.GKE_DEPLOY_END as long) - (env.GKE_DEPLOY_START as long)
                }
            }
        }
    }
    
    post {
        success {
            script {
                // Calculate total pipeline time
                env.TOTAL_PIPELINE_TIME = (System.currentTimeMillis() - env.PIPELINE_START)
                
                // Print out detailed timing information
                echo """
                ========== Pipeline Timing Report ==========
                Checkout Time:         ${env.CHECKOUT_TIME} ms
                Build Time:            ${env.BUILD_TIME} ms
                Docker Push Time:      ${env.PUSH_TIME} ms
                EKS Deployment Time:   ${env.EKS_DEPLOY_TIME} ms
                GKE Deployment Time:   ${env.GKE_DEPLOY_TIME} ms
                Total Pipeline Time:   ${env.TOTAL_PIPELINE_TIME} ms
                
                Detailed Breakdown:
                - Checkout: ${env.CHECKOUT_TIME} ms
                - Docker Build: ${env.BUILD_TIME} ms
                - Docker Push: ${env.PUSH_TIME} ms
                - EKS Deploy: ${env.EKS_DEPLOY_TIME} ms
                - GKE Deploy: ${env.GKE_DEPLOY_TIME} ms
                ==========================================
                """
                
                // Optional: You can add additional actions like sending a timing report via email
            }
            echo 'Deployment successful to both EKS and GKE!'
        }
        always {
            script {
                // Ensure pipeline start time is captured at the beginning of the pipeline
                env.PIPELINE_START = env.PIPELINE_START ?: System.currentTimeMillis()
            }
        }
        failure {
            echo 'Deployment failed. Check the logs for details.'
        }
    }
}