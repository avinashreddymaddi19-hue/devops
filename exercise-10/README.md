# Exercise 10: Multi-Node Kubernetes with Two Applications

## Objective
Run two Flask services on a three-node Minikube cluster: Product Catalog with two replicas and Shopping Cart with three replicas. Verify that replicas of each app occupy different nodes and test both APIs.

## Verified Results — 18 October 2026
The saved evidence confirms successful deployment and API operation. These results describe the captured run, not a live cluster status check.

| Requirement | Observed result | Evidence |
| --- | --- | --- |
| Three-node cluster | All three nodes Ready, running Kubernetes v1.37.0 | [Nodes](evidence/nodes.txt) |
| Product Catalog deployment | 2/2 replicas ready and available | [Deployments](evidence/deployments.txt) |
| Shopping Cart deployment | 3/3 replicas ready and available | [Deployments](evidence/deployments.txt) |
| Deployment-managed ReplicaSets | Product Catalog: desired/current/ready 2; Shopping Cart: desired/current/ready 3 | [ReplicaSets](evidence/replicasets.txt) |
| Pod placement | Five Pods were 1/1 Running, with zero restarts; replicas of each application occupied different nodes | [Pod distribution](evidence/pod-distribution.txt) |
| Services | Both applications exposed through NodePort Services | [Services](evidence/services.txt) |
| Product list | GET /products returned Laptop, Phone, and Headphones | [Product response](evidence/products-response.json) |
| Initial cart | GET /cart returned an empty array | [Initial cart](evidence/cart-initial.json) |
| Add-to-cart request | POST /cart returned the Laptop item with quantity 1 and status 201 | [Response](evidence/cart-post-response.json), [Status](evidence/cart-post-status.txt) |

### Recorded Pod Placement
| Node | Product Catalog Pod | Shopping Cart Pod |
| --- | --- | --- |
| devops-multinode | None | shopping-cart-6fbf7c85cd-xkcw2 |
| devops-multinode-m02 | product-catalog-76b57bff88-4wnf4 | shopping-cart-6fbf7c85cd-nl72b |
| devops-multinode-m03 | product-catalog-76b57bff88-pnk4f | shopping-cart-6fbf7c85cd-t58xk |

The two Product Catalog replicas occupied two different nodes. The three Shopping Cart replicas occupied all three nodes, satisfying the per-application anti-affinity requirement.

### Recorded Service Ports
| Service | Cluster IP | Service port | NodePort |
| --- | --- | --- | --- |
| product-catalog-service | 10.101.121.202 | 80 | 30658 |
| shopping-cart-service | 10.100.167.203 | 80 | 30310 |

Cluster IPs, NodePorts, Pod names, and tunnel URLs may change on a later run. Use the current URL printed by Minikube for browser access.

### API Results
GET /products:

```json
[
  {"id": 1, "name": "Laptop", "price": 1200},
  {"id": 2, "name": "Phone", "price": 800},
  {"id": 3, "name": "Headphones", "price": 150}
]
```

Initial GET /cart:

```json
[]
```

POST /cart returned HTTP 201:

```json
[{"id": 1, "name": "Laptop", "quantity": 1}]
```

## Environment
Windows PowerShell, Docker Desktop with Linux containers, Minikube, and kubectl. Jenkins is not needed. Use the independent Minikube profile devops-multinode, and namespace default for both Deployments and both Services.

## Application Files
| File | Purpose |
| --- | --- |
| product_catalog.py | GET /products returns three products |
| shopping_cart.py | GET /cart and POST /cart implement an in-memory cart |
| Dockerfile.product | Build Product Catalog image |
| Dockerfile.shopping | Build Shopping Cart image |
| requirements.txt | Flask 3.1.2 |
| product_catalog_deployment.yaml | Two Product Catalog replicas |
| shopping_cart_deployment.yaml | Three Shopping Cart replicas |
| product_catalog_service.yaml | Product Catalog NodePort Service |
| shopping_cart_service.yaml | Shopping Cart NodePort Service |

## Cluster and Image Setup
Run from this exercise folder with Docker Desktop running:

```powershell
minikube start --driver=docker --nodes=3 -p devops-multinode
kubectl config use-context devops-multinode
kubectl config set-context --current --namespace=default
kubectl get nodes
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
```

The images are loaded into the cluster's node runtimes. This is not a registry push; the registry add-on is unnecessary for this local-load approach. imagePullPolicy: Never prevents registry pulls for the app images. The separate profile avoids deleting earlier clusters.

## Deploy and Verify
```powershell
kubectl apply -f product_catalog_deployment.yaml
kubectl apply -f shopping_cart_deployment.yaml
kubectl apply -f product_catalog_service.yaml
kubectl apply -f shopping_cart_service.yaml
kubectl rollout status deployment/product-catalog --timeout=180s
kubectl rollout status deployment/shopping-cart --timeout=180s
kubectl get deployments
kubectl get replicasets
kubectl get pods -o wide
kubectl get services
```

Expected: three Ready nodes, Product Catalog 2/2 ready, Shopping Cart 3/3 ready, and five running app Pods. Required Pod anti-affinity on kubernetes.io/hostname prevents two replicas of the same application being scheduled on one node. Pods from different apps may share a node. A Deployment manages a ReplicaSet; these manifests do not create standalone ReplicaSets.

## Service Access
Run each command in a separate PowerShell window and leave its tunnel open:

```powershell
minikube -p devops-multinode service product-catalog-service --url
```

```powershell
minikube -p devops-multinode service shopping-cart-service --url
```

Append /products or /cart to the respective printed localhost URL. The root paths are not defined.

## API Checks
In a third PowerShell window, enter the actual base URLs from the two tunnels:

```powershell
$catalogUrl = (Read-Host "Product Catalog base URL").TrimEnd('/')
$cartUrl = (Read-Host "Shopping Cart base URL").TrimEnd('/')
Invoke-RestMethod -Uri "$catalogUrl/products"
Invoke-RestMethod -Uri "$cartUrl/cart"
$item = @{ id = 1; name = 'Laptop'; quantity = 1 } | ConvertTo-Json
Invoke-RestMethod -Uri "$cartUrl/cart" -Method Post -ContentType 'application/json' -Body $item
```

Expected: three products, an initially empty cart on a fresh replica, and a POST response containing the Laptop item with HTTP 201.

## Limitations
Each cart Pod stores its own list in memory. Requests routed to different replicas can see different carts; restarts erase a Pod's data. This lab demonstrates scheduling, replicated processes, and API access, not shared persistent cart state or production-grade availability. All nodes run on the same Windows machine. There is one control plane, and host failure still takes down the cluster. Required anti-affinity can leave replacement cart Pods Pending when fewer than three eligible nodes are available. No node-failure test is claimed.

## Evidence and Results
Nine command-output and API-response evidence files are saved and linked in the verified-results section. No screenshots were present in the evidence folder when this README was updated. The saved text and JSON files establish the recorded results; screenshots can be added as supplementary evidence.

## Completion Checklist
- [x] Three Kubernetes nodes recorded as Ready.
- [x] Product Catalog has two ready replicas.
- [x] Shopping Cart has three ready replicas.
- [x] Each application's replicas run on distinct nodes.
- [x] Both NodePort Services are created.
- [x] Product list retrieval succeeds.
- [x] Initial cart is empty and adding an item returns HTTP 201.
- [x] Configuration and API results are saved as evidence.

Stopping or deleting the cluster is optional cleanup and is not demonstrated by the saved evidence. Git commit and push status are not established by these evidence files.

## Troubleshooting
For a Pending Pod, run kubectl describe pod POD_NAME and inspect scheduling events. Three shopping-cart replicas require three eligible nodes due to strict anti-affinity. For image errors, reload both app images into the devops-multinode profile before retrying. Verify that kubectl config current-context shows devops-multinode.

## Stop the Cluster
Close the service tunnels with Ctrl+C, then:

```powershell
minikube stop -p devops-multinode
```

Restart it later with the same profile. Do not delete the profile unless intentionally discarding the cluster.
