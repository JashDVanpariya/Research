# Use the official Jenkins LTS image as the base
FROM jenkins/jenkins:lts

# Skip the setup wizard
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

# Install Docker inside the Jenkins container for building and running Docker images
USER root
RUN apt-get update && apt-get install -y docker.io

# Set user back to Jenkins
USER jenkins

# Expose the Jenkins web UI port and agent port
EXPOSE 8080
EXPOSE 50000