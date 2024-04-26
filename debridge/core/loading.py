import json
from pathlib import Path
from typing import Any

LOAD_DIR = Path(__file__).parent.parent.parent


def load_config_payload() -> dict[str, Any]:
    path = LOAD_DIR / "config.json"
    content = path.read_text()
    return json.loads(content)


def load_wallets() -> list[str]:
    path = LOAD_DIR / "wallets.txt"
    content = path.read_text()
    return content.splitlines()


def load_proxies() -> list[str]:
    path = LOAD_DIR / "proxies.txt"
    try:
        content = path.read_text()
        return content.splitlines()
    except FileNotFoundError:
        return []
