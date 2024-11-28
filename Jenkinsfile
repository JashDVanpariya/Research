stage('Verify Deployment') {
    steps {
        script {
            sh "kubectl get deployments"
            sh "kubectl get pods"
            sh "kubectl get svc"
        }
    }
}pipeline {
    agent any
    environment {
        PROJECT_ID = 'gold-circlet-439215-k9'
        IMAGE_NAME = 'my-expense-app'
        IMAGE_TAG = 'latest'
        GCR_URI = "europe-west1-docker.pkg.dev/${PROJECT_ID}/my-gcr-repo/${IMAGE_NAME}:${IMAGE_TAG}"
        KUBE_DEPLOYMENT = 'my-expense-app'
    }
    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/JashVanpariya/ResearchProject.git', branch: 'main'
            }
        }
        stage('Validate Environment') {
            steps {
                script {
                    sh 'gcloud container clusters list'
                    sh 'gcloud auth list'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${GCR_URI} ."
                }
            }
        }
        stage('Push to GCR') {
            steps {
                script {
                    sh "gcloud auth configure-docker europe-west1-docker.pkg.dev --quiet"
                    sh "docker push ${GCR_URI}"
                }
            }
        }
        stage('Deploy to GKE') {
            steps {
                script {
                    sh "gcloud container clusters get-credentials my-cluster --zone europe-west1-b"
                    
                    // Apply Kubernetes Deployment
                    sh """
                    cat <<EOF | kubectl apply -f -
                    apiVersion: apps/v1
                    kind: Deployment
                    metadata:
                      name: ${KUBE_DEPLOYMENT}
                    spec:
                      replicas: 2
                      selector:
                        matchLabels:
                          app: ${KUBE_DEPLOYMENT}
                      template:
                        metadata:
                          labels:
                            app: ${KUBE_DEPLOYMENT}
                        spec:
                          containers:
                          - name: ${KUBE_DEPLOYMENT}
                            image: ${GCR_URI}
                            ports:
                            - containerPort: 8081
                            resources:
                              requests:
                                memory: "256Mi"
                                cpu: "250m"
                              limits:
                                memory: "512Mi"
                                cpu: "500m"
                    EOF
                    """
                    
                    // Apply Kubernetes Service
                    sh """
                    cat <<EOF | kubectl apply -f -
                    apiVersion: v1
                    kind: Service
                    metadata:
                      name: ${KUBE_DEPLOYMENT}-service
                    spec:
                      selector:
                        app: ${KUBE_DEPLOYMENT}
                      ports:
                      - protocol: TCP
                        port: 80
                        targetPort: 8081
                      type: LoadBalancer
                    EOF
                    """
                }
            }
        }
    }
    post {
        always {
            script {
                sh "docker rmi ${GCR_URI} || true"
                echo 'Pipeline Completed'
            }
        }
    }
}
         