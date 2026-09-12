# Exercise 3: Scaling a Flask App with a ReplicaSet

## Objective
Deploy a simulated flash-sale Flask application on a single-node Minikube cluster, scale it from three to five Pods, and observe automatic Pod replacement after deleting one Pod.

## Environment and Configuration
- Windows PowerShell and Docker Desktop with Linux containers
- Minikube using the Docker driver; kubectl for cluster management
- Application file: `app.py`
- Image: `flashsale:1.0`, built locally and loaded into Minikube
- ReplicaSet: `flashsale-rs`
- Service: `flashsale-svc` (`ClusterIP`, port 80 to container port 5000)
- Gunicorn serves the Flask application with one worker and two threads.
- Readiness and liveness probes use `/health`.
- Each Pod requests 100m CPU and 128Mi memory, with limits of 500m CPU and 256Mi memory.

## Application Endpoints
| Path | Purpose |
| --- | --- |
| `/` | Welcome message, Pod hostname, and timestamp |
| `/buy?user=bheem` | Simulated purchase with a random product and serving Pod hostname |
| `/health` | Health status and Pod hostname |

Purchases are simulated and are not stored.

## Commands Used
Run from the `exercise-3` folder in PowerShell. Docker Desktop must be running.

### Start the Cluster and Build the Image
```powershell
minikube start --driver=docker --nodes=1
kubectl config use-context minikube
kubectl get nodes
docker build -t flashsale:1.0 .
minikube image load flashsale:1.0
```

The YAML uses `imagePullPolicy: Never` to run the locally loaded image.

### Deploy Three Replicas
```powershell
kubectl apply -f flashsale-replicaset.yaml
kubectl wait --for=condition=Ready pod -l app=flashsale --timeout=180s
kubectl get rs flashsale-rs
kubectl get pods -l app=flashsale -o wide
kubectl get service flashsale-svc
```

### Access the Application
```powershell
kubectl port-forward service/flashsale-svc 8080:80
```

Keep the terminal open and visit `http://localhost:8080/`, `http://localhost:8080/buy?user=bheem`, or `http://localhost:8080/health`. Stop forwarding with Ctrl+C. If the selected Pod is deleted, restart port forwarding.

### Scale to Five Replicas
In a second PowerShell window:

```powershell
kubectl scale rs flashsale-rs --replicas=5
kubectl get pods -l app=flashsale -w
```

Once five Pods show `1/1 Running`, stop watching with Ctrl+C and check:

```powershell
kubectl get rs flashsale-rs
kubectl get pods -l app=flashsale -o wide
```

### Delete One Pod and Observe Replacement
```powershell
$podToDelete = kubectl get pods -l app=flashsale -o jsonpath='{.items[0].metadata.name}'
$podToDelete
kubectl delete pod $podToDelete
kubectl get pods -l app=flashsale -w
```

Once five Pods are ready again, press Ctrl+C. Inspect the final state:

```powershell
kubectl get pods -l app=flashsale -o wide
kubectl describe rs flashsale-rs
kubectl logs -l app=flashsale --tail=20 --prefix=true
```

## Observed Results
The saved command outputs confirm:

| Stage | Result | Evidence |
| --- | --- | --- |
| Initial deployment | Desired, current, and ready counts were all 3 | [ReplicaSet](evidence/initial-replicaset.txt), [Pods](evidence/initial-pods.txt) |
| Scaling | Desired, current, and ready counts increased to 5 | [ReplicaSet](evidence/scaled-replicaset.txt), [Pods](evidence/scaled-pods.txt) |
| Pod replacement | `flashsale-rs-2rhp8` disappeared and `flashsale-rs-rwtg2` appeared; five Pods were ready afterward | [Before deletion](evidence/before-deletion.txt), [After replacement](evidence/after-replacement.txt) |
| Node placement | All five Pods ran on the single node named `minikube` | [Final Pod placement](evidence/after-replacement.txt) |

The optional request-distribution test (Step 12) was skipped. No load-balancing or performance-test results are claimed.

## Key Learnings
- A ReplicaSet maintains the desired number of Pods by creating or removing Pods as needed.
- Scaling from three to five replicas creates two additional Pods.
- Deleting one managed Pod triggers creation of a replacement to restore the desired count.
- Multiple Pods on one node demonstrate replication but do not protect against failure of that node.
- Scaling here is manual; traffic-based automatic scaling requires additional configuration.
- Port forwarding selects one Pod and does not demonstrate request distribution across all replicas.

## Configuration Note
The YAML retains `replicas: 3` as the starting configuration. The live ReplicaSet was scaled to five with `kubectl scale`; reapplying the YAML can return it to three.

## Optional Cleanup
From the `exercise-3` folder, after saving evidence:

```powershell
kubectl delete -f flashsale-replicaset.yaml
minikube stop
```
