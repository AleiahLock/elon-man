# 7. What he can take on

Each block is a job for one Bot. The robot gives it eyes, a voice and a face; the work itself runs on Grok Bot with its connectors. Ready-to-paste routines: [../grok-bot/routines.md](../grok-bot/routines.md).

## Voice

- Wakes on his name and listens
- Answers in plain language, 1-2 sentences
- You can cut in mid-sentence and he stops
- Turns real requests into jobs for the Bots and reads you the result

## Office watch

- Who came in and when, who left, when the office went empty
- Motion after hours, logged as an event (a snapshot only if you approve it)
- An evening summary from the event log: who was in, deliveries, anything unusual

## The money desk

Finance through Plaid, read-only: banks, cards, investments. The Bot never sees your bank login.

- The morning number by voice: cash, in, out, bills due
- Every recurring charge in the last 90 days, unused ones marked
- Unpaid invoices older than 14 days with draft reminders
- "What did I spend on food this week?" answered from the source, not from memory
- A watchlist that tells you why a ticker moved. Trades are always an approval card
- A Page with the month: income, spending by category, subscriptions, portfolio

He reads everything and can't move a cent on his own.

## Phone calls

Grok Bot can call someone or a business for you, make the request, take notes and send a summary. "Elon Man, call the dentist and move my appointment to any morning next week." Check where calling works for your account first; users report US businesses only for now.

## Shopping and booking

- Finds the item, compares stores, shows the total after shipping
- Watches a price and tells you when it drops
- Tracks orders from your inbox

Payments go through Link with a single-use card per purchase, and you approve every spend.

## Home and office devices

Lights, blinds, music. Either Home in the Grok Bot phone app (turn on Auto-review first), or Home Assistant on your network, which can also act as an MCP server for the Bot. "Unlock the door" always asks.

## Content

Image and video drafts, voiceover, edits. Everything comes to you for approval before it's posted.

## Commerce

Shopify connector: product records, stock, prices, orders not shipped after 48 hours, low stock.

## Print farm

If your printers run OctoPrint, each has an API. A Print Farm Bot keeps the queue, logs every finished print, and asks before starting anything.

## Memory and learning

- Memory built from the event log, which is append-only
- Your rules and preferences, kept by Grok Bot memory
- Every mistake written down with its fix so it doesn't happen twice

## Timed routines

Self-tests, disk space, printer checks, weekly reviews. Once a day beats every 5 minutes for almost everything, and it saves usage.

Next: [8. Connect Grok Bot to the robot](08-connect.md)
