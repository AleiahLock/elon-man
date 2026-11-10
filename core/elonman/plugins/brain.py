"""The live conversation. A Grok model through the xAI API answers small talk
right away; anything that is real work becomes a job for Grok Bot.

Not a plugin on its own: voice.py calls handle(). No manifest needed.
"""
import json
from collections import deque

from .. import config

SYSTEM = """You are Elon Man, a desk robot with a red body, a round face screen and a camera.
Your brain for real work is Grok Bot. You are the voice.
Reply ONLY with JSON: {"say": "...", "job": null or "...", "look": null or "left|right|center|up|down", "mood": "idle|happy|think|alert"}
Rules:
- "say" is spoken aloud: 1-2 short sentences, no lists, no markdown.
- Anything that needs email, calendar, money, calls, shopping, files, the web, posting or devices is a "job":
  write the full request for Grok Bot in "job" and say something like "On it." Never claim a job is done.
- You never send, pay, post, delete, sign, trade or unlock. Grok Bot asks the owner for those.
- Small talk, jokes and questions you can answer from general knowledge: answer in "say", job = null.
"""

_history = deque(maxlen=10)
_client = None


def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI
        key = config.get("XAI_API_KEY")
        if not key:
            raise RuntimeError("XAI_API_KEY is empty in core/.env")
        _client = OpenAI(api_key=key, base_url="https://api.x.ai/v1")
    return _client


def _parse(raw: str) -> dict:
    try:
        return json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
    except ValueError:
        return {"say": raw.strip()[:300], "job": None}


def handle(core, text: str):
    try:
        model = config.get("XAI_MODEL")
        if not model:
            raise RuntimeError("XAI_MODEL is empty in core/.env")
        msgs = [{"role": "system", "content": SYSTEM}, *_history, {"role": "user", "content": text}]
        resp = _get_client().chat.completions.create(model=model, messages=msgs, temperature=0.4)
        raw = resp.choices[0].message.content or ""
        _history.extend([{"role": "user", "content": text}, {"role": "assistant", "content": raw}])
        out = _parse(raw)
    except Exception as e:
        core.bus.emit("brain_error", error=str(e))
        core.set_face("alert")
        core.speaker.say("My brain link is down. Check the API key.")
        return

    if out.get("look"):
        try:
            pan, nod = core.policy.direction(out["look"])
            core.look(pan, nod, 0, 400)
        except Exception:
            pass

    job = out.get("job")
    if job:
        bridge = core.plugins.get("mail_bridge")
        if bridge:
            try:
                bridge.send_job(core, job)
            except Exception as e:
                core.bus.emit("mail_error", error=str(e)[:200])
                out["say"] = "I couldn't send that to Grok Bot. Check the mail settings."
        else:
            out["say"] = "I can't reach Grok Bot. The mail bridge is off."
    core.speaker.say(out.get("say") or "On it.")
