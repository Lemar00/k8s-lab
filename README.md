

# Kubernetes Lab.

This repository includes a FastAPI application connected to a PostgreSQL database, set up for seamless deployment within a Kubernetes environment.

## Prerequisites

Ensure you have the following installed before starting:

- [Docker](https://www.docker.com/get-started)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [PostgreSQL](https://www.postgresql.org/download/)

## Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/lemar00/k8s-lab.git
   cd k8s-lab
   ```

2. **Build the Docker Image**:

   Build the Docker image for the FastAPI application:

   ```bash
   docker build -t myapp-backend .
   ```

## Deployment

1. **Start Minikube**:

   Start a Minikube cluster with three nodes:

   ```bash
   minikube start --nodes 3 --driver=docker
   ```

2. **Apply Kubernetes Manifests**:

   Deploy the application and database by applying the Kubernetes manifest files:

   ```bash
   kubectl apply -f k8s/database-secret.yaml
   kubectl apply -f k8s/database-configmap.yaml
   kubectl apply -f k8s/database-deployment.yaml
   kubectl apply -f k8s/database-service.yaml
   kubectl apply -f k8s/backend-secret.yaml
   kubectl apply -f k8s/backend-configmap.yaml
   kubectl apply -f k8s/backend-deployment.yaml
   kubectl apply -f k8s/backend-service.yaml
   ```

3. **Verify Deployments**:

   Check that all pods are running:

   ```bash
   kubectl get pods
   ```

   You should see the backend and database pods with a `Running` status.

## Accessing the Application

To access the FastAPI application, find the NodePort for the backend service:

```bash
kubectl get services
```

Locate `backend-service` and note the `NodePort` (between `30000` and `30080`). Access the application in your web browser or with curl:

```
http://<minikube-ip>:<NodePort>
```

To get the Minikube IP:

```bash
minikube ip
```

## Testing the Application

1. **Health Check**:

   Use the following endpoints to verify if the application is live and ready:

   ```bash
   curl http://<minikube-ip>:<NodePort>/health/live
   curl http://<minikube-ip>:<NodePort>/health/ready
   ```

2. **CRUD Operations**:

   Test CRUD operations on the `/items` endpoint:

   - **Create an Item**:

     ```bash
     curl -X POST http://<minikube-ip>:<NodePort>/items -H "Content-Type: application/json" -d '{"name": "Item Name"}'
     ```

   - **Get All Items**:

     ```bash
     curl http://<minikube-ip>:<NodePort>/items
     ```

## Cleanup

To remove all Kubernetes resources created during this setup:

```bash
kubectl delete -f k8s/
```

To stop the Minikube cluster:

```bash
minikube stop
```
