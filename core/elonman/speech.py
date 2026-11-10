"""Speaking out loud. macOS `say` by default, Piper if PIPER_MODEL is set.

stop() cuts him off mid-sentence; the voice plugin calls it on barge-in.
"""
import shutil
import subprocess
import tempfile
import threading

from . import config


class Speaker:
    def __init__(self, core):
        self.core = core
        self._proc = None
        self._lock = threading.Lock()
        self.piper_model = config.get("PIPER_MODEL")

    def speaking(self) -> bool:
        p = self._proc
        return p is not None and p.poll() is None

    def stop(self):
        with self._lock:
            if self.speaking():
                self._proc.terminate()
                self.core.bus.emit("speech_stopped")
            self._proc = None

    def say(self, text: str):
        text = text.strip()
        if not text:
            return
        self.stop()
        cmd = self._command(text)
        with self._lock:
            self._proc = subprocess.Popen(cmd)
            proc = self._proc
        self.core.set_face("talk")
        self.core.bus.emit("said", text=text[:200])
        threading.Thread(target=self._wait, args=(proc,), daemon=True).start()

    def _command(self, text):
        if self.piper_model and shutil.which("piper"):
            wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            subprocess.run(["piper", "--model", self.piper_model, "--output_file", wav],
                           input=text.encode(), check=True, capture_output=True)
            return ["afplay", wav] if shutil.which("afplay") else ["aplay", wav]
        if shutil.which("say"):
            return ["say", text]
        print(f"[speech] no voice installed, would say: {text}")
        return ["true"]

    def _wait(self, proc):
        proc.wait()
        with self._lock:
            if self._proc is proc:
                self._proc = None
                self.core.set_face("idle")
