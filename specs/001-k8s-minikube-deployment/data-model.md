# Data Model: Kubernetes Minikube Deployment

## Overview

This document defines the data structures and entities relevant to the Kubernetes Minikube deployment feature. Since this feature primarily focuses on deployment infrastructure rather than application data, the data model centers on configuration and deployment artifacts.

## Key Entities

### 1. Docker Configuration Entity
**Definition**: Configuration parameters for Docker containerization

**Attributes**:
- image_name: String - Name of the Docker image
- base_image: String - Base image for the container
- build_context: String - Path to build context
- build_args: Map[String, String] - Build-time variables
- exposed_ports: List[Int] - Ports exposed by the container
- environment_vars: Map[String, String] - Runtime environment variables
- health_check: Object - Health check configuration

**Relationships**:
- Belongs to one Deployment Configuration
- Referenced by one Container Runtime

### 2. Kubernetes Deployment Entity
**Definition**: Deployment configuration for Kubernetes orchestration

**Attributes**:
- name: String - Unique deployment name
- replicas: Int - Number of desired pod instances
- image: String - Container image reference
- resources_requests: Object - Minimum resource requirements
- resources_limits: Object - Maximum resource allowances
- environment: Map[String, String] - Environment variables
- volumes: List[Object] - Volume mounts configuration
- health_checks: Object - Liveness and readiness probes

**Relationships**:
- Contains multiple Kubernetes Pod entities
- Connected to one Kubernetes Service entity
- Uses ConfigMap and Secret entities for configuration

### 3. Kubernetes Service Entity
**Definition**: Service configuration for network access to deployments

**Attributes**:
- name: String - Unique service name
- type: String - Service type (ClusterIP, NodePort, LoadBalancer)
- selector: Map[String, String] - Labels to select target pods
- ports: List[Object] - Port mappings (port, targetPort, protocol)
- external_traffic_policy: String - How external traffic is routed

**Relationships**:
- Targets one or more Kubernetes Deployment entities
- May be accessed by external clients
- Connects internal and external network boundaries

### 4. Configuration Entity
**Definition**: Non-sensitive configuration data stored in ConfigMap

**Attributes**:
- name: String - Unique configuration name
- data: Map[String, String] - Configuration key-value pairs
- namespace: String - Kubernetes namespace

**Relationships**:
- Referenced by Kubernetes Deployment entities
- Stores application settings, URLs, and non-sensitive parameters

### 5. Secret Entity
**Definition**: Sensitive data stored securely in Kubernetes Secret

**Attributes**:
- name: String - Unique secret name
- data: Map[String, String] - Base64 encoded secret key-value pairs
- namespace: String - Kubernetes namespace
- type: String - Secret type (Opaque, kubernetes.io/basic-auth, etc.)

**Relationships**:
- Referenced by Kubernetes Deployment entities
- Stores passwords, API keys, and certificates

### 6. Helm Chart Entity
**Definition**: Packaged Kubernetes application with configurable parameters

**Attributes**:
- name: String - Chart name
- version: String - Chart version
- app_version: String - Application version
- description: String - Chart description
- values_schema: Object - Schema for value validation
- dependencies: List[Object] - Chart dependencies

**Relationships**:
- Contains multiple Kubernetes resource templates
- Uses values file for parameterization
- Deploys complete application stack

### 7. Helm Values Entity
**Definition**: Parameter values for Helm chart customization

**Attributes**:
- frontend_config: Object - Frontend service configuration
- backend_config: Object - Backend service configuration
- mcp_server_config: Object - MCP server configuration
- resource_constraints: Object - Resource requests and limits
- image_tags: Object - Image version tags
- replica_counts: Object - Replica counts for deployments

**Relationships**:
- Applied to Helm Chart during installation
- Overrides default values in templates
- Enables environment-specific configurations

## State Transitions

### Docker Build State Machine
- INITIALIZED → BUILDING (on build trigger)
- BUILDING → SUCCESSFUL (on successful build completion)
- BUILDING → FAILED (on build failure)
- SUCCESSFUL → PUSHED (on successful registry push)

### Kubernetes Deployment State Machine
- CREATED → PENDING (on deployment creation)
- PENDING → RUNNING (on pod scheduling)
- RUNNING → FAILED (on deployment failure)
- RUNNING → TERMINATED (on deletion request)
- FAILED → RUNNING (on successful restart)

### Helm Release State Machine
- UNKNOWN → DEPLOYED (on initial install)
- DEPLOYED → FAILED (on installation failure)
- DEPLOYED → DELETED (on uninstall)
- DEPLOYED → SUPERSEDED (on upgrade)

## Validation Rules

### Docker Configuration Validation
- image_name must follow valid Docker naming conventions
- exposed_ports must be in valid port range (1-65535)
- base_image must be a valid Docker image reference
- build_context must exist in the filesystem

### Kubernetes Deployment Validation
- replica count must be non-negative
- resource requests must be less than or equal to limits
- environment variables keys must follow DNS label rules
- selectors must match pod labels

### Service Validation
- port numbers must be in valid range (1-65535)
- service type must be one of allowed types
- selector labels must match deployment labels

### Helm Chart Validation
- chart version must follow semantic versioning
- required values must be present
- value types must match schema definitions
- templates must render without errors

## Relationships Summary

- **Docker Configuration** → **Kubernetes Deployment**: Provides container image
- **Configuration Entity** → **Kubernetes Deployment**: Supplies non-sensitive config
- **Secret Entity** → **Kubernetes Deployment**: Supplies sensitive config
- **Kubernetes Deployment** → **Kubernetes Service**: Defines service target
- **Helm Chart** → **Kubernetes Deployment/Service**: Template source
- **Helm Values** → **Helm Chart**: Parameterization source

## Architecture Patterns

### Infrastructure as Code
- Kubernetes manifests define desired state
- Helm charts package reusable infrastructure components
- Templates enable parameterized deployments

### Configuration Management
- Separation of code and configuration
- Environment-specific overrides
- Secure storage for sensitive data

### Container Orchestration
- Declarative infrastructure definition
- Automated deployment and scaling
- Service discovery and load balancing