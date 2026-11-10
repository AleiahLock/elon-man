# Prompt pack

One-off prompts for chat. For scheduled ones see [routines.md](routines.md).

## Setup

**First contact**
> Run elonman status, then look left, look right, center, and say hello to me in one sentence.

**Who I am**
> Ask me 15 questions about my work, my office, my week and how I like things done, then remember the answers as standing rules.

**Teach it the body (Way 1)**
> You can control your body with the elonman command on my computer. Commands: elonman say "text", elonman look left|right|center|up|down, elonman face sleep|idle|listen|think|talk|happy|alert, elonman status, elonman events --last 20, elonman events --type person_entered. Every command prints JSON. Use my computer only for elonman commands unless I say otherwise.

**Add the MCP server (Way 2)**
> Add a custom MCP server called elonman at https://<your tunnel>/mcp with the header X-Elonman-Key: <key>.

## Office

> Who came in today and when? Read elonman events, don't guess.

> When the next person_entered event happens, run elonman look center and elonman say "Welcome in."

> I'm leaving. Watch the office tonight and tell me in the morning if anything moved after hours.

## Money

> What did I spend on food this week? Reopen Finance before answering.

> Build a Page with this month's income, spending by category, subscriptions and the portfolio. Update it every Monday.

> List every subscription I haven't used in 60 days, with the cancel link or phone number. Cancel nothing.

## Calls

> Call my internet provider, ask to cancel the plan, refuse every retention offer, get a confirmation number. Agree to nothing new without asking me.

> Call these 3 restaurants and ask which has a table for 4 on Friday at 8. Book nothing, tell me the options.

## Shopping

> Find me the best price on a 2 mm brass rod kit and 4 M2 ball links. Three stores, total after shipping. Buy nothing.

## Content

> Make three 6-second loops of the robot turning its head, same first and last frame. Send them to me. Post nothing.

## Night shift

> I'm leaving. What can you work on for the next 12 hours that moves this week's goal? Draft everything, send nothing, and tell me in the morning.

## Build the robot with it

> Here is my OpenSCAD file [attach]. Make the head 10% wider and the face hole 64 mm. Show me the code first.

> Here is my ESP32 sketch [attach]. Add a 'wink' face. Show me the diff, don't flash anything.

> Write a plugin for the Elon Man core in a new git branch: [job]. It must have a start(core) function, a manifest in core/manifests, and a test that fails now and passes after your change. Show me the diff and the test output. Merge nothing.

> This is my robot's event log [paste elonman events --last 50]. What's wrong?
