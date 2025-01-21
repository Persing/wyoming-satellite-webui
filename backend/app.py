from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os

app = Flask(__name__)

# Configuration file path
CONFIG_FILE = "/opt/wyoming-satellite-web/config.yaml"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/configure", methods=["POST"])
def configure():
    wake_word = request.form.get("wake_word")
    mic_gain = request.form.get("mic_gain")
    noise_suppression = request.form.get("noise_suppression")

    # Save settings to config file
    with open(CONFIG_FILE, "w") as f:
        f.write(f"wake_word: {wake_word}\n")
        f.write(f"mic_gain: {mic_gain}\n")
        f.write(f"noise_suppression: {noise_suppression}\n")

    # Restart the Wyoming Satellite service
    subprocess.run(["systemctl", "restart", "wyoming-satellite"])
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)