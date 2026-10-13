# Exercise 9: Jenkins Multi-Stage Python Pipeline

## Objective
Build a Flask application, run its unit test, copy it to a mock deployment directory, start the deployed copy, and verify it over HTTP.

## Verified Outcome
Build **#1** of `Python-MultiStage-Pipeline` completed successfully on **18 October 2026**, taking approximately **11 seconds**. The saved console, reports, deployment artifacts, and screenshots confirm all five stages passed.

| Stage | Observed result |
| --- | --- |
| Build | Python 3.13.5 created `.venv`; Flask 3.1.2 and its dependencies installed successfully |
| Test | `test_home` passed; one unit test ran in 0.010 seconds and reported `OK` |
| Deploy | `app.py` and `requirements.txt` were copied to the mock deployment directory and matched the source files |
| Run Application | The deployed application started with PID 1695 |
| Test Application | The live HTTP request returned 200 and the exact expected greeting |
| Post actions | Application PID 1695 was stopped, artifacts were archived, and the build ended with `Finished: SUCCESS` |

Recorded source revision: `c01a5437e1daba0f24a6209abb4ba868122ca231`.

Commit message: `Add multi-stage Flask Jenkins pipeline`.

These are verified results from the saved build evidence, not a live container status check.

## Repositories and Environment
The source files are stored in the root of [Bheema97/devops-sample-code](https://github.com/Bheema97/devops-sample-code) on `main`, alongside the existing `hello-world.sh` from Exercise 8. This `DevOps-Repo/exercise-9` folder stores a reference copy of the source, the exercise report, and saved evidence.

Use the existing jenkins-ci-lab container from Exercise 7 at http://localhost:8080. The job is named Python-MultiStage-Pipeline, type Pipeline, definition Pipeline script from SCM, SCM Git, public repository URL above, branch */main, and script path Jenkinsfile.

## Prepare Jenkins
From Windows PowerShell:

```powershell
docker start jenkins-ci-lab
docker exec -u root jenkins-ci-lab apt-get update
docker exec -u root jenkins-ci-lab apt-get install -y python3 python3-venv python3-pip
docker exec --user jenkins jenkins-ci-lab python3 --version
```

Pipeline support must be installed through Jenkins plugins. Python system packages are installed in the existing container for this lab, while application dependencies are installed by the pipeline into its own virtual environment. System packages survive container stop/start but must be reinstalled if the container is removed and recreated. A custom Jenkins agent image is preferable for repeatable production use.

## Pipeline Stages
| Stage | Work |
| --- | --- |
| Build | Create .venv and install requirements.txt |
| Test | Execute unittest; fail the build if the test fails |
| Deploy | Copy app.py and requirements.txt into WORKSPACE/python-app-deploy and compare the copies |
| Run Application | Start the copied app on container localhost port 5050 with logs and a recorded PID |
| Test Application | Retry an HTTP request until ready and verify status 200 and the exact greeting |

The post action stops this build's app process and archives its deployment files, application log, unit-test output, and HTTP test report. The server runs only for verification; it is not published to the Windows browser and is not a persistent production deployment.

## Corrections to the Supplied Instructions
- The Build stage actually installs dependencies instead of only printing a message.
- Flask is pinned to 3.1.2 rather than the older 2.1.2 requirement.
- The final test queries the running deployed app over HTTP; rerunning Flask's test-client unit test alone would not verify the server.
- The mock deployment path consistently follows the provided pipeline's workspace directory, rather than the contradictory /tmp path in its expected-outcome text.
- The app disables debug mode and the reloader, and post-build cleanup stops it.
- No nested git init or replacement remote is needed because the sample repository already exists.

## Run
Commit these files to the sample repository and push main. Configure the job from SCM as described above, then choose Build Now. The standard SCM checkout loads Jenkinsfile and the app from the same selected revision. This is a manual trigger; no webhook or SCM polling is configured.

## Recorded Test Output
Unit-test report:

```text
test_home (test_app.TestApp.test_home) ... ok
Ran 1 test in 0.010s
OK
```

Live HTTP report:

```text
HTTP smoke test passed: 200 OK
Hello, Jenkins Multi-Stage Pipeline!
```

Final console messages:

```text
Stopped application PID 1695
Archiving artifacts
Pipeline completed successfully!
Finished: SUCCESS
```

## Saved Evidence
| File | What it demonstrates |
| --- | --- |
| [Jenkins console](evidence/jenkins-console-output.txt) | SCM checkout, all five stages, cleanup, artifact archiving, and successful completion |
| [Unit-test report](evidence/unit-test-output.txt) | One passing Flask route test |
| [HTTP-test report](evidence/http-test-output.txt) | Successful request to the running deployed application |
| [Application log](evidence/app.log) | Flask server startup and request logging |
| [Deployed application](evidence/app.py) | Archived application file copied during deployment |
| [Deployed requirements](evidence/requirements.txt) | Archived Flask requirement |
| [Source commit](evidence/source-commit.txt) | Source revision and commit message |
| [Source repository](evidence/source-repository.txt) | GitHub remote used for this exercise |
| [Successful stages](<evidence/Screenshot 2026-10-18 210401.png>) | Green status for checkout, all application stages, and post actions |
| [Build summary and artifacts](<evidence/Screenshot 2026-10-18 210409.png>) | Build #1 success, source revision, duration, and five archived artifacts |

Artifacts were downloaded into the root of `evidence/`; their links above match the actual saved filenames.

### Pipeline Stages
![All pipeline stages successful](<evidence/Screenshot 2026-10-18 210401.png>)

### Build Summary and Archived Artifacts
![Build 1 summary and artifacts](<evidence/Screenshot 2026-10-18 210409.png>)

## Completion Checklist
- [x] Application and Jenkinsfile retrieved from GitHub `main`.
- [x] Build installs dependencies in a virtual environment.
- [x] Unit test passes.
- [x] Deployment copies match the source files.
- [x] The deployed application starts and passes a live HTTP test.
- [x] The application process is stopped after verification.
- [x] Reports, deployment artifacts, console output, and screenshots are saved.
- [x] Jenkins reports `Finished: SUCCESS`.

No credentials or initial Jenkins password belong in the repository.

## Lifecycle
The source repository retains hello-world.sh, so the Exercise 8 HelloWorld job continues to work. This pipeline uses the same Jenkins instance and a separate job workspace. The five stages demonstrate a mock CI/CD workflow, not deployment to a production server.
