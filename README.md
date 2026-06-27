Here is the entire `README.md` file layout ready to be copied into your project root as a single block:

```markdown
# Containerized Flask-MongoDB Stack with Kubernetes Orchestration

A production-ready, highly available deployment of a Python Flask microservice securely paired with an authenticated MongoDB database layer. This architecture is orchestrated locally via Kubernetes (`minikube`) and utilizes an automated, metric-driven Horizontal Pod Autoscaler (HPA) to handle traffic surges dynamically.

---

## Technical Architecture Overview

* **Application Tier:** A stateless Python-Flask web application running a baseline configuration of 2 replicas with strict container resource boundaries.
* **Database Tier:** A stateful MongoDB entity orchestrated via a `StatefulSet` tied directly to a local persistent block storage volume to ensure lifecycle data longevity.
* **Security & Authentication:** Zero hardcoded configuration policy. Administrative credentials and database connection URIs are injected into runtime containers using isolated native Kubernetes `Secrets`.
* **Automated Scalability:** Integrated infrastructure scaling via a Horizontal Pod Autoscaler monitoring active container computing metrics.

---

## Compute & Resource Constraints

To guarantee structural stability and isolate execution bounds, both deployment tiers are limited to identical production-grade resource constraints:

```yaml
resources:
  requests:
    cpu: "200m"     # 0.2 Core allocation baseline
    memory: "250Mi" # Baseline memory profile
  limits:
    cpu: "500m"     # Max ceiling capability
    memory: "500Mi" # Hard limit container constraint

```

---

## Operational Verification & Logs

### 1. Data Persistence & Cluster State Validation

Flawless end-to-end data round-trips verify successful communication, network discovery, and operational authentication between the compute containers and the database state layer.

**Ingest Stateful Record (`POST /data`):**

```powershell
Invoke-RestMethod -Uri "[http://127.0.0.1:56514/data](http://127.0.0.1:56514/data)" -Method Post -ContentType "application/json" -Body '{"student":"Akash","status":"fully-deployed"}'
# Output Status: Data inserted

```

**Query Data Pool (`GET /data`):**

```powershell
Invoke-RestMethod -Uri "[http://127.0.0.1:56514/data](http://127.0.0.1:56514/data)" -Method Get
# Output Payload: [{"student":"Akash","status":"fully-deployed"}]

```

---

### 2. Horizontal Pod Autoscaler (HPA) Load Test

The cluster is configured to trigger expansion immediately when average CPU overhead breaches a **70%** threshold. Under a multi-threaded load simulation, system utilization spiked significantly, prompting an automated horizontal expansion from 2 to 5 replicas.

```powershell
kubectl get hpa flask-app-hpa -w

```

| NAME | REFERENCE | TARGETS | MINPODS | MAXPODS | REPLICAS | AGE |
| --- | --- | --- | --- | --- | --- | --- |
| flask-app-hpa | Deployment/flask-app | 1%/70% | 2 | 5 | 2 | 16m |
| flask-app-hpa | Deployment/flask-app | 45%/70% | 2 | 5 | 2 | 20m |
| flask-app-hpa | Deployment/flask-app | **194%/70%** | 2 | 5 | **5** | 22m |

**Scale-Out Pod Status Verification:**
Running `kubectl get pods` during the peak load period captures all 5 application nodes initialized and sharing the system load flawlessly:

---

## Setup & Deployment Sequence

Follow these steps to instantiate and run the cluster environment locally:

1. **Initialize Cluster Environment & Enable Core Metrics:**
```powershell
minikube start --driver=docker
minikube addons enable metrics-server

```


2. **Expose Host Shell to Minikube Local Docker Daemon:**
```powershell
minikube docker-env | Invoke-Expression

```


3. **Compile Application Image Directly Inside Sandbox Registry:**
```powershell
cd flask-mongodb-app
docker build -t flask-mongodb-app:v1 .

```


4. **Instantiate Layered Orchestration Manifests:**
```powershell
kubectl apply -f ./k8s/secrets.yaml
kubectl apply -f ./k8s/mongodb.yaml
kubectl apply -f ./k8s/flask-app.yaml
kubectl apply -f ./k8s/hpa.yaml

```


5. **Expose App Routing Tunnel Link:**
```powershell
minikube service flask-service

```



```

```
