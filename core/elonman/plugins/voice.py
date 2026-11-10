"""Voice: wake word -> record -> local speech-to-text -> brain -> speak.

Barge-in: while he talks, loud input for ~0.3 s stops him and he listens.
Use a speakerphone with echo cancelling, or he'll interrupt himself.
"""
import queue
import threading
import time

from .. import config
from . import brain

SR = 16000
CHUNK = 1280          # 80 ms, what openWakeWord expects


def _rms(x):
    import numpy as np
    return float(np.sqrt(np.mean((x.astype(np.float32) / 32768.0) ** 2)))


def start(core):
    threading.Thread(target=_run, args=(core,), daemon=True, name="voice").start()


def _record(q, silence_s=0.9, max_s=12.0, level=0.015):
    """Collect audio until ~0.9 s of quiet after speech, or 12 s."""
    import numpy as np

    chunks, quiet, heard = [], 0.0, False
    t0 = time.time()
    while time.time() - t0 < max_s:
        c = q.get()
        chunks.append(c)
        if _rms(c) > level:
            heard, quiet = True, 0.0
        else:
            quiet += CHUNK / SR
            if (heard and quiet > silence_s) or (not heard and quiet > 4.0):
                break
    return np.concatenate(chunks) if heard else None


def _run(core):
    import numpy as np
    import sounddevice as sd
    import openwakeword
    from openwakeword.model import Model
    from faster_whisper import WhisperModel

    wake = config.get("WAKE_MODEL", "hey_jarvis")
    if not wake.endswith((".onnx", ".tflite")):
        openwakeword.utils.download_models()
    ww = Model(wakeword_models=[wake], inference_framework="onnx")
    threshold = config.get_float("WAKE_THRESHOLD", 0.5)
    stt = WhisperModel(config.get("WHISPER_MODEL", "small.en"), device="cpu", compute_type="int8")
    core.bus.emit("voice_ready", wake=wake)

    q = queue.Queue()

    def on_audio(indata, frames, t, status):
        q.put(indata[:, 0].copy())

    loud, listen_now = 0, False
    with sd.InputStream(samplerate=SR, channels=1, dtype="int16", blocksize=CHUNK, callback=on_audio):
        while True:
            chunk = q.get()

            if core.speaker.speaking():
                loud = loud + 1 if _rms(chunk) > 0.04 else 0
                if loud >= 4:
                    core.speaker.stop()
                    core.bus.emit("barge_in")
                    loud, listen_now = 0, True
                continue

            scores = ww.predict(chunk)
            if not listen_now and max(scores.values()) < threshold:
                continue

            listen_now = False
            ww.reset()
            core.bus.emit("wake_word")
            core.set_face("listen")
            audio = _record(q)
            if audio is None:
                core.set_face("idle")
                continue
            core.set_face("think")
            segments, _ = stt.transcribe(audio.astype(np.float32) / 32768.0, language="en", vad_filter=True)
            text = " ".join(s.text.strip() for s in segments).strip()
            if not text:
                core.set_face("idle")
                continue
            core.bus.emit("heard", text=text)
            threading.Thread(target=brain.handle, args=(core, text), daemon=True).start()
