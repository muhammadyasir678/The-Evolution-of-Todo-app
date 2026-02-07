---
name: cloud-infrastructure
description: Design, deploy, and operate production-grade cloud infrastructure using managed Kubernetes, CI/CD, monitoring, and infrastructure as code.
---

# Cloud Infrastructure Engineering

## Instructions

1. **Cloud Platform Deployment**
   - Deploy containerized applications to managed Kubernetes:
     - Azure Kubernetes Service (AKS)
     - Google Kubernetes Engine (GKE)
     - DigitalOcean Kubernetes (DOKS)
   - Configure namespaces, node pools, and autoscaling
   - Use container registries (ACR, GCR, Docker Hub)

2. **CI/CD Pipelines**
   - Create GitHub Actions workflows for:
     - Build and test stages
     - Container image creation
     - Secure image publishing
     - Automated Kubernetes deployments
   - Manage secrets using GitHub Secrets and cloud secret managers

3. **Infrastructure as Code (IaC)**
   - Provision cloud resources using:
     - Terraform (preferred)
     - Cloud-native IaC tools when required
   - Maintain modular, reusable configurations
   - Support multiple environments (dev, staging, production)

4. **Monitoring & Logging**
   - Configure monitoring stacks:
     - Prometheus & Grafana
     - Cloud-native monitoring solutions
   - Centralize logs using managed logging services
   - Set up alerts for availability, performance, and cost anomalies

5. **Networking & Security**
   - Configure VPCs/VNETs, subnets, and routing
   - Secure clusters with:
     - RBAC
     - Network policies
     - Ingress controllers
   - Implement TLS, secrets management, and least-privilege access

6. **Cost Management & Optimization**
   - Right-size compute and storage resources
   - Enable autoscaling and resource limits
   - Monitor cloud spend and optimize continuously

## Best Practices
- Use GitOps principles for Kubernetes deployments
- Keep infrastructure definitions version-controlled
- Separate application and infrastructure concerns
- Automate everything that can be automated
- Design for security, scalability, and failure from day one
- Prefer managed services to reduce operational overhead

## Example Structure
```yaml
# Terraform Kubernetes Cluster (Example)
module "kubernetes" {
  source        = "./modules/kubernetes"
  cluster_name  = "production-cluster"
  region        = "us-central1"
  node_count    = 3
}
