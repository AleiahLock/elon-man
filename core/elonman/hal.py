"""Hardware layer. The only code that touches the serial port.

Everything above this file only knows look(), face() and ping().
Swap the servos or the screen and nothing above changes.
"""
import json
import threading
import time


class Body:
    def __init__(self, port: str, baud: int = 115200):
        import serial  # pyserial

        self.ser = serial.Serial(port, baud, timeout=1.0)
        time.sleep(2.0)  # most ESP32 boards reset when the port opens
        self.ser.reset_input_buffer()
        self._lock = threading.Lock()

    def _send(self, obj: dict) -> dict:
        with self._lock:
            self.ser.reset_input_buffer()
            self.ser.write((json.dumps(obj) + "\n").encode())
            raw = self.ser.readline().decode(errors="ignore").strip()
        if not raw:
            raise TimeoutError("no reply from the body (check the USB cable and the port)")
        reply = json.loads(raw)
        if not reply.get("ok"):
            raise RuntimeError(f"body said: {reply.get('err', reply)}")
        return reply

    def ping(self) -> dict:
        return self._send({"cmd": "ping"})

    def look(self, pan: float, nod: float, tilt: float = 0, ms: int = 400) -> dict:
        return self._send({"cmd": "look", "pan": round(pan, 1), "nod": round(nod, 1), "tilt": round(tilt, 1), "ms": int(ms)})

    def face(self, mood: str) -> dict:
        return self._send({"cmd": "face", "mood": mood})


class FakeBody:
    """Stands in for the robot before the parts arrive."""

    def __init__(self):
        self.state = {"pan": 0, "nod": 0, "tilt": 0, "mood": "sleep"}

    def ping(self):
        return {"ok": True, "fw": "fake", **self.state}

    def look(self, pan, nod, tilt=0, ms=400):
        self.state.update(pan=pan, nod=nod, tilt=tilt)
        print(f"[fake body] look pan={pan:.0f} nod={nod:.0f} tilt={tilt:.0f} over {ms} ms")
        return {"ok": True}

    def face(self, mood):
        self.state["mood"] = mood
        print(f"[fake body] face {mood}")
        return {"ok": True}


def open_body(port: str):
    if not port or port == "fake":
        return FakeBody()
    return Body(port)
