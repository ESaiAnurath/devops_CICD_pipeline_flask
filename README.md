# End-to-End DevOps CI/CD Pipeline (GitHub → Jenkins → Docker → Cloud → Prometheus → Grafana)

A complete, resume-ready DevOps project: a Flask app that gets automatically built, tested,
containerized, deployed to the cloud, and monitored — every time you push code to GitHub.

## Architecture

```
 Developer            GitHub              Jenkins (CI/CD)          Cloud Server(s)
 ─────────         ────────────         ──────────────────       ──────────────────
 git push  ─────▶  main branch  ──▶  Webhook triggers  ──▶  1. Checkout code
                                      Jenkins pipeline         2. Install deps
                                                                3. Run pytest tests
                                                                4. Build Docker image
                                                                5. Push image → DockerHub
                                                                6. SSH deploy to server
                                                                        │
                                                                        ▼
                                                        ┌───────────────────────────┐
                                                        │  App container running     │
                                                        │  on EC2 / VM (port 5000)    │
                                                        └───────────────────────────┘
                                                                        │
                                            ┌───────────────────────────┴───────────────────────────┐
                                            ▼                                                        ▼
                                  Prometheus (scrapes metrics)                          Grafana (visualizes metrics)
                                  - node-exporter (server health)                       - dashboards
                                  - Jenkins metrics                                     - alerts
                                  - app metrics
```

**Tools used:** GitHub (source control + webhook trigger), Jenkins (CI/CD orchestration),
Docker (containerization), DockerHub (image registry), a cloud VM — AWS EC2 / Azure / GCP
(hosting), Prometheus (metrics collection), Grafana (dashboards/alerting).

---

## Repo structure

```
devops-pipeline-project/
├── app/
│   ├── app.py              # Flask application
│   ├── test_app.py         # Unit tests (run by Jenkins)
│   ├── requirements.txt
│   └── Dockerfile
├── Jenkinsfile              # Defines the CI/CD pipeline stages
├── monitoring/
│   ├── prometheus.yml
│   └── docker-compose-monitoring.yml   # Spins up Prometheus + Grafana + Node Exporter
├── k8s/
│   └── deployment.yaml      # Optional: deploy to Kubernetes instead of a plain VM
└── README.md
```

---

## Step-by-step build guide

### Step 1 — Push this project to GitHub
```bash
cd devops-pipeline-project
git init
git add .
git commit -m "Initial commit: DevOps pipeline project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/devops-pipeline-project.git
git push -u origin main
```
This is your **single source of truth**. Every pipeline run starts from a `git push` here.

### Step 2 — Launch a cloud server for Jenkins
Spin up one Ubuntu 22.04 VM (AWS EC2 `t2.medium` free/low-cost tier works fine, or use Azure/GCP
equivalents). Open inbound ports: `22` (SSH), `8080` (Jenkins UI), `5000` (app), `9090`
(Prometheus), `3000` (Grafana).

Install Jenkins:
```bash
sudo apt update
sudo apt install -y openjdk-17-jre docker.io
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install -y jenkins
sudo usermod -aG docker jenkins    # let Jenkins run docker commands
sudo systemctl restart jenkins
```
Visit `http://<server-ip>:8080`, unlock Jenkins with the initial admin password
(`sudo cat /var/lib/jenkins/secrets/initialAdminPassword`), and install the suggested plugins
plus: **Git**, **Docker Pipeline**, **SSH Agent**, **Prometheus metrics**, **JUnit**.

### Step 3 — Connect GitHub → Jenkins (webhook)
1. In Jenkins: **New Item → Pipeline**, point it at your GitHub repo, script path `Jenkinsfile`.
2. In GitHub repo: **Settings → Webhooks → Add webhook** → Payload URL
   `http://<jenkins-server-ip>:8080/github-webhook/`, content type `application/json`,
   trigger on **push events**.
3. In the Jenkins job, enable **"GitHub hook trigger for GITScm polling"**.

Now every `git push` automatically fires a new Jenkins build. This is the core of CI.

### Step 4 — Store credentials in Jenkins (never hardcode secrets)
**Manage Jenkins → Credentials → Add**:
- `dockerhub-creds` — DockerHub username/password (used to push images)
- `deploy-server-ssh-key` — SSH private key for the deploy target server

### Step 5 — Understand the pipeline stages (`Jenkinsfile`)
| Stage | What it does | Why it matters |
|---|---|---|
| Checkout | Pulls latest code from GitHub | Ensures build always uses current code |
| Install Dependencies | `pip install -r requirements.txt` | Reproducible build environment |
| Run Tests | `pytest` with JUnit report | **Pipeline fails fast** if tests fail — bad code never reaches production |
| Build Docker Image | `docker build` | Packages app + dependencies into one portable artifact |
| Push to DockerHub | `docker push` | Makes the image available to any server that pulls it |
| Deploy | SSH into server, pull image, restart container | Zero manual deployment steps |

### Step 6 — Set up monitoring (Prometheus + Grafana)
On the same server (or a separate monitoring VM):
```bash
cd monitoring
docker compose -f docker-compose-monitoring.yml up -d
```
This starts:
- **Prometheus** (`:9090`) — scrapes metrics every 15s from Node Exporter, Jenkins, and the app
- **Node Exporter** (`:9100`) — exposes CPU/RAM/disk metrics of the host
- **Grafana** (`:3000`, login `admin`/`admin`) — visualizes everything

In Grafana: **Connections → Data sources → Add → Prometheus** → URL
`http://prometheus:9090` → Save & Test. Then **Dashboards → New → Import** and use community
dashboard ID **1860** (Node Exporter Full) for instant server metrics visualization.

### Step 7 — Deploy the app (two options)
**Option A — plain Docker on a VM** (what the `Jenkinsfile` does by default): Jenkins SSHes into
the server and runs the container directly.

**Option B — Kubernetes** (`k8s/deployment.yaml`): swap the Deploy stage for
`kubectl apply -f k8s/deployment.yaml` if you want to demonstrate K8s knowledge — includes 2
replicas, resource limits, and a liveness probe hitting `/health`.

### Step 8 — Verify the full loop
1. Change something in `app/app.py`, commit, push to `main`.
2. Watch Jenkins auto-trigger a build (Blue Ocean view is nice for screenshots).
3. Confirm tests pass, image is pushed to DockerHub, and the app updates on the server.
4. Check Grafana — you should see the deploy show up as a blip in CPU/network graphs.

---

## What to say in your interview

- **"I built a full CI/CD pipeline"**: explain the trigger chain — GitHub webhook → Jenkins →
  automated test gate → Docker build → registry push → automated deploy.
- **"Why Docker?"**: consistent environment from dev → test → prod, no "works on my machine."
- **"Why a test stage before deploy?"**: shows you understand CI's real purpose — catching bugs
  before they reach users, not just automating deployment.
- **"How would you scale this?"**: mention Kubernetes (included here), blue-green or canary
  deployments, and separating Jenkins agents from the controller for parallel builds.
- **"How do you handle secrets?"**: Jenkins Credentials store, never committed to Git.
- **"What does Prometheus/Grafana add?"**: observability — you can see CPU/memory/error rates
  and set alerts (e.g., Grafana alert if app `/health` fails) instead of finding out about
  outages from users.

## Possible resume bullet points
- *Designed and implemented an end-to-end CI/CD pipeline (GitHub → Jenkins → Docker → AWS EC2)
  that automated build, test, and deployment, cutting manual deployment steps to zero.*
- *Containerized a Flask application with Docker and automated image builds/pushes to DockerHub
  triggered by GitHub webhooks.*
- *Set up Prometheus and Grafana for real-time infrastructure and application monitoring,
  including custom dashboards for CPU, memory, and request metrics.*
- *Wrote a declarative Jenkinsfile implementing a multi-stage pipeline with automated testing
  as a quality gate before deployment.*

## Next steps to go further (optional, great for standing out)
- Add Slack/email notifications on pipeline failure (Jenkins post-build step).
- Add a staging + production environment with manual approval gate before prod deploy.
- Add Grafana alerting rules (e.g., alert if error rate > 5% or CPU > 80% for 5 min).
- Use Terraform to provision the EC2/VM infrastructure itself (Infrastructure as Code).
- Replace SSH-deploy with Kubernetes + Helm for a more production-realistic setup.
