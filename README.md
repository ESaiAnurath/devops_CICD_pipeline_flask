<div align="center">

# 🚀 End-to-End CI/CD Pipeline for Flask Application
### using GitHub • Jenkins • Docker • Docker Hub • AWS EC2

*Automating the complete deployment lifecycle — from `git push` to a live, running application — with zero manual steps.*

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
10. [Real Challenges & Troubleshooting](#-real-challenges--troubleshooting)
11. [Screenshots](#-screenshots)
12. [Important Commands Reference](#-important-commands-reference)
13. [Interview Questions From This Project](#-interview-questions-from-this-project)
14. [Learning Outcomes](#-learning-outcomes)
15. [Future Improvements](#-future-improvements)
16. [Author](#-author)

---

## 📖 Project Overview

This project implements a **fully automated CI/CD pipeline** for a Python Flask application. Every time code is pushed to GitHub, the application is automatically **built, containerized, pushed to a registry, and deployed to a live AWS EC2 server** — with no manual intervention.

> 💡 **In short:** `git push` → live, updated application. That's the entire deployment process for the developer.

This project was built to demonstrate practical, hands-on understanding of **Continuous Integration (CI)** and **Continuous Deployment (CD)**, using the same category of tools used in real production environments.

---

## 🎯 Project Goal

Manually deploying an application is slow and error-prone: build a Docker image, log in to a registry, push the image, SSH into a server, stop the old container, remove it, pull the new image, and start a new container — every single time the code changes.

The goal of this project is to **eliminate every manual step** in that process by encoding it into a Jenkins pipeline, so that deployment becomes:

- ✅ Repeatable
- ✅ Fast
- ✅ Consistent (no "it worked on my machine")
- ✅ Free of human error

---

## 🧰 Tech Stack

| Category | Tool | Why It Was Used |
|---|---|---|
| **Backend Framework** | Python Flask | Lightweight, fast to set up, ideal for demonstrating a real deployable web service |
| **Production Server** | Gunicorn | Flask's built-in server is single-threaded and not designed for production traffic; Gunicorn is a production-grade WSGI server that handles concurrent requests reliably |
| **Containerization** | Docker | Packages the app with all its dependencies into one portable unit — guarantees the app runs identically on any machine, dev or prod |
| **Container Registry** | Docker Hub | A central, always-available location to store and version built images so any server can pull the exact image that was tested |
| **Version Control** | Git | Tracks every code change, enables rollback, and is the trigger point for the entire pipeline |
| **Source Code Management** | GitHub | Hosts the repository and provides **webhooks**, which is what allows GitHub to automatically notify Jenkins the instant new code is pushed |
| **CI/CD Orchestration** | Jenkins | An open-source automation server that executes the build → push → deploy sequence automatically, exactly the same way every single time |
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
┌────────────┐     ┌─────────┐     ┌──────────┐     ┌─────────┐     ┌───────────┐     ┌────────────┐     ┌────────────┐
│ Developer  │────▶│ GitHub  │────▶│ Webhook  │────▶│ Jenkins │────▶│ Build     │────▶│ Docker Hub │────▶│ AWS EC2    │
│ (git push) │     │  Repo   │     │ Trigger  │     │ Pipeline│     │ Docker    │     │ (Registry) │     │ (Deploy)   │
└────────────┘     └─────────┘     └──────────┘     └─────────┘     │ Image     │     └────────────┘     └─────┬──────┘
                                                                     └───────────┘                              │
                                                                                                                 ▼
                                                                                                         ┌────────────────┐
                                                                                                         │ Docker Container│
                                                                                                         │ Flask Application│
                                                                                                         │  (Live & Running)│
                                                                                                         └────────────────┘
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
1.  Developer writes code
        ↓
2.  Developer pushes code to GitHub
        ↓
3.  GitHub webhook automatically triggers Jenkins
        ↓
4.  Jenkins pulls the latest source code
        ↓
5.  Jenkins builds a Docker image
        ↓
6.  Jenkins logs into Docker Hub
        ↓
7.  Jenkins pushes the Docker image
        ↓
8.  Jenkins connects to AWS EC2 via SSH
        ↓
9.  EC2 pulls the latest Docker image
        ↓
10. Old Docker container is stopped
        ↓
11. Old Docker container is removed
        ↓
12. New Docker container starts
        ↓
13. ✅ Updated application is live — automatically
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

> 💡 **Why GitHub in a CI/CD pipeline?**
> GitHub isn't just storage — it's the **trigger mechanism**. Its webhook feature notifies Jenkins the moment new code is pushed, which is what makes the pipeline "continuous" instead of something you have to run manually.

### 5️⃣ Installed Jenkins Inside a Docker Container
**Purpose:** Automate the build, test, and deployment process.

> 💡 **Why Jenkins?**
> Jenkins is the industry-standard open-source automation server for CI/CD. It listens for triggers (like a GitHub webhook), executes a defined sequence of steps (the pipeline), and reports success/failure — removing all manual deployment work.

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

This ensures every single build starts from the exact current state of the `main` branch — never a stale or cached copy.

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
docker pull image:latest      # Downloads the newest image from Docker Hub
docker stop devops-demo-app   # Gracefully stops the currently running container
docker rm devops-demo-app     # Removes the stopped container so the name/port is freed
docker run -d --name devops-demo-app -p 5000:5000 image:latest   # Starts the new version
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

## 🐞 Real Challenges & Troubleshooting

This section documents actual problems encountered during the build — and how each was resolved. This is often what interviewers care about most, since it proves hands-on debugging experience rather than just following a tutorial.

| Issue | Root Cause | Fix |
|---|---|---|
| **Jenkins container could not SSH into EC2** | The Jenkins Docker container didn't have the SSH Agent plugin configured, and no key was mounted/loaded | Installed the **SSH Agent plugin** and added the private key as a Jenkins credential (`deploy-server-ssh-key`) |
| **`deploy-server-ssh-key` not found** | Credential ID in the Jenkinsfile didn't exactly match the ID configured in Jenkins' Credentials Store | Re-checked and matched the credential ID exactly (IDs are case-sensitive) |
| **Docker permission denied** | The Jenkins user account didn't have permission to access the Docker daemon | Added the `jenkins` user to the `docker` group: `sudo usermod -aG docker jenkins`, then restarted Jenkins |
| **Ubuntu user not in Docker group (on EC2)** | Same root cause as above, but on the deploy server itself | `sudo usermod -aG docker ubuntu` and re-logged in for the group change to take effect |
| **Permission denied accessing `docker.sock`** | The Docker socket file has restrictive permissions by default, and the calling user wasn't in the `docker` group | Fixed by correcting group membership (see above) instead of unsafely `chmod`-ing the socket |
| **Extra braces / Groovy syntax errors in Jenkinsfile** | Declarative pipeline syntax is strict — a missing or extra `{ }` breaks the entire pipeline parse step | Used Jenkins' **"Replay"** and **"Validate Declarative Pipeline"** tools to pinpoint the exact line, then corrected the brace structure |
| **SSH connectivity issues** | EC2 Security Group didn't have port 22 open to the Jenkins server's IP | Updated the inbound rule to allow SSH from the correct source |
| **Pipeline failed multiple times on first setup** | Combination of missing plugins, wrong credential IDs, and syntax issues | Debugged stage-by-stage using **Jenkins Console Output**, fixing one error at a time rather than rewriting the whole pipeline |
| **Confusion between `localhost` and public IP** | Tried accessing the app via `localhost` from a local machine, which doesn't resolve to the remote EC2 server | Used the EC2 instance's **public IPv4 address** instead |
| **Docker login warnings** | Docker CLI warned about storing credentials in plaintext config | Used credential injection via Jenkins (`docker login -u $USER -p $PASS`) rather than manual, persistent `docker login` sessions |

> 📌 **Key takeaway:** Almost every real DevOps issue in this project traced back to either **permissions** (Linux user/group access) or **credential/ID mismatches** — both extremely common in real-world CI/CD debugging.

---

## 📸 Screenshots

> Replace these placeholders with your actual screenshots in the `screenshots/` folder.

| # | Screenshot | Description |
|---|---|---|
| 01 | `screenshots/01-github-repo.png` | GitHub Repository |
| 02 | `<img width="1919" height="886" alt="image" src="https://github.com/user-attachments/assets/8f616ee2-fe31-4c2f-8679-76a1ba45e39c" />
` | Jenkins Dashboard |
| 03 | `screenshots/03-successful-pipeline.png` | Successful Pipeline Run |
| 04 | `screenshots/04-console-output.png` | Jenkins Console Output |
| 05 | `screenshots/05-docker-images.png` | Docker Images (`docker images`) |
| 06 | `screenshots/06-dockerhub-repo.png` | Docker Hub Repository |
| 07 | `screenshots/07-ec2-instance.png` | AWS EC2 Instance |
| 08 | `screenshots/08-security-group.png` | Security Group Configuration |
| 09 | `screenshots/09-running-container.png` | Running Docker Container (`docker ps`) |
| 10 | `screenshots/10-app-running.png` | Application Running in Browser |
| 11 | `screenshots/11-github-webhook.png` | GitHub Webhook Configuration |

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


## 🎓 Learning Outcomes

Through building this project, the following skills were developed hands-on:

- 🐳 **Docker** — writing Dockerfiles, image tagging, container lifecycle management
- ⚙️ **Jenkins** — declarative pipelines, plugins, credentials management, webhook triggers
- 🐧 **Linux** — user/group permissions, systemd services, file permissions
- ☁️ **AWS** — EC2 provisioning, Security Groups, cloud server management
- 🌐 **GitHub** — version control, webhooks, repository management
- 📦 **Docker Hub** — image registries, push/pull workflows
- 🔐 **SSH** — key-based authentication, secure remote command execution
- 🔄 **CI/CD** — end-to-end automated build/test/deploy pipeline design
- 🧩 **Pipeline Design** — structuring multi-stage, fail-fast automation workflows

---

## 🚧 Future Improvements

- [ ] Add automated **unit testing** with **Pytest** as a pipeline stage/quality gate
- [ ] Integrate **SonarQube** for static code quality analysis
- [ ] Add **Trivy** for Docker image vulnerability scanning
- [ ] Add **OWASP Dependency Check** for dependency vulnerability scanning
- [ ] Add an **Nginx reverse proxy** in front of the app for SSL termination and load balancing
- [ ] Use **Docker Compose** for multi-container orchestration
- [ ] Migrate deployment to **Kubernetes** for scalability and self-healing
- [ ] Provision infrastructure with **Terraform** (Infrastructure as Code)
- [ ] Automate server configuration with **Ansible**
- [ ] Add **Prometheus + Grafana** for real-time monitoring and alerting
- [ ] Explore **GitHub Actions** as an alternative/complementary CI/CD trigger
- [ ] Implement **Blue-Green Deployment** and **Rolling Updates** for zero-downtime releases

---

## 👤 Author

Built and documented as a hands-on DevOps portfolio project demonstrating real-world CI/CD pipeline design, cloud deployment, and troubleshooting skills.

**Connect with me:** *[Add your LinkedIn / GitHub / Portfolio links here]*

---

<div align="center">

⭐ **If you found this project useful, consider giving it a star!** ⭐

</div>
