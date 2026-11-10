# Elon Man

A desk robot with Grok Bot as its brain. Red 3D-printed body, a round face screen, a camera on its head, a neck that turns toward whoever walks in, and a voice you can interrupt mid-sentence.

The body is about $170 of parts. The brain is Grok Bot (SpaceXAI), which already has your email, calendar, finance, calls, shopping and routines. This repo gives it a face, eyes and a voice, and wires the two together.

```
  YOU ──voice──►  ┌──────────── THE BODY (ESP32-S3) ────────────┐
                  │  3 servos (pan + 2 push rods), face screen   │
                  │  USB camera, USB speakerphone                │
                  └──────────────┬───────────────────────────────┘
                                 │ USB (one JSON line per command)
                  ┌──────────────▼──────── THE CORE (Python, Mac) ┐
                  │  HAL  ·  event bus  ·  policy.yaml            │
                  │  plugins: vision, voice, mail_bridge          │
                  │  elonman CLI  ·  MCP server (optional)        │
                  └──────────────┬────────────────────────────────┘
          local execution /      │      email to bot+elonman@
          MCP over https tunnel  │
                  ┌──────────────▼──────── THE BRAIN (Grok Bot) ──┐
                  │  Elon Man (Chief) + specialist Bots           │
                  │  connectors, routines, approvals, memory      │
                  └───────────────────────────────────────────────┘
```

## What it does

- Turns its head toward the biggest face in view and logs who came in and left
- Wakes on its name, listens, answers out loud, stops talking the moment you speak
- Hands real work to Grok Bot by email and reads the reply back to you
- Lets Grok Bot drive the body: `elonman say`, `look`, `face`, `status`, `events`
- Keeps camera frames and audio on your Mac. Only text events leave it
- Refuses any command that isn't on the list in `core/policy.yaml`

What it does through Grok Bot (connectors, not code in this repo): the money desk (Plaid, read-only), calls, shopping with approval, inbox, content, Shopify, print farm, home devices. See [docs/07-jobs.md](docs/07-jobs.md).

## Build order

| Step | Guide | Time |
|---|---|---|
| 1 | [Parts list](docs/01-parts.md) and [BOM.csv](hardware/BOM.csv) | order day 1 |
| 2 | [Print the body](docs/02-print.md) with [elonman.scad](hardware/cad/elonman.scad) | 1-2 days of printing |
| 3 | [Wiring](docs/03-wiring.md) | 1 hour |
| 4 | [Firmware](docs/04-firmware.md) for the ESP32 | 30 min |
| 5 | [The core on your Mac](docs/05-core.md) | 1 hour |
| 6 | [Grok Bot setup](docs/06-grok-bot-setup.md) | 30 min |
| 7 | [Connect Grok Bot to the robot](docs/08-connect.md): 3 ways | 15 min to 1 hour |
| 8 | [Jobs, routines and prompts](grok-bot/) | ongoing |
| 9 | [Trust and control](docs/09-safety.md) | read before step 7 |

Stuck? [docs/10-troubleshooting.md](docs/10-troubleshooting.md).

## Quick start (no hardware yet)

You can run the whole core with a fake body and test the Grok Bot link before the parts arrive.

```bash
git clone https://github.com/AleiahLock/elon-man.git
cd elon-man/core
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[all]"
cp .env.example .env          # leave ELONMAN_PORT=fake
elonman daemon                # terminal 1
elonman status                # terminal 2
elonman look left
elonman say "Hello. I don't have a body yet."
```

The fake body prints every servo and face command instead of sending it over USB.

## Repo map

```
docs/                  step-by-step guides 01-10
hardware/BOM.csv       parts with rough prices (Nov 2026)
hardware/cad/          OpenSCAD source for every printed part
firmware/elonman_body/ Arduino sketch for the ESP32-S3
core/                  Python package: daemon, HAL, bus, plugins, CLI, MCP server
core/policy.yaml       the command allowlist and angle limits (lock this file)
core/manifests/        one manifest per plugin; no manifest, no load
grok-bot/              charter, rules, routines and the prompt pack to paste into Grok Bot
```

## Requirements

- macOS on Apple silicon (Intel works, speech is slower). Linux works if you swap `say` for Piper
- Python 3.10+
- Arduino IDE 2.x or arduino-cli with the ESP32 core
- A Grok Bot plan (included in The X Subscription; Premium is $30/month, Super and Ultra give more weekly usage)
- An xAI API key from console.x.ai for the live voice conversation
- A spare email account for the robot (Way 3 only)

## Safety in one paragraph

Grok Bot runs commands on your Mac only with Execution on Local Computer set to **Ask every time**, so you see each one. The `elonman` command accepts only what's listed in `policy.yaml`, clamps every angle, and never returns a camera image, only a local file path. Anything that sends, pays, posts, deletes, signs, trades or unlocks comes back to you as a draft or an approval card on the Grok Bot side. Full rules in [docs/09-safety.md](docs/09-safety.md).

## Not affiliated

Elon Man is a hobby project. It isn't made, endorsed or supported by SpaceXAI, xAI or X. Grok Bot features and plans change; check x.ai/bot for the current state before you build a routine on one.

## License

MIT. See [LICENSE](LICENSE).
