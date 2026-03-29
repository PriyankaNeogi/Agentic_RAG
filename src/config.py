import yaml
import os


def load_config():
    # Get absolute path to config.yaml
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config.yaml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"config.yaml not found at {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config