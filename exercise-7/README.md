# Exercise 7: Introduction to CI and Jenkins Installation

## Objective
Understand Continuous Integration and install Jenkins using Docker.

## Environment
Windows PowerShell and Docker Desktop running Linux containers.

## Installation
- Container: `jenkins-ci-lab`
- Image: `jenkins/jenkins:lts-jdk21`
- Web interface: http://localhost:8080
- Persistent volume: `exercise7_jenkins_home`

```powershell
docker volume create exercise7_jenkins_home
docker run -d --name jenkins-ci-lab --restart unless-stopped -p 127.0.0.1:8080:8080 -v exercise7_jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk21
```

## Setup
1. Start Jenkins and wait for startup.
2. Retrieve the initial administrator password.
3. Unlock Jenkins in the browser.
4. Install suggested plugins.
5. Create an administrator account.
6. Open the Jenkins dashboard.

## Verification
- [x] Jenkins container is running.
- [x] Browser setup completed.
- [x] Jenkins dashboard is accessible.

## Evidence
- [Container status](evidence/jenkins-container.txt)
- [Configuration](evidence/jenkins-configuration.txt)
- [HTTP response](evidence/jenkins-http-response.txt)

![Jenkins dashboard](evidence/Screenshot%202026-10-18%20193432.png)

## Learning
Continuous Integration uses frequent code integration and automated
builds and tests to detect issues early.

Jenkins can automate these workflows. This exercise installs the
server; Git triggers, builds, and tests require job configuration.

## Stop and Restart
```powershell
docker stop jenkins-ci-lab
docker start jenkins-ci-lab
```

This instance is separate from Exercise 6. Stopping it retains its data.

