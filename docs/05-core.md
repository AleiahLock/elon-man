# 5. The core on your Mac

A small Python service that owns the robot. Nothing else touches the USB port.

```
core/
  elonman/hal.py          the only file that talks to the serial port
  elonman/bus.py          publish/subscribe + events.jsonl (append-only log)
  elonman/policy.py       reads policy.yaml, refuses anything not listed, clamps angles
  elonman/daemon.py       the service: body + bus + policy + plugins, HTTP on 127.0.0.1:8765
  elonman/cli.py          the elonman command (what Grok Bot runs)
  elonman/mcp_server.py   optional MCP server for Grok Bot
  elonman/plugins/        vision, voice (+ brain), mail_bridge
  manifests/              one manifest per plugin. No manifest, no load
  policy.yaml             allowlist + limits. Lock it
```

## Install

```bash
cd elon-man/core
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[all]"          # or ".[vision]" / ".[voice]" / ".[mcp]" for less
cp .env.example .env
```

Find the board's port and put it in `.env`:

```bash
ls /dev/cu.usbmodem*
# ELONMAN_PORT=/dev/cu.usbmodem1101
```

Run the tests (they use the fake body, no hardware needed):

```bash
pytest tests
```

## Start it

```bash
elonman daemon
```

macOS asks for camera and microphone access for your terminal the first time. Allow both.

In a second terminal:

```bash
elonman ping
elonman status
elonman look left
elonman look --pan 20 --nod 5
elonman face happy
elonman say "Hello. I'm Elon Man."
elonman events --last 10
elonman events --type person_entered --last 5
elonman snap                      # saves a frame in ~/.elonman/snaps, prints the path
```

If `elonman say` works and the head moves, the body is done.

## Plugins

Set in `.env`: `ELONMAN_PLUGINS=vision,voice,mail_bridge`. Each needs a manifest in `core/manifests/` that declares what it reads, writes and whether anything leaves the Mac.

### vision

- Follows the biggest face with small eased moves (attention, not a turret)
- Events: `person_entered`, `person_left`, `office_empty`, `motion_after_hours` (outside `WORK_HOURS`, at most one per 10 minutes)
- Frames stay in memory and are dropped. Only event text is logged
- If he turns away from you instead of toward you, set `PAN_SIGN=-1`
- It counts visible faces, so someone with their back to the camera doesn't count. For better counts, swap the Haar cascade for MediaPipe or a YOLO person model; the events stay the same

### voice

- Wake word with openWakeWord. Starts with the built-in `hey_jarvis` model. Train your own "hey Elon Man" from a few dozen recordings with the openWakeWord training notebook, then set `WAKE_MODEL=/path/hey_elon_man.onnx`
- Speech to text with faster-whisper, on the Mac. Audio never leaves it
- Replies with a Grok model through the xAI API (`XAI_API_KEY`, `XAI_MODEL` from console.x.ai). Only the transcribed text is sent
- Real work (email, money, calls, shopping, posting) becomes a job for Grok Bot through the mail bridge. He says "On it" and tells you the answer when the Bot replies
- Barge-in: talk over him and he stops and listens
- Voice: macOS `say` by default. For a better local voice install Piper and set `PIPER_MODEL`

### mail_bridge

See [8. Connect Grok Bot, Way 3](08-connect.md#way-3-the-robot-hands-jobs-to-the-bot).

## Run it on login

Save as `~/Library/LaunchAgents/com.elonman.core.plist` (fix the paths):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.elonman.core</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/YOU/elon-man/core/.venv/bin/elonman</string>
    <string>daemon</string>
  </array>
  <key>WorkingDirectory</key><string>/Users/YOU/elon-man/core</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>/tmp/elonman.log</string>
  <key>StandardErrorPath</key><string>/tmp/elonman.log</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.elonman.core.plist
```

Camera and mic permissions for a LaunchAgent can be fussy. If vision or voice don't start, run `elonman daemon` from Terminal once and allow access there.

## Add your own plugin

1. `core/elonman/plugins/myjob.py` with a `start(core)` function. Listen with `core.bus.on("person_entered", fn)`, emit with `core.bus.emit("my_event", key=value)`.
2. `core/manifests/myjob.yaml` declaring `reads`, `writes`, `effects`, `leaves_this_mac`, `risk`.
3. Add `myjob` to `ELONMAN_PLUGINS`.

Plugins never import each other. They talk through events, so a broken one can't take the others down.

Next: [6. Grok Bot setup](06-grok-bot-setup.md)
