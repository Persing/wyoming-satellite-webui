from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import subprocess
import os

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

# Configuration file path
CONFIG_FILE = "config.yaml"

@app.route("/")
def index():
    # Load current configuration
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                key, value = line.strip().split(": ", 1)
                config[key] = value
    return render_template("index.html", config=config)

@app.route("/configure", methods=["POST"])
def configure():
    # Save settings to config file
    config = {
        "wake_word": request.form.get("wake_word"),
        "mic_gain": request.form.get("mic_gain"),
        "noise_suppression": request.form.get("noise_suppression"),
        "wake_uri": request.form.get("wake_uri"),
        "mic_command": request.form.get("mic_command"),
        "snd_command": request.form.get("snd_command"),
    }
    with open(CONFIG_FILE, "w") as f:
        for key, value in config.items():
            f.write(f"{key}: {value}\n")

    # Restart the Wyoming Satellite service (mock)
    print("Mock: Restarting Wyoming Satellite service...")
    return redirect(url_for("index"))

@app.route("/run_setup")
def run_setup():
    # Stream the output of the setup script
    def generate():
        process = subprocess.Popen(
            ["./scripts/setup.sh"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        for line in iter(process.stdout.readline, ""):
            yield f"data: {line}\n\n"
        process.stdout.close()
        process.wait()

    return Response(generate(), mimetype="text/event-stream")

@app.route("/status")
def status():
    # Check the status of services
    def get_service_status(service_name):
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
        except Exception as e:
            return f"error: {str(e)}"

    return jsonify({
        "wyoming_satellite": get_service_status("wyoming-satellite"),
        "wake_word_service": get_service_status("wyoming-openwakeword"),
        "web_portal": get_service_status("wyoming-web-portal"),
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)