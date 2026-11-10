# Routines

Paste each into the Bot named in brackets. Slow clocks win: once a day beats every 5 minutes for almost everything.

## Voice to work (Elon Man) - needed for Way 3

> When an email arrives at <yourbot+elonman@...>, treat the body as a spoken request from me. Do it within your rules. Reply to the sender in at most 3 sentences that will be read aloud, no lists, no links. If it needs my approval, say so in the reply and create the approval card.

## Morning brief (Elon Man)

> Every weekday at 8:30, collect from the other Bots: today's calendar, emails that need me, money red flags, unfinished prints. Run elonman say with the 3 most important items in under 20 seconds, red items first. If I'm not in the office yet (no person_entered event today), send it to me as a message instead.

## Office evening summary (Office Watch)

> Every weekday at 18:30, run elonman events --last 200 and give me five lines: who was in, deliveries, anything left on, anything unusual, what to check tomorrow. Stay silent on weekends unless there's a motion_after_hours event.

## After-hours alert (Office Watch)

> Every 30 minutes between 20:00 and 07:00, run elonman events --type motion_after_hours --last 5. If there's a new one since your last check, message me one line with the time. Don't take a snapshot. Silent otherwise.

## Morning number (Money Desk)

> Every weekday at 8:00, give me: cash across accounts, what came in yesterday, what went out, bills due this week, anything unusual. Reopen Finance before every number. Then run elonman say with it in 20 seconds max.

## Subscriptions (Money Desk)

> On the 1st of every month, list every recurring charge from the last 90 days with the price and the date. Mark the ones nobody used. Cancel nothing.

## Invoices (Money Desk)

> Every Monday at 9:00, list unpaid invoices older than 14 days and draft a polite reminder for each. Send nothing.

## Watchlist (Money Desk)

> Watch these tickers: <list>. Once a day at 16:30, if anything moved more than 5%, tell me why in 3 lines with links. Never place a trade.

## Orders (Elon Man, if you sell on Shopify)

> Every morning at 9:00, check yesterday's orders. Flag anything unshipped after 48 hours and anything under 10 units. Run elonman say with it if a person_entered event happened today.

## Print finished (Print Farm)

> Every 20 minutes during work hours, check my printers. When a print finishes, run elonman say "Printer <n> is done" and log the file, time and material. Ask before starting the next one.

## Memory (Elon Man)

> At 23:00, read today's chats and elonman events. Add new facts about me to MEMORY.md and any mistake plus its fix to RULES.md. Show me what you changed in 5 lines tomorrow morning.

## Self-check (Elon Man)

> Every Friday at 17:00, list every routine, its runs, its failures and how often it found nothing. Recommend what to slow down or delete. Change nothing.

## Body self-test (Elon Man)

> Every Sunday at 10:00, run elonman ping, elonman look left, elonman look right, elonman look center, elonman face happy, elonman face idle. Tell me if any of them failed.
