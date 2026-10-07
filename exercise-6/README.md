# Exercise 6: Real-Time Delivery Monitoring and Alerting

## Objective
Simulate delivery metrics with Python, scrape them with Prometheus, visualize them in Grafana, and use Jenkins to build and start the monitoring stack. Demonstrate alert firing and recovery with controlled simulated load.

## Recorded Results — 18 October 2026
The repository's saved outputs and screenshots demonstrate the following results. These describe the captured run, not a live status check.

| Check | Verified result | Evidence |
| --- | --- | --- |
| Service startup | Metrics, Prometheus, Grafana, and Jenkins were all running | [Container status](evidence/containers.txt) |
| Normal simulation | Current workload 95, pending deliveries 7, and in-transit deliveries 18 in the captured sample | [Normal metrics](evidence/metrics-normal.txt) |
| Prometheus scraping | Both `delivery_service` and `prometheus` targets were UP with no scrape errors | [Target API response](evidence/targets.json) |
| Grafana visualization | Four delivery graphs displayed normal activity, then increased pending counts and delivery duration under high load | Dashboard screenshots below |
| Pending-delivery alert | `HighPendingDeliveries` was firing with severity `warning`; API sample value: 64 | [High-load alerts](evidence/alerts-high-load.json) |
| Delivery-duration alert | `HighAverageDeliveryTime` was firing with severity `critical`; API sample value: approximately 39.79 seconds | [High-load alerts](evidence/alerts-high-load.json) |
| Return toward normal | Latest dashboard capture shows pending counts returning below 10 and the one-minute mean duration falling below 30 seconds | Recovery screenshot below |
| Current source configuration | `delivery_metrics.py` has been restored to `HIGH_LOAD = False` | [Application source](delivery_metrics.py) |

The evidence includes Jenkins setup and its home page, but no build-console output or screenshot confirming `Finished: SUCCESS`. A recovered-alert API response has not been saved, so final alert clearance is not independently documented. Cleanup completion is also not recorded.

## Evidence Screenshots

### Prometheus Target Health
Both scrape targets are UP.

![Prometheus targets UP](<evidence/Screenshot 2026-10-18 190744.png>)

### Normal Delivery Activity
The dashboard shows low pending counts and a mean duration of approximately 20 seconds.

![Grafana normal delivery activity](<evidence/Screenshot 2026-10-18 190948.png>)

### High-Load Alert Evaluation
Prometheus shows both configured alerts firing. Values in screenshots and API snapshots differ because they were captured at different times.

![Prometheus high-load alerts firing](<evidence/Screenshot 2026-10-18 191332.png>)

### High-Load Dashboard
Pending counts rise into the simulated 50–100 range, while the mean delivery duration rises to approximately 40 seconds.

![Grafana high-load delivery activity](<evidence/Screenshot 2026-10-18 191421.png>)

### Recovery Trend
Pending counts return below the threshold, and the duration graph falls below 30 seconds at the end of this capture. The alert-status panels are below the visible area, so this image is evidence of metric recovery rather than final alert-state confirmation.

![Grafana recovery toward normal](<evidence/Screenshot 2026-10-18 191759.png>)

### Jenkins Setup Evidence
- [Plugin installation](<evidence/Screenshot 2026-10-18 185021.png>)
- [Initial administrator setup screen](<evidence/Screenshot 2026-10-18 185434.png>)
- [Setup completion](<evidence/Screenshot 2026-10-18 185450.png>) — this run skipped creating a separate administrator account.
- [Jenkins home page](<evidence/Screenshot 2026-10-18 185456.png>)

## Requirements
Windows PowerShell and Docker Desktop running Linux containers, including Docker Compose. Python, Jenkins, Prometheus, and Grafana run in containers; host installations are not needed.

## Design
All services use the Compose network `exercise6_default`. Prometheus scrapes `metrics:8000`, and Grafana queries `http://prometheus:9090`. Container names replace platform-specific host IP addresses. Configuration is copied into images to avoid Docker host versus Jenkins workspace bind-mount path mismatches.

| Service | Browser URL |
| --- | --- |
| Python metrics | http://localhost:8000/metrics |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Jenkins | http://localhost:8081 |

Jenkins uses Docker CLI and Compose through the Docker socket. It runs as root for this local lab and can control the Docker engine. Only run trusted pipeline code. Web ports are published on localhost. This is a learning configuration, not a production Jenkins deployment.

## Start Jenkins
Run from this folder with Docker Desktop running:

```powershell
docker version
docker compose version
docker compose -p exercise6 config --quiet
docker compose -p exercise6 up -d --build jenkins
docker compose -p exercise6 logs --tail 30 jenkins
docker compose -p exercise6 exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Use the displayed password only to unlock http://localhost:8081. Do not save it in evidence. Install suggested plugins, create an administrator, and finish setup. The image also includes Pipeline support and Docker CLI/Compose.

Create a Pipeline job named `delivery-monitoring`. Select `Pipeline script`, paste the complete contents of `Jenkinsfile`, save, and choose Build Now. Its stages validate configuration, build three monitoring images, check Prometheus rules, start the services, and verify the delivery scrape target is UP. The source is read from the read-only `/lab` mount of this folder, so rebuilding uses current local files. This is a local pipeline, not an SCM checkout or automatic Git-triggered job.

## Verify Monitoring
```powershell
docker compose -p exercise6 ps
curl.exe --fail http://localhost:8000/metrics
Invoke-RestMethod http://localhost:9090/api/v1/targets | ConvertTo-Json -Depth 12
```

Check http://localhost:9090/targets: both jobs should be UP. At http://localhost:3000, initial Grafana credentials for a fresh volume are `admin` / `admin`; set a new password when prompted. Open Dashboards > Delivery Monitoring > Delivery Operations. The Prometheus data source and six panels are provisioned automatically.

The four delivery panels show current total workload, pending deliveries, deliveries in transit, and the one-minute mean delivery duration. The final two panels show Prometheus firing-alert status (1 means firing; 0 means not firing). These are not separately managed Grafana alert rules.

## Simulate High Load
The default `HIGH_LOAD = False` generates pending counts from 5 to 9 and durations from 15 to 25 seconds. Switch modes from PowerShell:

```powershell
(Get-Content -Raw delivery_metrics.py).Replace('HIGH_LOAD = False', 'HIGH_LOAD = True') | Set-Content -Encoding utf8 delivery_metrics.py
```

Choose Build Now in Jenkins again. High-load mode generates pending counts from 50 to 100 and durations from 35 to 45 seconds. Within approximately one to two minutes, check http://localhost:9090/alerts and the Grafana alert-status panels.

| Alert | Condition | Sustained period | Severity |
| --- | --- | --- | --- |
| HighPendingDeliveries | Pending deliveries > 10 | 15 seconds | warning |
| HighAverageDeliveryTime | One-minute mean duration > 30 seconds | 15 seconds | critical |

The pending state precedes firing. Scrape/evaluation timing and the averaging window affect the exact delay. This exercise evaluates alerts and displays their states; it does not send email or messages because no Alertmanager receiver/contact point is configured.

## Capture Evidence on a New Run
The `evidence/` folder already contains the outputs linked above and nine screenshots. The following commands are for a new run; avoid replacing the existing normal/high-load captures unless intentionally recording fresh results. Capture normal metrics while normal mode is active, and the alert response only while high-load alerts are firing.

```powershell
New-Item -ItemType Directory -Force evidence
docker compose -p exercise6 ps | Set-Content -Encoding utf8 evidence\containers.txt
curl.exe --fail --silent --show-error http://localhost:8000/metrics | Set-Content -Encoding utf8 evidence\metrics-normal.txt
Invoke-RestMethod http://localhost:9090/api/v1/targets | ConvertTo-Json -Depth 12 | Set-Content -Encoding utf8 evidence\targets.json
Invoke-RestMethod http://localhost:9090/api/v1/alerts | ConvertTo-Json -Depth 12 | Set-Content -Encoding utf8 evidence\alerts-high-load.json
```

The dashboard and firing-alert screenshots are already present and embedded above. To finish the evidence record, save the successful Jenkins build console or screenshot showing `Finished: SUCCESS`. Do not include passwords or Jenkins unlock tokens.

## Restore Normal Load
```powershell
(Get-Content -Raw delivery_metrics.py).Replace('HIGH_LOAD = True', 'HIGH_LOAD = False') | Set-Content -Encoding utf8 delivery_metrics.py
```

The source has already been restored to normal mode, and the latest dashboard screenshot shows metrics falling below the thresholds. On a repeat run, run the Jenkins job after changing the source and wait for the averaging window to settle. To explicitly document final alert clearance, check the alerts page and save:

```powershell
Invoke-RestMethod http://localhost:9090/api/v1/alerts | ConvertTo-Json -Depth 12 | Set-Content -Encoding utf8 evidence\alerts-recovered.json
```

## Corrections to the Original Instructions
- Supplies the missing application Dockerfile and Docker tools required inside Jenkins.
- Uses consistent `prometheus.yml` and `alert_rules.yml` filenames.
- Uses shared Docker networking rather than Linux host networking/IP addresses.
- Provisions Grafana's data source and dashboard automatically.
- Provides normal and high-load modes, so both alerts can be demonstrated reliably.
- Adds `for: 15s` to both rules and uses a one-minute duration mean rather than a process-lifetime mean.
- Python's Summary exposes sum and count; the Python client does not calculate Summary quantiles.
- The metric `total_deliveries` is retained from the exercise as a gauge of current workload, not a cumulative completed-delivery counter.

## Troubleshooting
Use `docker compose -p exercise6 logs --tail 50 SERVICE` with `metrics`, `prometheus`, `grafana`, or `jenkins`. If a host port is occupied, stop the conflicting lab service or update the host-side port in `compose.yaml` and use that URL. A successful configuration check is silent. If Grafana requests credentials after restarting, use the password saved during its first setup; named volumes persist accounts.

## Cleanup
```powershell
docker compose -p exercise6 down
```

This removes this project's containers and network while retaining named volumes for Jenkins, Grafana, and Prometheus. Do not add `--volumes` unless you intentionally want to delete their saved data.

## Git Submission
From the repository root:

```powershell
git add exercise-6
git --no-pager diff --cached --stat
git --no-pager diff --cached
git commit -m "Complete exercise 6: delivery monitoring and alerting pipeline"
git push
```

Base service images use upstream moving tags for this lab. Pin tested versions or digests if fixed reproducibility is required.
