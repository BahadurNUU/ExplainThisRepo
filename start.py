import subprocess

# Start FastAPI backend
backend = subprocess.Popen(["uvicorn", "server:app", "--reload"])

# Start React frontend
frontend = subprocess.Popen(["npm", "run", "dev"], cwd="client")

try:
    backend.wait()
    frontend.wait()
except KeyboardInterrupt:
    backend.terminate()
    frontend.terminate()