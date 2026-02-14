import subprocess
import sys
import os
import time

def run_services():
    # Paths
    root_dir = os.getcwd()
    frontend_dir = os.path.join(root_dir, "frontend")

    print(f"Root: {root_dir}")
    print(f"Frontend: {frontend_dir}")

    # Start Backend
    print("🚀 Starting Backend (FastAPI)...")
    backend_cmd = [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
    backend_process = subprocess.Popen(backend_cmd, cwd=root_dir)

    # Start Frontend
    print("🚀 Starting Frontend (Vite)...")
    # shell=True required for npm on Windows, but be careful with PIDs
    frontend_process = subprocess.Popen(["npm", "run", "dev"], cwd=frontend_dir, shell=True)

    print("\n✅ Services are running!")
    print("Backend: http://127.0.0.1:8000")
    print("Frontend: http://localhost:5173")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Terminate Backend
        backend_process.terminate()
        
        # Terminate Frontend
        # On Windows, terminating the shell doesn't always kill the child (npm/vite)
        if sys.platform == "win32":
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(frontend_process.pid)])
        else:
            frontend_process.terminate()
            
        backend_process.wait()
        # frontend_process.wait()
        print("Services stopped.")

if __name__ == "__main__":
    run_services()
