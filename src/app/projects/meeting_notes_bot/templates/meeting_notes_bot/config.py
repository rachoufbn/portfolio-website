import yaml
from pathlib import Path

_config_path = Path(__file__).resolve().parent.parent / "config.yml"
_config = None

def get_config(key: str):

    global _config

    if _config is None:
        _config = _load_config()

    value = _config.get(key)

    if not value:
        raise Exception(f"{key} is missing in configuration")
    
    return value

def _load_config():

    with _config_path.open("r", encoding="utf-8") as config_file:
        return yaml.safe_load(config_file) or {}