# 9. Trust and control

A robot with a camera, a microphone and a line to your bank needs limits that hold when you're in a hurry. Here's where each one lives.

## On the Mac (this repo)

| Rule | Where it's enforced |
|---|---|
| Only listed commands run | `core/policy.yaml` `cli.allowed`, checked in `policy.py` before any handler |
| Angles can't break the neck | Clamped twice: `policy.yaml` limits and `config.h` in the firmware |
| Camera images never leave the Mac | `snap` is `local_only`: it saves a file and returns the path, never the image |
| Audio never leaves the Mac | Speech-to-text runs locally; only text goes to the xAI API |
| Frames aren't stored | Vision keeps the last frame in memory only |
| Every plugin declares its power | `core/manifests/<name>.yaml`. No manifest, no load |
| The robot only mails one address | `mail_bridge` sends to `BOT_EMAIL` only, reads only `BOT_REPLY_FROM` |
| The MCP server needs a key | `X-Elonman-Key`, compared in constant time; no shell tool exists |
| The core listens on 127.0.0.1 only | `daemon.py`, `mcp_server.py` |

## Lock the floor

Some files the robot must never change, even if a Bot asks nicely:

```bash
chflags uchg core/policy.yaml          # unlock: chflags nouchg core/policy.yaml
chflags uchg core/.env
chmod 600 core/.env
```

Keep the repo in git and only merge to `main` yourself. If a Bot writes code for the robot, it works in a branch:

```bash
git checkout -b bot/new-skill
# Bot works here. You review the diff and merge.
```

## On Grok Bot

| Rule | Setting |
|---|---|
| You see every command on your Mac | Execution on Local Computer: **Ask every time** |
| Risky actions get a second check | **Auto-review** on |
| Send, pay, post, delete, sign, trade, unlock come back to you | The rules block below + approval cards (Allow once, Always allow, Deny) |
| Night jobs don't hang | Approvals from background work expire after about 30 minutes. Night routines must end in a draft, or use an allow rule you set in advance |

**What to always-allow after a few days:** `elonman status`, `elonman events`, `elonman face`, `elonman look`, `elonman say`.
**Keep on Ask forever:** `elonman snap`, anything that isn't `elonman`.

## The rules block

Paste once, every Bot inherits it. Same text as [../grok-bot/rules.txt](../grok-bot/rules.txt):

> Rules for every Bot on this account: 1) Anything that sends, pays, posts, deletes, signs, trades or unlocks becomes a draft or an approval card. 2) Reopen the source before reporting any number. 3) Use only the logins your job needs. 4) On my computer, run only elonman commands unless I say otherwise. 5) Camera snapshots never leave my Mac without my yes. 6) Night routines never wait for approval: they use an allow rule I set or leave a draft. 7) When something goes wrong, add the fix to RULES.md. Show me the rules first and change nothing until I confirm.

## Self-improvement, in stages

If you let a Bot extend the robot, unlock it one level at a time, and only after the level before has a track record:

| Level | Allowed |
|---|---|
| 0 | Suggests changes in chat |
| 1 | Writes a plugin in its own git branch |
| 2 | Runs it in a sandbox against a copy of `events.jsonl` |
| 3 | Goes live after you merge it |

Proof first: a new skill comes with a test that fails before the change and passes after. No test, no merge.

## Privacy checklist for an office

- Tell people there's a camera. Put a sign on the door
- Set `WORK_HOURS` to your real hours
- `snap` stays on Ask, always
- Delete old events now and then: `~/.elonman/events.jsonl`
