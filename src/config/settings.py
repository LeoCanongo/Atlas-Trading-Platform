import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
settings_file = project_root / "config" / "settings.json"


def load_settings():
    with open(settings_file, "r") as f:
        return json.load(f)


def save_settings(settings):
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=4)


SETTINGS = load_settings()