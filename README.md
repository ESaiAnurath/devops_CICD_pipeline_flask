<div align="center">

# 🚀 End-to-End CI/CD Pipeline for Flask Application
### using GitHub • Jenkins • Docker • Docker Hub • AWS EC2

## 📸 OUTCOMES

| # | Screenshot | Description |
|---|---|---|
| 01 | `screenshots/01-github-repo.png` | GitHub Repository |
| 02 | `<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/8f616ee2-fe31-4c2f-8679-76a1ba45e39c"/>` | Jenkins Dashboard |
| 03 | `screenshots/03-successful-pipeline.png` | Successful Build |
| 04 | `` | Jenkins Console Output |
| 05 | `<img width="1888" height="172" alt="image" src="https://github.com/user-attachments/assets/4756e792-146d-41d4-9917-a48c481b60c4"/>` | Docker Images |
| 06 | `<img width="1919" height="883" alt="image" src="https://github.com/user-attachments/assets/c429128f-4571-4b79-9c2e-ff117cbcbe1b" />` | DockerHub Repository |
| 07 | `<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/f977a5b9-ec40-4cbc-8541-1f87de103fb3"/>` | EC2 Instance |
| 08 | `<img width="1919" height="885" alt="image" src="https://github.com/user-attachments/assets/73264c5b-8e2b-4b37-91f3-40dcfea06e83"/>` | Security Group |
| 09 | `<img width="1854" height="78" alt="image" src="https://github.com/user-attachments/assets/29f7825e-421b-4cd5-b11b-d0457bc99501"/>` | Running Container (`docker ps`) |
| 10 | `<img width="1605" height="973" alt="image" src="https://github.com/user-attachments/assets/36855752-d267-4f24-9053-a5bfc2b0de8b" />` | Browser Output |

---

*Deploying a Flask application through a Jenkins pipeline — from `git push` to a manually triggered, live running application.*

![CI/CD](https://img.shields.io/badge/CI%2FCD-Automated-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-Pipeline-D24939?logo=jenkins&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python-Flask-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)

</div>

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Project Goal](#-project-goal)
3. [Tech Stack](#-tech-stack)
4. [Project Structure](#-project-structure)
5. [Architecture Diagrams](#-architecture-diagrams)
6. [Project Workflow](#-project-workflow)
7. [What We Implemented](#-what-we-implemented-step-by-step)
8. [Jenkins Pipeline Details](#-jenkins-pipeline-details)
9. [AWS Configuration](#-aws-configuration)
10. [Jenkins Credentials](#-jenkins-credentials)
11. [Docker Deployment Process](#-docker-deployment-process)
12. [Real Challenges & Troubleshooting](#-real-challenges--troubleshooting)
13. [Important Commands Reference](#-important-commands-reference)
14. [Project Screenshots](#-project-screenshots)
15. [Learning Outcomes](#-learning-outcomes)
16. [Future Improvements](#-future-improvements)
17. [Author](#-author)

---

## 📖 Project Overview

This project implements a **CI/CD Pipeline with Manual Jenkins Trigger** for a Python Flask application. After pushing code to GitHub, Jenkins can be manually triggered to build and deploy the latest version of the application — the Flask app is built, containerized with Docker, pushed to Docker Hub, and deployed to a live AWS EC2 server over SSH. This pipeline does not use a GitHub webhook; the build is started manually via **Build Now**.

This project was built to demonstrate practical, hands-on understanding of **Continuous Integration (CI)** and **Continuous Deployment (CD)**, using the same category of tools used in real production environments.

---

## 🎯 Project Goal

The goal of this project was to:

- 📚 Learn how a CI/CD pipeline is implemented in practice
- ⚙️ Automate the build and deployment steps using Jenkins
- 🧹 Reduce manual deployment effort (build, push, SSH, restart container)
- 🐳 Deploy a Docker container of the Flask application on AWS EC2

---

## 🧰 Tech Stack

| Category | Tool | Why It Was Used |
|---|---|---|
| **Backend Framework** | Python Flask | Lightweight, fast to set up, ideal for demonstrating a real deployable web service |
| **Production Server** | Gunicorn | Flask's built-in server is single-threaded and not designed for production traffic; Gunicorn is a production-grade WSGI server that handles concurrent requests reliably |
| **Containerization** | Docker | Packages the app with all its dependencies into one portable unit — guarantees the app runs identically on any machine, dev or prod |
| **Container Registry** | Docker Hub | A central, always-available location to store and version built images so any server can pull the exact image that was tested |
| **Version Control** | Git | Tracks every code change and is the source of truth for what Jenkins builds |
| **Source Code Management** | GitHub | GitHub stores the source code repository that Jenkins clones during the Checkout stage |
| **CI/CD Orchestration** | Jenkins | An open-source automation server that executes the build → push → deploy sequence when manually triggered via **Build Now** |
| **Deployment Server** | AWS EC2 (Ubuntu) | A real cloud virtual machine that hosts the live, running application — simulating a production environment |
| **Remote Access** | SSH | A secure, encrypted channel that allows Jenkins to execute deployment commands on the remote EC2 server without exposing credentials in plain text |
| **Operating System** | Ubuntu Linux | Industry-standard, well-documented Linux distribution for both the Jenkins host and the EC2 deployment target |

---

## 📁 Project Structure

```
devops_CICD_pipeline_flask/
│
├── app/
│   ├── app.py                 # Flask application source code
│   ├── requirements.txt       # Python dependencies (Flask, Gunicorn)
│   └── Dockerfile             # Instructions to containerize the app
│
├── Jenkinsfile                 # Declarative CI/CD pipeline definition
├── README.md                   # Project documentation (this file)
└── screenshots/                 # Visual proof of each pipeline stage
```

---

## 🏗 Architecture Diagrams

### High-Level Pipeline Flow

```
Developer
      ↓
GitHub
      ↓
Manual Build (Build Now)
      ↓
Jenkins
      ↓
Docker Build
      ↓
Docker Hub
      ↓
EC2
      ↓
Docker Container
```

### Inside AWS EC2 — Container Lifecycle

```
                        ┌────────────────────────── AWS EC2 Instance (Ubuntu) ──────────────────────────┐
                        │                                                                                │
   Jenkins  ──SSH──────▶│   docker pull   ──▶   docker stop (old)   ──▶   docker rm (old)   ──▶  docker run (new)  │
                        │                                                                                │
                        │                         ┌───────────────────────────┐                          │
                        │                         │   New Docker Container     │                          │
                        │                         │   Flask + Gunicorn         │                          │
                        │                         │   Listening on port 5000   │                          │
                        │                         └───────────────────────────┘                          │
                        └────────────────────────────────────────────────────────────────────────────────┘
```

> 📝 **Note:** The old container is always fully removed before the new one starts, which prevents port conflicts and ensures the server only ever runs one live version of the app at a time.

---

## 🔄 Project Workflow

```
1. Developer writes code
2. Pushes code to GitHub
3. Opens Jenkins
4. Clicks Build Now
5. Jenkins clones repository
6. Builds Docker image
7. Pushes image to Docker Hub
8. Jenkins SSH into EC2
9. Pull latest Docker image
10. Stop old container
11. Remove old container
12. Start new container
13. Application available on EC2
```

---

## 🛠 What We Implemented (Step-by-Step)

### 1️⃣ Created a Flask REST API
**Purpose:** Simulate a real backend application that can be built, tested, and deployed.

Sample response:
```json
{
  "message": "Hello from the DevOps Pipeline Demo App!",
  "status": "running"
}
```

### 2️⃣ Created `requirements.txt`
**Purpose:** Pin and install Flask and Gunicorn so the exact same dependency versions are used in every environment (dev, CI, production).

### 3️⃣ Created the `Dockerfile`
**Purpose:** Containerize the Flask application so it runs identically anywhere.

The Dockerfile performs:
- Uses a lightweight **Python slim base image** (smaller image = faster builds and pulls)
- Creates a working directory inside the container
- Copies `requirements.txt` and installs dependencies (done *before* copying app code, so Docker can cache this layer and skip re-installing dependencies on every code change)
- Copies the application source code
- Exposes port `5000`
- Starts the app using **Gunicorn**, not Flask's built-in server

> ⚠️ **Why Gunicorn instead of the Flask development server?**
> Flask's built-in server (`app.run()`) is single-threaded, unoptimized, and explicitly documented by Flask itself as unsafe for production. Gunicorn is a WSGI HTTP server designed to handle multiple concurrent requests, worker processes, and production-level traffic reliably.

### 4️⃣ Created a GitHub Repository
**Purpose:** Central, version-controlled home for the code.

> 💡 **Why GitHub in this pipeline?**
> GitHub stores the source code repository. Whenever the Jenkins pipeline is triggered after pushing code to GitHub, Jenkins clones the latest version of the repository as the first step of the build.

### 5️⃣ Installed Jenkins Inside a Docker Container
**Purpose:** Automate the build, test, and deployment process.

> 💡 **Why Jenkins?**
> Jenkins is the industry-standard open-source automation server for CI/CD. It executes a defined sequence of steps (the pipeline) when manually triggered, and reports success/failure — reducing manual deployment work.

> 💡 **Why run Jenkins inside Docker?**
> Running Jenkins as a container keeps the host machine clean, makes Jenkins easy to back up/restore/move, and avoids polluting the host with Jenkins' own dependencies (Java, plugins, etc.).

### 6️⃣ Installed Docker Inside AWS EC2
**Purpose:** Allow the EC2 server to pull and run the application's Docker containers.

### 7️⃣ Configured Docker Hub Credentials Inside Jenkins
- **Credential Type:** Username + Password
- **Credential ID:** `dockerhub-creds`

> ⚠️ **Why credentials should never be hardcoded:**
> Hardcoding a username/password directly into a Jenkinsfile means anyone with read access to the repository — including on public GitHub — can see and misuse those credentials. Jenkins' built-in **Credentials Store** encrypts secrets at rest and injects them into the pipeline only at runtime, so they never appear in the source code or in plain text in logs.

### 8️⃣ Configured SSH Credentials
- **Credential Type:** SSH Username with Private Key
- **Credential ID:** `deploy-server-ssh-key`
- **Username:** `ubuntu`

> 💡 **Why SSH?**
> SSH provides an encrypted channel between Jenkins and the EC2 server, authenticated via key pairs rather than passwords. This means Jenkins can securely execute remote commands (pull image, restart container) without exposing login credentials over the network.

### 9️⃣ Created a Jenkins Declarative Pipeline
Pipeline stages: **Checkout → Build Docker Image → Push Docker Image → Deploy → Post**

(Each stage is explained in detail below.)

---

## ⚙️ Jenkins Pipeline Details

### 🔹 Stage 1 — Checkout
**Purpose:** Pull the latest code from GitHub into the Jenkins workspace.

This ensures every build starts from the exact current state of the `main` branch — never a stale or cached copy.

### 🔹 Stage 2 — Build Docker Image
**Purpose:** Package the application and its dependencies into a Docker image.

```bash
docker build -t image:buildnumber -t image:latest .
```

> 🏷️ **Tagging strategy explained:**
> - `image:buildnumber` — a unique, immutable tag per build (e.g. `image:42`). This means you can always trace exactly which pipeline run produced which image, and roll back to any specific previous version.
> - `image:latest` — a moving tag that always points to the most recent successful build, used for convenience when deploying "whatever is newest."

### 🔹 Stage 3 — Push Docker Image
**Purpose:** Upload the built image to Docker Hub so it's accessible from anywhere, including the EC2 server.

> 💡 **Why push both tags?**
> Pushing the `buildnumber` tag preserves a full history of every version ever built (useful for rollback and auditing). Pushing `latest` gives the deploy stage a single, predictable tag to always pull.

### 🔹 Stage 4 — Deploy
**Purpose:** SSH into the EC2 server and replace the running container with the newly built one.

```bash
docker pull

docker stop

docker rm

docker run
```

Each command explained:
| Command | What It Does |
|---|---|
| `docker pull` | Fetches the latest image layers from Docker Hub onto the EC2 server |
| `docker stop` | Sends a graceful shutdown signal to the currently running container |
| `docker rm` | Deletes the stopped container object (the image itself is untouched) |
| `docker run -d` | Starts a new container in detached (background) mode from the freshly pulled image |

### 🔹 Stage 5 — Post
**Purpose:** Run cleanup and status-reporting actions regardless of whether the pipeline succeeded or failed (e.g., `docker logout`, success/failure logging).

---

## ☁️ AWS Configuration

| Component | Configuration |
|---|---|
| **Instance** | EC2 Ubuntu Server |
| **Software Installed** | Docker |
| **Connectivity** | Jenkins connects via SSH |

### Inbound Security Group Rules

| Port | Purpose | Why It's Open |
|---|---|---|
| `22` | SSH | Required for Jenkins to remotely execute deployment commands on the server |
| `5000` | Flask App | The port the containerized application listens on, so it's reachable from a browser |
| `8080` | Jenkins UI | Allows access to the Jenkins web dashboard for managing and monitoring pipelines |

> ⚠️ **Best Practice Note:** In a real production environment, port 22 should be restricted to specific trusted IP addresses rather than open to `0.0.0.0/0`, to reduce attack surface.

---

## 🔐 Jenkins Credentials

| Credential | Type | Credential ID |
|---|---|---|
| **DockerHub Credentials** | Username + Password | `dockerhub-creds` |
| **SSH Private Key** | SSH Username with Private Key | `deploy-server-ssh-key` |

These credentials are stored in Jenkins' built-in **Credentials Store**, which encrypts secrets at rest and injects them into the pipeline only at runtime — keeping them out of the Jenkinsfile and out of build logs.

---

## 🐳 Docker Deployment Process

```
docker pull

docker stop

docker rm

docker run
```

On the EC2 server, Jenkins connects over SSH and runs this sequence: it **pulls** the latest image from Docker Hub, **stops** the currently running container, **removes** that stopped container, and then **runs** a new container from the freshly pulled image. This guarantees the server always ends up running exactly one, up-to-date instance of the application.

---

## 🐞 Real Challenges & Troubleshooting

This section documents actual problems encountered during the build — and how each was resolved.

| Issue | Root Cause | Fix |
|---|---|---|
| **Docker permission denied** | The Jenkins user account didn't have permission to access the Docker daemon | Added the `jenkins` user to the `docker` group: `sudo usermod -aG docker jenkins`, then restarted Jenkins |
| **Permission denied accessing `docker.sock`** | The Docker socket file has restrictive permissions by default, and the calling user wasn't in the `docker` group | Fixed by correcting group membership instead of unsafely `chmod`-ing the socket |
| **Jenkins container could not SSH into EC2 / SSH key issues** | The Jenkins Docker container didn't have the SSH Agent plugin configured, and no key was mounted/loaded | Installed the **SSH Agent plugin** and added the private key as a Jenkins credential (`deploy-server-ssh-key`) |
| **`deploy-server-ssh-key` not found (wrong credential ID)** | Credential ID in the Jenkinsfile didn't exactly match the ID configured in Jenkins' Credentials Store | Re-checked and matched the credential ID exactly (IDs are case-sensitive) |
| **Jenkinsfile syntax errors** | Declarative pipeline syntax is strict — a missing or extra `{ }` breaks the entire pipeline parse step | Reviewed the pipeline stage-by-stage to pinpoint the exact line, then corrected the brace structure |
| **Missing docker group (on EC2)** | The `ubuntu` user wasn't in the `docker` group on the deploy server | `sudo usermod -aG docker ubuntu` and re-logged in for the group change to take effect |
| **Container not running after deploy** | Old container removal or new container start step failed silently | Debugged stage-by-stage using **Jenkins Console Output**, fixing one error at a time |
| **Security Group configuration** | Required ports (22, 5000, 8080) weren't open in the EC2 Security Group | Updated the inbound rules to allow the correct ports |

> 📌 **Key takeaway:** Almost every real DevOps issue in this project traced back to either **permissions** (Linux user/group access) or **credential/ID mismatches** — both extremely common in real-world CI/CD debugging.

---

## 💻 Important Commands Reference

```bash
# Docker
docker build -t image_name:tag .      # Build an image from a Dockerfile
docker images                          # List all local images
docker push image_name:tag             # Upload image to Docker Hub
docker pull image_name:tag             # Download image from Docker Hub
docker ps                              # List running containers
docker stop container_name             # Stop a running container
docker rm container_name               # Remove a stopped container
docker run -d --name app -p 5000:5000 image_name:tag   # Run a container in the background

# Git
git clone <repo-url>                   # Clone a repository
git add .                              # Stage changes
git commit -m "message"                # Commit changes
git push origin main                   # Push to GitHub

# System / Server
sudo systemctl status jenkins          # Check Jenkins service status
sudo systemctl restart jenkins         # Restart Jenkins
sudo usermod -aG docker jenkins        # Add jenkins user to docker group
chmod 400 key.pem                      # Restrict SSH key file permissions
ssh -i key.pem ubuntu@<ec2-public-ip>  # Connect to EC2 via SSH
```

---

## 📸 Project Screenshots

- GitHub Repository
- Jenkins Dashboard
- Successful Build
- Jenkins Console Output
- Docker Images
- DockerHub Repository
- EC2 Instance
- Security Group
- Running Container
- Browser Output

---

## 🎓 Learning Outcomes

Through building this project, the following skills were developed hands-on:

- 🐳 **Docker** — writing Dockerfiles, image tagging, container lifecycle management
- ⚙️ **Jenkins** — declarative pipelines, plugins, credentials management, **Manual Jenkins Pipeline Execution**
- 🐧 **Linux** — user/group permissions, systemd services, file permissions
- ☁️ **AWS EC2** — provisioning, Security Groups, cloud server management
- 🔐 **SSH** — key-based authentication, secure remote command execution
- 📦 **Docker Hub** — image registries, push/pull workflows
- 🔄 **CI/CD Pipeline** — end-to-end automated build/deploy pipeline design

---

## 🚀 Future Improvements

- [ ] Add **GitHub Webhooks** to trigger the pipeline automatically
- [ ] Implement **Automatic Pipeline Trigger** on every push
- [ ] Add automated **Unit Testing** with **Pytest** as a pipeline stage/quality gate
- [ ] Integrate **SonarQube** for static code quality analysis
- [ ] Add **Trivy** for Docker image vulnerability scanning
- [ ] Use **Docker Compose** for multi-container orchestration
- [ ] Migrate deployment to **Kubernetes** for scalability and self-healing
- [ ] Provision infrastructure with **Terraform** (Infrastructure as Code)
- [ ] Automate server configuration with **Ansible**
- [ ] Add **Prometheus + Grafana** for real-time monitoring and alerting
- [ ] Explore **GitHub Actions** as an alternative/complementary CI/CD trigger

---

## 👤 Author

Built and documented as a hands-on DevOps portfolio project demonstrating real-world CI/CD pipeline design, cloud deployment, and troubleshooting skills.

**Connect with me:** *[Add your LinkedIn / GitHub / Portfolio links here]*

---

<div align="center">

⭐ **If you found this project useful, consider giving it a star!** ⭐

</div>
