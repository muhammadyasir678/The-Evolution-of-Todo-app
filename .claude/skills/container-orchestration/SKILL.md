---
name: container-orchestration
description: Containerize applications and orchestrate them using Docker and Kubernetes for local and cloud environments.
---

# Container Orchestration

## Instructions

1. **Containerization**
   - Create efficient Dockerfiles using multi-stage builds
   - Follow best practices for image size and security
   - Containerize frontend and backend applications separately

2. **Docker Compose**
   - Define multi-container applications with `docker-compose.yml`
   - Configure networks, volumes, and environment variables
   - Support local development and testing workflows

3. **Kubernetes Manifests**
   - Build core resources:
     - Deployments
     - Services
     - ConfigMaps
     - Secrets
   - Apply proper labels and selectors
   - Separate configuration from application code

4. **Helm Charts**
   - Create reusable Helm charts
   - Define values.yaml for environment-specific configuration
   - Manage chart dependencies and versioning

5. **Local Kubernetes Development**
   - Use Minikube for local clusters
   - Enable addons (Ingress, Metrics Server)
   - Validate manifests before cloud deployment

6. **Cloud Kubernetes Deployment**
   - Deploy workloads to managed Kubernetes:
     - AKS (Azure)
     - GKE (Google Cloud)
     - DOKS (DigitalOcean)
   - Configure namespaces and RBAC
   - Use container registries securely

7. **Reliability & Performance**
   - Implement liveness and readiness probes
   - Define CPU and memory requests/limits
   - Support rolling updates and zero-downtime deployments

## Best Practices
- Use minimal base images (alpine, distroless)
- Never hardcode secrets in images or manifests
- Version-control all manifests and Helm charts
- Keep development, staging, and production values separate
- Validate YAML with schema checks and dry runs

## Example Structure

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: app
          image: my-app:latest
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
