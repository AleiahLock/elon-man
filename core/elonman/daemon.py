"""The core service. Owns the body, the bus, the policy and the plugins.

The CLI and the MCP server talk to it over HTTP on 127.0.0.1 only.
"""
import importlib
import json
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import config
from .bus import Bus, tail
from .hal import open_body
from .policy import Policy, PolicyError
from .speech import Speaker


class Core:
    def __init__(self):
        self.policy = Policy(config.POLICY)
        self.bus = Bus(config.EVENTS)
        self.body = open_body(config.get("ELONMAN_PORT", "fake"))
        self.speaker = Speaker(self)
        self.state = {"pan": 0.0, "nod": 0.0, "tilt": 0.0, "mood": "sleep",
                      "started": datetime.now().isoformat(timespec="seconds")}
        self.plugins = {}
        self._body_lock = threading.Lock()

    # ---- body ----
    def set_face(self, mood: str):
        self.policy.check_mood(mood)
        with self._body_lock:
            self.body.face(mood)
        self.state["mood"] = mood

    def look(self, pan: float, nod: float, tilt: float = 0.0, ms: int = 400):
        pan, nod, tilt = self.policy.clamp_look(pan, nod, tilt)
        with self._body_lock:
            self.body.look(pan, nod, tilt, ms)
        self.state.update(pan=pan, nod=nod, tilt=tilt)
        return pan, nod, tilt

    # ---- plugins ----
    def load_plugins(self, names):
        for name in [n.strip() for n in names if n.strip()]:
            if not (config.MANIFESTS / f"{name}.yaml").exists():
                print(f"[core] skip plugin '{name}': no manifest in core/manifests/")
                continue
            try:
                mod = importlib.import_module(f"elonman.plugins.{name}")
                mod.start(self)
                self.plugins[name] = mod
                self.bus.emit("plugin_loaded", name=name)
            except Exception as e:
                print(f"[core] plugin '{name}' failed to start: {e}")
                self.bus.emit("plugin_failed", name=name, error=str(e))

    # ---- commands (CLI + MCP) ----
    def handle(self, req: dict) -> dict:
        cmd = str(req.get("cmd", ""))
        self.policy.check(cmd)

        if cmd == "ping":
            with self._body_lock:
                return {"ok": True, "body": self.body.ping()}

        if cmd == "say":
            text = str(req.get("text", ""))[: self.policy.say_max]
            self.speaker.say(text)
            return {"ok": True, "said": text}

        if cmd == "look":
            if req.get("direction"):
                pan, nod = self.policy.direction(str(req["direction"]))
                tilt = 0.0
            else:
                pan = req.get("pan", self.state["pan"])
                nod = req.get("nod", self.state["nod"])
                tilt = req.get("tilt", self.state["tilt"])
            pan, nod, tilt = self.look(pan, nod, tilt, int(req.get("ms", 400)))
            self.bus.emit("looked", pan=pan, nod=nod, tilt=tilt, by=req.get("by", "cli"))
            return {"ok": True, "pan": pan, "nod": nod, "tilt": tilt}

        if cmd == "face":
            mood = str(req.get("mood", ""))
            self.set_face(mood)
            return {"ok": True, "mood": mood}

        if cmd == "status":
            recent = tail(config.EVENTS, 8)
            return {"ok": True, "state": self.state, "plugins": sorted(self.plugins),
                    "speaking": self.speaker.speaking(),
                    "people_in_view": self.state.get("people", 0),
                    "recent_events": [f"{e['t']} {e['type']}" for e in recent]}

        if cmd == "events":
            n = max(1, min(int(req.get("last", 20)), self.policy.events_max))
            kind = req.get("type")
            evs = tail(config.EVENTS, n * 5 if kind else n)
            if kind:
                evs = [e for e in evs if e["type"] == kind][-n:]
            return {"ok": True, "events": evs}

        if cmd == "snap":
            vision = self.plugins.get("vision")
            if not vision:
                return {"ok": False, "err": "vision plugin not loaded"}
            path = vision.snap(self)
            self.bus.emit("snap_saved", path=str(path))
            # local_only: return a path on this Mac, never the image itself
            return {"ok": True, "saved_locally": str(path), "note": "image stays on this Mac"}

        return {"ok": False, "err": f"no handler for {cmd}"}


def serve():
    core = Core()
    core.bus.emit("core_started", port=config.get("ELONMAN_PORT", "fake"))
    try:
        core.look(0, 0, 0, 600)
        core.set_face("idle")
    except Exception as e:
        print(f"[core] body not answering yet: {e}")
    core.load_plugins(config.get("ELONMAN_PLUGINS", "").split(","))

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path != "/cmd":
                self.send_error(404)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                req = json.loads(self.rfile.read(length) or b"{}")
                out = core.handle(req)
                code = 200
            except PolicyError as e:
                out, code = {"ok": False, "err": str(e), "refused": True}, 403
            except Exception as e:
                out, code = {"ok": False, "err": str(e)}, 500
            body = json.dumps(out, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    srv = ThreadingHTTPServer(config.DAEMON_ADDR, Handler)
    host, port = config.DAEMON_ADDR
    print(f"[core] Elon Man core on http://{host}:{port}  plugins: {sorted(core.plugins) or 'none'}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        core.bus.emit("core_stopped")
        try:
            core.set_face("sleep")
        except Exception:
            pass
        time.sleep(0.2)
