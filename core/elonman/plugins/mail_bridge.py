"""Way 3: the robot hands jobs to Grok Bot by email and reads the replies aloud.

Sends only to BOT_EMAIL. Reads only mail from BOT_REPLY_FROM with [elonman] in the subject.
"""
import email
import email.policy
import imaplib
import re
import smtplib
import threading
import time
import uuid
from email.message import EmailMessage
from email.utils import parseaddr

from .. import config

_cfg = {}


def start(core):
    for k in ("ROBOT_EMAIL", "ROBOT_EMAIL_PASSWORD", "BOT_EMAIL", "BOT_REPLY_FROM"):
        _cfg[k] = config.get(k)
        if not _cfg[k]:
            raise RuntimeError(f"{k} is empty in core/.env")
    _cfg["SMTP_HOST"] = config.get("SMTP_HOST", "smtp.gmail.com")
    _cfg["IMAP_HOST"] = config.get("IMAP_HOST", "imap.gmail.com")
    threading.Thread(target=_poll, args=(core,), daemon=True, name="mail_bridge").start()


def send_job(core, text: str) -> str:
    job_id = uuid.uuid4().hex[:6]
    msg = EmailMessage()
    msg["From"] = _cfg["ROBOT_EMAIL"]
    msg["To"] = _cfg["BOT_EMAIL"]
    msg["Subject"] = f"[elonman] {job_id}"
    msg.set_content(text)
    with smtplib.SMTP_SSL(_cfg["SMTP_HOST"], 465, timeout=20) as s:
        s.login(_cfg["ROBOT_EMAIL"], _cfg["ROBOT_EMAIL_PASSWORD"])
        s.send_message(msg)
    core.bus.emit("job_sent", id=job_id, text=text[:300])
    return job_id


def _clean(body: str) -> str:
    keep = []
    for line in body.splitlines():
        if line.startswith(">") or re.match(r"^On .+wrote:$", line.strip()):
            break
        keep.append(line)
    text = " ".join(" ".join(keep).split())
    return text[:600]


def _poll(core):
    want_from = _cfg["BOT_REPLY_FROM"].lower()
    while True:
        try:
            with imaplib.IMAP4_SSL(_cfg["IMAP_HOST"]) as m:
                m.login(_cfg["ROBOT_EMAIL"], _cfg["ROBOT_EMAIL_PASSWORD"])
                m.select("INBOX")
                _, data = m.search(None, '(UNSEEN SUBJECT "[elonman]")')
                for num in data[0].split():
                    _, parts = m.fetch(num, "(RFC822)")   # marks it seen
                    msg = email.message_from_bytes(parts[0][1], policy=email.policy.default)
                    sender = parseaddr(msg.get("From", ""))[1].lower()
                    if sender != want_from:
                        core.bus.emit("mail_ignored", sender=sender)
                        continue
                    part = msg.get_body(preferencelist=("plain",))
                    text = _clean(part.get_content() if part else "")
                    if text:
                        core.bus.emit("bot_reply", subject=str(msg["Subject"]), text=text[:300])
                        core.speaker.say(text)
        except Exception as e:
            core.bus.emit("mail_error", error=str(e)[:200])
        time.sleep(15)
