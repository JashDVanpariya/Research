pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sledgy/webapp:latest'
        AWS_REGION = 'eu-west-1'
        EKS_CLUSTER_NAME = 'eks-cluster'
        GCP_PROJECT_ID = 'gold-circlet-439215-k9'
        GCP_CLUSTER_NAME = 'gke-cluster'
        GCP_ZONE = 'europe-west1-b'
        KUBECONFIG_PATH = '/var/jenkins_home/.kube/config'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/JashDVanpariya/Research.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def buildStart = System.currentTimeMillis()
                    sh 'docker build -t $DOCKER_IMAGE .'
                    def buildEnd = System.currentTimeMillis()
                    def buildDuration = (buildEnd - buildStart) / 1000
                    echo "Docker Build Time: ${buildDuration} seconds"
                }
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                withDockerRegistry([credentialsId: 'dockerhub-credentials-id', url: '']) {
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    def deployStart = System.currentTimeMillis()
                    sh "aws eks update-kubeconfig --region $AWS_REGION --name $EKS_CLUSTER_NAME"
                    sh "kubectl apply -f k8s/eks-deployment.yaml"
                    def deployEnd = System.currentTimeMillis()
                    def deployDuration = (deployEnd - deployStart) / 1000
                    echo "EKS Deployment Time: ${deployDuration} seconds"
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                script {
                    def deployStart = System.currentTimeMillis()
                    sh "gcloud auth activate-service-account --key-file=/path/to/your-service-account-key.json"
                    sh "gcloud container clusters get-credentials $GCP_CLUSTER_NAME --zone $GCP_ZONE --project $GCP_PROJECT_ID"
                    sh "kubectl apply -f k8s/gke-deployment.yaml"
                    def deployEnd = System.currentTimeMillis()
                    def deployDuration = (deployEnd - deployStart) / 1000
                    echo "GKE Deployment Time: ${deployDuration} seconds"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
