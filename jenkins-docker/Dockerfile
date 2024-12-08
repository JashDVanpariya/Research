# Use the official Jenkins LTS image as the base
FROM jenkins/jenkins:lts

# Skip the setup wizard
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# Switch to root for installing additional tools
USER root

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    docker.io \
    curl \
    jq \
    unzip \
    awscli \
    apt-transport-https \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

# Install Google Cloud SDK
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-432.0.0-linux-x86_64.tar.gz && \
    tar -xvzf google-cloud-sdk-432.0.0-linux-x86_64.tar.gz && \
    ./google-cloud-sdk/install.sh && \
    rm -rf google-cloud-sdk-432.0.0-linux-x86_64.tar.gz

# Add Google Cloud SDK to PATH
ENV PATH="/google-cloud-sdk/bin:$PATH"

# Install GKE Auth Plugin
RUN curl -LO https://storage.googleapis.com/artifacts.k8s.io/binaries/kubernetes-client-go-auth-gcp/release/latest/gke-gcloud-auth-plugin && \
    chmod +x gke-gcloud-auth-plugin && \
    mv gke-gcloud-auth-plugin /usr/local/bin/

# Add Jenkins user to Docker group
RUN usermod -aG docker jenkins

# Expose adjusted Jenkins ports
EXPOSE 9090
EXPOSE 50002

# Switch back to Jenkins user
USER jenkins

# Set Jenkins home directory
ENV JENKINS_HOME=/var/jenkins_home
WORKDIR $JENKINS_HOME
