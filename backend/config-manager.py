import yaml

CONFIG_FILE = "/opt/wyoming-satellite-web/config.yaml"

def read_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def write_config(config):
    with open(CONFIG_FILE, "w") as f:
        yaml.safe_dump(config, f)