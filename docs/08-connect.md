# 8. Connect Grok Bot to the robot

Three ways. Start with Way 1 today. Add the others when you want more.

| | How | Good for | Setup |
|---|---|---|---|
| **Way 1** | Grok Bot runs `elonman` on your Mac | Everything, from day one | 5 min |
| **Way 2** | Your own MCP server behind an https tunnel | Typed tools, use from any chat with @ | 30 min |
| **Way 3** | The robot emails jobs to the Bot, reads replies aloud | Talking to him: voice to real work | 20 min |

```
            Way 1: local execution  ──►  elonman CLI ─┐
GROK BOT    Way 2: MCP over https   ──►  tunnel ─► mcp_server ─┤──► core daemon ──USB──► body
            Way 3: email  ◄────────────  mail_bridge ◄─────────┘
```

---

## Way 1: local execution

Needs: the core running (`elonman daemon`), Execution on Local Computer set to **Ask every time**.

The Bot runs commands in a shell on your Mac, so `elonman` must be on its PATH. The simplest fix is a symlink:

```bash
sudo ln -s "$(pwd)/.venv/bin/elonman" /usr/local/bin/elonman
which elonman     # /usr/local/bin/elonman
```

Then tell Elon Man in chat:

> "You can control your body with the elonman command on my computer. Commands: elonman say "text", elonman look left|right|center|up|down, elonman face sleep|idle|listen|think|talk|happy|alert, elonman status, elonman events --last 20, elonman events --type person_entered. Every command prints JSON. Run elonman status now and tell me what you see. Use my computer only for elonman commands unless I say otherwise."

Each command comes up for your OK. After a day, always-allow the harmless ones: `status`, `events`, `face`, `look`, `say`. Keep `snap` and anything new on Ask.

**Test:** "Run elonman look left, then right, then center, and say hello to me in one sentence."

---

## Way 2: your own MCP server

Grok Bot can't reach `localhost` (a URL like `http://localhost:8000/mcp` does not work). It needs a public https address, so you run the server on the Mac and put a tunnel in front of it.

**1. Set a key** in `core/.env`:

```bash
python3 -c "import secrets;print(secrets.token_urlsafe(40))"
# ELONMAN_MCP_KEY=<paste>
```

**2. Start the server** (the daemon must be running too):

```bash
elonman mcp
# [mcp] elonman MCP on http://127.0.0.1:8000/mcp
```

**3. Open a tunnel.** Cloudflare Tunnel, free:

```bash
brew install cloudflared
cloudflared tunnel --url http://127.0.0.1:8000
# prints https://<random>.trycloudflare.com
```

The quick tunnel gets a new address each run. For a fixed one (`https://robot.yourdomain.com`), create a named tunnel in the Cloudflare dashboard and point it at `http://127.0.0.1:8000`.

**4. Add it in Grok Bot.** In chat:

> "Add a custom MCP server called elonman at https://robot.yourdomain.com/mcp with the header X-Elonman-Key: <your key>."

Say **custom server**, or it may look for a catalog plugin. Click Add, then attach it with @ in any chat. If your client can't send headers, use `https://robot.yourdomain.com/mcp?key=<your key>`; the server accepts both. The header is better, since URLs end up in logs.

**Tools it exposes:** `status`, `say`, `look`, `face`, `events`. There is no "run a shell command" tool, and there shouldn't be one.

**Test:** "@elonman what's your status? Then look left and say hi."

---

## Way 3: the robot hands jobs to the Bot

You say "hey Jarvis, find me a table for four on Friday" (or "hey Elon Man" once you train the word). The voice plugin transcribes it on the Mac, the brain sees it's real work, and the mail bridge emails it to the Bot. A routine fires on that alias, does the job, and replies. The bridge reads the reply and Elon Man says it out loud.

**1. A mailbox for the robot.** Any account with IMAP. For Gmail: turn on 2-step verification, create an app password, then in `core/.env`:

```
ROBOT_EMAIL=myrobot@gmail.com
ROBOT_EMAIL_PASSWORD=<app password>
SMTP_HOST=smtp.gmail.com
IMAP_HOST=imap.gmail.com
BOT_EMAIL=yourbot+elonman@...        # the Bot's address with the plus alias
BOT_REPLY_FROM=yourbot@...           # the address the Bot's replies come from
ELONMAN_PLUGINS=vision,voice,mail_bridge
```

**2. The routine.** Tell Elon Man:

> "Create a routine: when an email arrives at <yourbot+elonman@...>, treat the body as a spoken request from me. Do it within your rules. Reply to the sender in at most 3 sentences that will be read aloud, no lists, no links. If it needs my approval, say so in the reply and create the approval card."

**3. Test without talking:**

```bash
python3 -c "from elonman.daemon import Core; c=Core(); import elonman.plugins.mail_bridge as m; m.start(c); m.send_job(c, 'What is on my calendar tomorrow?')"
```

Within a minute or so the reply lands in the robot inbox, and `elonman events --type bot_reply` shows it.

The bridge only sends to `BOT_EMAIL` and only reads mail from `BOT_REPLY_FROM` with `[elonman]` in the subject. Anyone else who mails the robot is ignored and logged as `mail_ignored`.

---

## Putting it together

With all three running:

1. Someone walks in. Vision emits `person_entered`, the head turns.
2. At 18:30 the Office Watch routine runs `elonman events` (Way 1) and writes the summary.
3. You say "what did I spend on food this week?" The voice plugin sends a job (Way 3), the Money Desk Bot answers from Finance, Elon Man says it.
4. From any chat you type "@elonman say: meeting in 5 minutes" (Way 2) and he says it in the office.

Next: [9. Trust and control](09-safety.md)
