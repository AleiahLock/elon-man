"""Paths and settings. Reads core/.env (or ~/.elonman/.env)."""
import os
from pathlib import Path

from dotenv import load_dotenv

CORE_DIR = Path(__file__).resolve().parents[1]          # .../core
HOME = Path(os.environ.get("ELONMAN_HOME", Path.home() / ".elonman"))
HOME.mkdir(parents=True, exist_ok=True)
EVENTS = HOME / "events.jsonl"
SNAPS = HOME / "snaps"
POLICY = CORE_DIR / "policy.yaml"
MANIFESTS = CORE_DIR / "manifests"
DAEMON_ADDR = ("127.0.0.1", int(os.environ.get("ELONMAN_DAEMON_PORT", "8765")))

for env in (CORE_DIR / ".env", HOME / ".env"):
    if env.exists():
        load_dotenv(env, override=False)


def get(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def get_int(name: str, default: int) -> int:
    try:
        return int(get(name, str(default)))
    except ValueError:
        return default


def get_float(name: str, default: float) -> float:
    try:
        return float(get(name, str(default)))
    except ValueError:
        return default
