import subprocess
import os

scripts_dir = "scripts"
scripts = [f for f in os.listdir(scripts_dir) if f.endswith(".py")]

print(f"Starting {len(scripts)} scripts...")

processes = []
for script in scripts:
    path = os.path.join(scripts_dir, script)
    print(f"Launching {script}...")
    p = subprocess.Popen(["python", path])
    processes.append(p)

try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("Shutting down all scripts...")
    for p in processes:
        p.terminate()
