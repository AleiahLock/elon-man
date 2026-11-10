"""The permission registry. Tools never decide on their own whether they're allowed."""
from pathlib import Path

import yaml


class PolicyError(PermissionError):
    pass


class Policy:
    def __init__(self, path: Path):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        cli = data.get("cli", {})
        self.allowed = set(cli.get("allowed", []))
        self.local_only = set(cli.get("local_only", []))
        lim = data.get("limits", {})
        self.pan = tuple(lim.get("pan", [-60, 60]))
        self.nod = tuple(lim.get("nod", [-20, 25]))
        self.tilt = tuple(lim.get("tilt", [-20, 20]))
        self.say_max = int(lim.get("say_max_chars", 400))
        self.events_max = int(lim.get("events_max", 200))
        self.directions = {k: tuple(v) for k, v in data.get("directions", {}).items()}
        self.moods = set(data.get("moods", []))
        self.always_ask = list(data.get("always_ask", []))

    def check(self, cmd: str):
        if cmd not in self.allowed:
            raise PolicyError(f"'{cmd}' is not in policy.yaml cli.allowed")

    @staticmethod
    def _clamp(v, rng):
        lo, hi = rng
        return max(lo, min(hi, float(v)))

    def clamp_look(self, pan, nod, tilt):
        return self._clamp(pan, self.pan), self._clamp(nod, self.nod), self._clamp(tilt, self.tilt)

    def direction(self, name: str):
        if name not in self.directions:
            raise PolicyError(f"unknown direction '{name}', use one of {sorted(self.directions)}")
        return self.directions[name]

    def check_mood(self, mood: str):
        if mood not in self.moods:
            raise PolicyError(f"unknown mood '{mood}', use one of {sorted(self.moods)}")
