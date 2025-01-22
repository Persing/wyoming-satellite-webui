import subprocess

def restart_wakeword_service():
    subprocess.run(["systemctl", "restart", "wyoming-openwakeword"])

def stop_wakeword_service():
    subprocess.run(["systemctl", "stop", "wyoming-openwakeword"])

def start_wakeword_service():
    subprocess.run(["systemctl", "start", "wyoming-openwakeword"])