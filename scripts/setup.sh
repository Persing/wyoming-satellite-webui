#!/bin/bash

# Wyoming Satellite Web Installer Script
# This script sets up the web-based configuration portal.

# Exit on error
set -e

# Variables
INSTALL_DIR="/opt/wyoming-satellite-web"
VENV_DIR="$INSTALL_DIR/.venv"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root."
  exit 1
fi

# Create installation directory
echo "Creating installation directory at $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

# Create a systemd service for the web portal
echo "Creating systemd service..."
cat <<EOF > /etc/systemd/system/wyoming-web-portal.service
[Unit]
Description=Wyoming Satellite Web Portal
After=network.target

[Service]
ExecStart=$VENV_DIR/bin/python3 $INSTALL_DIR/backend/app.py
WorkingDirectory=$INSTALL_DIR
Restart=always
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
echo "Enabling and starting the web portal service..."
systemctl daemon-reload
systemctl enable wyoming-web-portal
systemctl start wyoming-web-portal

echo "Installation complete! The web portal is now running."
echo "You can access it at http://<device-ip>:8080"