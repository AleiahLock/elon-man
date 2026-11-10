# Grok Bot config

Everything you paste into Grok Bot, in the order you paste it. Full walkthrough: [../docs/06-grok-bot-setup.md](../docs/06-grok-bot-setup.md).

| File | Paste where |
|---|---|
| [charter.txt](charter.txt) | Description of the Bot named Elon Man |
| [rules.txt](rules.txt) | Once, in a chat with Elon Man. Every Bot inherits it |
| [team.md](team.md) | Descriptions for the specialist Bots |
| [routines.md](routines.md) | One routine per block, into the Bot named in brackets |
| [prompts.md](prompts.md) | One-off prompts for chat |

Settings to check:

- Settings > General > Execution on Local Computer: **Ask every time**
- Auto-review: **on**
- Connectors: email, calendar, Finance, and whatever the specialists need
- The Bot's own email set up, alias `+elonman` noted in `core/.env`
