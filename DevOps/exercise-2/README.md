# Exercise 2: Deploy a Flask App on Minikube

## Objective
Build a Flask container image, deploy it with a Kubernetes Deployment, and expose it through a NodePort Service.

## Environment
Windows PowerShell, Docker Desktop with Linux containers, Minikube using the Docker driver, kubectl, and Git.

## Application and Configuration
- `app.py`: returns `Hello from Flask on Kubernetes!` at `/` and listens on port 15000.
- `Dockerfile`: builds the Python application image.
- `flask-deployment.yaml`: defines Deployment `flask-app` with one replica and NodePort Service `flask-app-service`.
- Image: `flask-app:latest`, loaded into Minikube and used with `imagePullPolicy: Never`.

## Run the Exercise
From the `exercise-2` folder with Docker Desktop running:

```powershell
minikube start --driver=docker
kubectl config use-context minikube
kubectl get nodes
docker build -t flask-app:latest .
minikube image load flask-app:latest
kubectl apply -f flask-deployment.yaml
kubectl rollout status deployment/flask-app --timeout=180s
kubectl get deployment flask-app
kubectl get pods -l app=flask-app
kubectl get service flask-app-service
kubectl logs deployment/flask-app
minikube service flask-app-service --url
```

Open the actual URL returned by Minikube in a browser. Keep the service terminal open if it maintains a tunnel. The expected page displays `Hello from Flask on Kubernetes!`.

Before creating the Service or another access route, `curl.exe --max-time 5 http://127.0.0.1:15000` is expected to fail if nothing else is listening on that Windows port. A container port does not automatically become a localhost port.

## Observed Results
Saved outputs confirm:

| Check | Observed result | Evidence |
| --- | --- | --- |
| Deployment | One ready and available replica | [Deployment status](evidence/deployment-status.txt) |
| Pod | `1/1 Running` | [Pod status](evidence/pod-status.txt) |
| Service | NodePort mapping `15000:32499/TCP` at capture time | [Service status](evidence/service-status.txt) |
| Application | Listening on port 15000; homepage request returned HTTP 200 | [Flask logs](evidence/flask-logs.txt) |

The Flask development-server warning is expected for this learning exercise. The logged `/favicon.ico` 404 means no favicon was provided; the homepage returned successfully.

## Key Learnings
A Deployment manages the application Pod and its desired replica count. The Service selects Pods labelled `app: flask-app` and forwards its port 15000 to container port 15000. The NodePort is a separate assigned port; use Minikube's returned URL for browser access on this Windows setup.

## Optional Cleanup
From the `exercise-2` folder:

```powershell
kubectl delete -f flask-deployment.yaml
minikube stop
```
