"""The elonman command. This is what Grok Bot runs on your Mac (local execution).

  elonman daemon                      start the core (keep it running)
  elonman status                      what he sees and what he's doing
  elonman say "text"                  speak out loud
  elonman look left|right|center|up|down
  elonman look --pan 20 --nod 5       exact angles (clamped by policy.yaml)
  elonman face sleep|idle|listen|think|talk|happy|alert
  elonman events --last 20 [--type person_entered]
  elonman snap                        save a camera frame on this Mac, prints the path
  elonman ping                        check the body over USB
  elonman mcp                         start the MCP server for Grok Bot (Way 2)
"""
import argparse
import json
import sys
import urllib.error
import urllib.request

from . import config


def call(payload: dict) -> dict:
    host, port = config.DAEMON_ADDR
    req = urllib.request.Request(f"http://{host}:{port}/cmd", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b'{"ok":false}')
    except urllib.error.URLError:
        return {"ok": False, "err": "core is not running. Start it with: elonman daemon"}


def main(argv=None):
    p = argparse.ArgumentParser(prog="elonman", description="Control the Elon Man robot.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("daemon")
    sub.add_parser("mcp")
    sub.add_parser("status")
    sub.add_parser("ping")
    sub.add_parser("snap")
    s = sub.add_parser("say")
    s.add_argument("text", nargs="+")
    lk = sub.add_parser("look")
    lk.add_argument("direction", nargs="?", choices=["left", "right", "center", "up", "down"])
    lk.add_argument("--pan", type=float)
    lk.add_argument("--nod", type=float)
    lk.add_argument("--tilt", type=float)
    lk.add_argument("--ms", type=int, default=400)
    f = sub.add_parser("face")
    f.add_argument("mood", choices=["sleep", "idle", "listen", "think", "talk", "happy", "alert"])
    ev = sub.add_parser("events")
    ev.add_argument("--last", type=int, default=20)
    ev.add_argument("--type")
    a = p.parse_args(argv)

    if a.cmd == "daemon":
        from .daemon import serve
        serve()
        return 0
    if a.cmd == "mcp":
        from .mcp_server import run
        run()
        return 0

    payload = {"cmd": a.cmd}
    if a.cmd == "say":
        payload["text"] = " ".join(a.text)
    elif a.cmd == "look":
        if a.direction:
            payload["direction"] = a.direction
        for k in ("pan", "nod", "tilt"):
            if getattr(a, k) is not None:
                payload[k] = getattr(a, k)
        payload["ms"] = a.ms
    elif a.cmd == "face":
        payload["mood"] = a.mood
    elif a.cmd == "events":
        payload["last"] = a.last
        if a.type:
            payload["type"] = a.type

    out = call(payload)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
