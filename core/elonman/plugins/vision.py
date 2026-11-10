"""Vision: turns the neck toward the biggest face, logs who comes and goes.

Frames live in memory only and are dropped. Nothing here writes an image,
except snap(), which saves one frame on this Mac when asked.
Upgrade path: swap the Haar cascade for MediaPipe or a YOLO person model.
"""
import threading
import time
from datetime import datetime

from .. import config

_latest = {"frame": None}


def _work_hours(now: datetime) -> bool:
    try:
        start, end = [int(x) for x in config.get("WORK_HOURS", "08-19").split("-")]
    except ValueError:
        start, end = 8, 19
    return now.weekday() < 5 and start <= now.hour < end


def start(core):
    import cv2  # noqa: F401  (fail early if OpenCV is missing)
    threading.Thread(target=_run, args=(core,), daemon=True, name="vision").start()


def snap(core):
    import cv2

    frame = _latest["frame"]
    if frame is None:
        raise RuntimeError("no camera frame yet")
    config.SNAPS.mkdir(parents=True, exist_ok=True)
    path = config.SNAPS / f"snap_{datetime.now():%Y%m%d_%H%M%S}.jpg"
    cv2.imwrite(str(path), frame)
    return path


def _run(core):
    import cv2

    cap = cv2.VideoCapture(config.get_int("CAMERA_INDEX", 0))
    if not cap.isOpened():
        core.bus.emit("camera_error", error="camera did not open, check CAMERA_INDEX")
        return
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    pan_sign = config.get_int("PAN_SIGN", 1)
    W, H = 320, 180

    stable = 0          # people count we've announced
    candidate, since = 0, time.time()
    last_track = 0.0
    prev = None
    last_motion_alert = 0.0

    while True:
        ok, frame = cap.read()
        if not ok:
            time.sleep(0.5)
            continue
        _latest["frame"] = frame
        now = time.time()
        small = cv2.resize(frame, (W, H))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(22, 22))
        n = len(faces)

        # Debounce: a new count must hold 1 s to count as "entered", 5 s as "left".
        if n != candidate:
            candidate, since = n, now
        elif n != stable and now - since > (1.0 if n > stable else 5.0):
            if n > stable:
                core.bus.emit("person_entered", count=n)
            else:
                core.bus.emit("person_left", count=n)
                if n == 0:
                    core.bus.emit("office_empty")
            stable = n
            core.state["people"] = n

        # Follow the biggest face with small eased moves (attention, not a turret).
        if n and now - last_track > 0.25 and not core.speaker.speaking():
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            dx = (x + w / 2) / W - 0.5
            dy = (y + h / 2) / H - 0.5
            if abs(dx) > 0.07 or abs(dy) > 0.10:
                pan = core.state["pan"] - pan_sign * dx * 24
                nod = core.state["nod"] - dy * 14
                try:
                    core.look(pan, nod, core.state["tilt"], 250)
                except Exception:
                    pass
            last_track = now

        # Motion after hours: frame difference outside WORK_HOURS, at most one alert per 10 min.
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        if prev is not None and not _work_hours(datetime.now()):
            moved = cv2.absdiff(prev, blur).mean()
            if moved > 6 and now - last_motion_alert > 600:
                core.bus.emit("motion_after_hours", level=round(float(moved), 1))
                last_motion_alert = now
        prev = blur
        time.sleep(0.05)
