import os
import time
import atexit
import subprocess

def exit_handler():
    print("###   Stopping Docker   ###")
    subprocess.run(["docker", "kill", "db"])
    subprocess.run(["docker", "kill", "backend"])
    print("###       Stopped       ###")

atexit.register(exit_handler)

print("### Files on watchlist: ###")

# Restarts docker compose.
files = [filename for filename in os.listdir("backend") if os.path.isfile(os.path.join("backend", filename))]
print(str(files)[1:-1])

last_modified_time = [os.path.getmtime(os.path.join("backend", x)) for x in files]

while True:
    for file_num in range(0, len(files)):
        current_modified_time = os.path.getmtime(os.path.join("backend", files[file_num]))
        if current_modified_time != last_modified_time[file_num]:
            print("###  Changes  detected  ###")
            print("###  Restarting Docker  ###")

            # Stop that ass
            subprocess.run(["docker", "rm", "-f", "backend"])
            subprocess.run(["docker", "rm", "-f", "db"])
            subprocess.run(["docker", "rmi", "gruppe-b/flask_application:latest"])

            # Start that baddie
            subprocess.run(["docker", "build", "-t", "gruppe-b/flask_application:latest", "."])
            subprocess.run(["docker-compose", "up", "-d"])
            last_modified_time[file_num] = current_modified_time

    time.sleep(.05)
