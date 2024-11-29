
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


FROM jenkins/jenkins:lts                         

# Skip the setup wizard
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

# Install Docker inside the Jenkins container for building and running Docker images
USER root
RUN apt-get update && apt-get install -y docker.io && \
    usermod -aG docker jenkins && \
    systemctl enable docker && \
    systemctl start docker

# Set user back to Jenkins
USER jenkins

# Expose the Jenkins web UI port and agent port
EXPOSE 8080
EXPOSE 50000

# Set the working directory to /var/jenkins_home
WORKDIR /var/jenkins_home

# Copy the Jenkins configuration files
COPY jenkins.config /var/jenkins_home/jenkins.config
COPY jenkins.xml /var/jenkins_home/jenkins.xml

# Set the environment variables
ENV JENKINS_HOME /var/jenkins_home
ENV JENKINS_USER jenkins
ENV JENKINS_GROUP jenkins

# Run the Jenkins containerUN /usr/local/bin/install-plugins.sh < /var/jenkins_home/plugins.txt
# Install plugins
RUN /usr/local/bin/install-plugins.sh < /var/jenkins_home/plugins.txt            
