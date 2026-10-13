"""Manage and verify the mock-deployed application inside Jenkins."""
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time
from urllib.request import urlopen

deploy = Path("python-app-deploy").resolve()
pid_file = deploy / "app.pid"
app_path = deploy / "app.py"
expected = "Hello, Jenkins Multi-Stage Pipeline!"

def start():
    # Fail clearly if another application owns this lab port.
    with socket.socket() as check:
        check.bind(("127.0.0.1", 5050))
    env = os.environ.copy()
    env["JENKINS_NODE_COOKIE"] = "exercise9-mock-app"
    with (deploy / "app.log").open("ab") as log:
        proc = subprocess.Popen(
            [sys.executable, str(app_path)],
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=env,
            start_new_session=True,
        )
    pid_file.write_text(str(proc.pid), encoding="ascii")
    print(f"Started deployed application: PID {proc.pid}", flush=True)

def test():
    last_error = None
    for _ in range(30):
        try:
            with urlopen("http://127.0.0.1:5050/", timeout=2) as response:
                body = response.read().decode("utf-8")
                if response.status != 200 or body != expected:
                    raise AssertionError(f"Unexpected HTTP response: {body}")
            report = f"HTTP smoke test passed: 200 OK\n{body}\n"
            Path("http-test-output.txt").write_text(report, encoding="utf-8")
            print(report, end="")
            return
        except OSError as exc:
            last_error = exc
            time.sleep(0.5)
    if (deploy / "app.log").exists():
        print((deploy / "app.log").read_text(errors="replace"))
    raise RuntimeError(f"Application did not become ready: {last_error}")

def stop():
    if not pid_file.exists():
        return
    pid = int(pid_file.read_text())
    cmdline = Path(f"/proc/{pid}/cmdline")
    if cmdline.exists() and str(app_path).encode() in cmdline.read_bytes().split(b"\x00"):
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Stopped application PID {pid}")
        except ProcessLookupError:
            pass
    pid_file.unlink(missing_ok=True)

if __name__ == "__main__":
    {"start": start, "test": test, "stop": stop}[sys.argv[1]]()
