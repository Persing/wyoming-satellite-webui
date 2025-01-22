import subprocess

def restart_satellite():
    subprocess.run(["systemctl", "restart", "wyoming-satellite"])

def stop_satellite():
    subprocess.run(["systemctl", "stop", "wyoming-satellite"])

def start_satellite():
    subprocess.run(["systemctl", "start", "wyoming-satellite"])