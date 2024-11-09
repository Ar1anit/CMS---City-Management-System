import tkinter as tk
import subprocess

root = tk.Tk()
root.title("File-Watcher")
root.geometry("250x100")

label = tk.Label(root, text="File-Watcher is listening. Press F7 to restart")
label.pack()

def action():
    subprocess.run(["docker", "rm", "-f", "backend"])
    #subprocess.run(["docker", "rm", "-f", "db"])
    subprocess.run(["docker", "rmi", "gruppe-b/flask_application:latest"])

    # Start that baddie
    subprocess.run(["docker", "build", "-t", "gruppe-b/flask_application:latest", "."])
    subprocess.run(["docker-compose", "up", "-d"])


button = tk.Button(root, text="Restart the container", command=action, width=250, height=50)
button.pack()

root.attributes("-topmost", True)

root.mainloop()
