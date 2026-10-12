# Exercise 8: Hello World Jenkins Job

## Objective
Create a shell script in a public GitHub repository, configure a Jenkins Freestyle project to check out the repository, and execute the script successfully.

## Environment
- Windows PowerShell for local file creation and Git commands.
- Docker Desktop running the Exercise 7 Jenkins container, `jenkins-ci-lab`.
- Jenkins web interface: http://localhost:8080.
- Shell commands execute inside Jenkins's Linux container.

## Source Repository
- [Public sample repository](https://github.com/Bheema97/devops-sample-code)
- [Script on the main branch](https://github.com/Bheema97/devops-sample-code/blob/main/hello-world.sh)
- Revision used by successful build #1: `2bd528514e3a8c31ee427cc66bb61b4bca8b29c9`.
- Commit message: `Add Hello Jenkins shell script`.

The sample repository supplies the actual Jenkins checkout. This `exercise-8` folder contains a reference copy of the script, documentation, and execution evidence.

## Shell Script
File: [hello-world.sh](hello-world.sh)

```sh
#!/bin/sh
echo 'Hello, Jenkins!'
```

The script was prepared with LF line endings and no UTF-8 byte-order mark. It is invoked with `sh`, so execution does not depend on its executable permission in the Jenkins checkout.

## Jenkins Job Configuration
| Setting | Value |
| --- | --- |
| Job name | `HelloWorld` |
| Job type | Freestyle project |
| Source Code Management | Git |
| Repository URL | `https://github.com/Bheema97/devops-sample-code.git` |
| Checkout credentials | None; the repository is public |
| Branch specifier | `*/main` |
| Build step | Execute shell |
| Shell command | `sh hello-world.sh` |
| Trigger used | Manual, through Build Now |

## Procedure
1. Start Docker Desktop and the existing Jenkins container.
2. Create the public `devops-sample-code` GitHub repository.
3. Create `hello-world.sh`, commit it on `main`, and push it to the sample repository.
4. In Jenkins, create the `HelloWorld` Freestyle project.
5. Configure Git checkout using the repository URL and `*/main`, replacing the default `*/master`.
6. Add an Execute shell step containing `sh hello-world.sh`.
7. Save the configuration and select Build Now.
8. Open build #1 and its Console Output to verify checkout, script output, and final status.

### Useful PowerShell Commands
Start the already-created Jenkins container:

```powershell
docker start jenkins-ci-lab
Start-Process "http://localhost:8080"
```

For subsequent changes to the script in the sample repository:

```powershell
cd "C:\Users\bheem\devops-sample-code"
git add hello-world.sh
git commit -m "Update Hello Jenkins script"
git push origin main
```

Choose Build Now again to execute the updated revision. No webhook or SCM polling trigger was configured as part of this exercise.

## Verified Results
The saved console output and screenshots confirm:

- [x] Jenkins fetched the public sample repository without checkout credentials.
- [x] Jenkins checked out the expected revision from `origin/main`.
- [x] The job executed `sh hello-world.sh`.
- [x] The script printed `Hello, Jenkins!`.
- [x] Build #1 ended with `Finished: SUCCESS`.

Relevant console excerpt:

```text
Checking out Revision 2bd528514e3a8c31ee427cc66bb61b4bca8b29c9 (refs/remotes/origin/main)
Commit message: "Add Hello Jenkins shell script"
+ sh hello-world.sh
Hello, Jenkins!
Finished: SUCCESS
```

Build #1 completed in approximately 4.2 seconds, as shown in the build summary screenshot. These are recorded results, not a live status check.

## Evidence
| File | Contents |
| --- | --- |
| [Console output](evidence/jenkins-console-output.txt) | Git checkout, executed command, greeting, and successful result |
| [Repository URL](evidence/sample-repository-url.txt) | Sample repository remote URL |
| [Repository commit](evidence/sample-repository-commit.txt) | Source commit hash and message |
| [Build #1 summary](<evidence/Screenshot 2026-10-18 200158.png>) | Successful build, source repository, revision, and duration |
| [Stable-build summary](<evidence/Screenshot 2026-10-18 200205.png>) | Build #1 available through the stable-build link |
| [Console screenshot](<evidence/Screenshot 2026-10-18 200213.png>) | Visible greeting and `Finished: SUCCESS` |

### Successful Build
![Successful HelloWorld build](<evidence/Screenshot 2026-10-18 200158.png>)

### Console Output
![Hello Jenkins console output](<evidence/Screenshot 2026-10-18 200213.png>)

## Authentication and Setup Notes
The Exercise 7 setup used Skip and continue as admin, so the existing Jenkins administrator account was reused. Credentials are not included in this repository.

The build log explicitly reports `No credentials specified` for public Git checkout. It does not establish how the local Git push was authenticated. Creation or use of a fine-grained GitHub personal access token is not demonstrated by the saved evidence; this is separate from the verified Jenkins execution result. If a PAT is required for assessment, complete that step separately without including its value in files or screenshots.

## Learning
A Jenkins Freestyle project can retrieve a specific source revision and automate a shell command. Its console output provides feedback and identifies the executed revision. This exercise demonstrates manual initiation of an automated job; it does not demonstrate push-triggered CI, automated application tests, or deployment.

## Stop and Resume Jenkins
```powershell
docker stop jenkins-ci-lab
docker start jenkins-ci-lab
```

The Exercise 7 named volume retains the Jenkins configuration and job data. No additional Jenkins container is needed.
