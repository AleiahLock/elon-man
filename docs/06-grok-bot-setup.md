# 6. Grok Bot setup

Grok Bot is the brain. It has a computer in the cloud with a browser, files and a terminal, your logins through connectors, memory, routines on a schedule or on an event, and coworker Bots that hand work to each other. It keeps running when your laptop is closed.

Three of its features make the robot possible:

| Feature | Where | Used for |
|---|---|---|
| Execution on Local Computer | Settings > General | Grok Bot runs `elonman ...` on your Mac (Way 1) |
| Custom MCP server | Added by asking in chat | Structured tools over an https tunnel (Way 2) |
| The Bot's own email | Asked for in chat | The robot sends spoken jobs, a routine fires on them (Way 3) |

Grok Bot comes with The X Subscription. Premium ($30/month) includes it; Super and Ultra give more weekly usage. A robot that runs routines all day uses a lot, so start with slow schedules.

## Step 1. Install

Go to x.ai/bot, "Download for macOS", pick Apple silicon or Intel. Sign in with a plan that includes Grok Bot.

## Step 2. Create the Chief

New Bot, name it **Elon Man**. Paste [../grok-bot/charter.txt](../grok-bot/charter.txt) as its description.

## Step 3. Tell it who you are, once

> "Ask me 15 questions about my work, my office, my week and how I like things done, then remember the answers as standing rules."

## Step 4. Connect the apps

Sidebar > connect apps. Connect what you'll use: email, calendar, Slack or Telegram, Notion, Finance (Plaid, read-only), Shopify if you sell, Robinhood or Coinbase if you invest.

Connectors are cheaper and more reliable than the Bot clicking through a website.

## Step 5. Turn on local execution

Settings > General > **Execution on Local Computer** > **Ask every time**.

Every command the Bot wants to run on your Mac shows up for your OK. After a few days you can always-allow the harmless ones (see [9. Trust and control](09-safety.md)).

## Step 6. Claim the Bot's email

Ask Elon Man:

> "Set up your own email address."

Use a plus alias for the robot, for example `yourbot+elonman@...`. Put it in `core/.env` as `BOT_EMAIL`, and the address replies come from as `BOT_REPLY_FROM`.

## Step 7. Add the specialists

Don't make Elon Man do everything. Create one Bot per job and let Elon Man route:

| Bot | Job | Connectors |
|---|---|---|
| Office Watch | Reads robot events, evening summary, after-hours alerts | local execution or MCP |
| Money Desk | Morning number, subscriptions, invoices, watchlist | Finance (Plaid), Robinhood/Coinbase, invoicing |
| Inbox | Triage, drafts, follow-ups | Gmail/Outlook, calendar |
| Content | Clips, captions, drafts for approval | video in chat, Krea/HeyGen plugins |
| Print Farm | Print queue, finished prints | OctoPrint via MCP or local execution |
| Home | Lights, blinds, music | Home in the phone app, or Home Assistant |

Descriptions for each are in [../grok-bot/team.md](../grok-bot/team.md).

## Step 8. Paste the rules

Paste [../grok-bot/rules.txt](../grok-bot/rules.txt) once. Ask it to show the rules back to you and change nothing until you confirm.

## Step 9. Turn on Auto-review

Auto-review is a separate model that checks risky actions (shell commands, plugin calls, computer use, new routines) before they run. Turn it on before you connect Home, so unlocks follow the approval rules.

Next: [7. What he can take on](07-jobs.md), then [8. Connect Grok Bot to the robot](08-connect.md)
