import pytest

from elonman import config
from elonman.bus import Bus, tail
from elonman.daemon import Core
from elonman.policy import Policy, PolicyError


def test_policy_refuses_unlisted_command():
    p = Policy(config.POLICY)
    with pytest.raises(PolicyError):
        p.check("shell")
    p.check("status")


def test_angles_are_clamped():
    p = Policy(config.POLICY)
    pan, nod, tilt = p.clamp_look(500, -500, 0)
    assert (pan, nod, tilt) == (60, -20, 0)


def test_bus_logs_every_event(tmp_path):
    bus = Bus(tmp_path / "events.jsonl")
    seen = []
    bus.on("person_entered", seen.append)
    bus.emit("person_entered", count=1)
    bus.emit("office_empty")
    assert len(seen) == 1
    assert [e["type"] for e in tail(tmp_path / "events.jsonl")] == ["person_entered", "office_empty"]


def test_core_with_fake_body(monkeypatch, tmp_path):
    monkeypatch.setenv("ELONMAN_PORT", "fake")
    monkeypatch.setattr(config, "EVENTS", tmp_path / "events.jsonl")
    core = Core()
    assert core.handle({"cmd": "look", "direction": "left"})["pan"] == 40
    assert core.handle({"cmd": "look", "pan": 99})["pan"] == 60
    with pytest.raises(PolicyError):
        core.handle({"cmd": "face", "mood": "angry"})
    with pytest.raises(PolicyError):
        core.handle({"cmd": "rm"})
