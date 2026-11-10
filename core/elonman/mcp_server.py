"""MCP server for Grok Bot (Way 2).

Grok Bot can't reach localhost, so this runs on 127.0.0.1:8000 and you put it
behind an https tunnel. Every request must carry the X-Elonman-Key header.
Only safe tools are exposed. There is no "run a shell command" tool, on purpose.
"""
import hmac
import json

from . import config
from .cli import call


def run():
    import uvicorn
    from mcp.server.fastmcp import FastMCP
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import JSONResponse

    key = config.get("ELONMAN_MCP_KEY")
    if len(key) < 24:
        raise SystemExit("Set ELONMAN_MCP_KEY in core/.env to a long random string first.")

    mcp = FastMCP("elonman")

    def _do(payload):
        payload["by"] = "grok-bot-mcp"
        return json.dumps(call(payload), ensure_ascii=False)

    @mcp.tool()
    def status() -> str:
        """What Elon Man sees and is doing: angles, mood, people in view, recent events."""
        return _do({"cmd": "status"})

    @mcp.tool()
    def say(text: str) -> str:
        """Speak out loud through the robot. Keep it under 3 sentences."""
        return _do({"cmd": "say", "text": text})

    @mcp.tool()
    def look(direction: str) -> str:
        """Turn the head: left, right, center, up or down."""
        return _do({"cmd": "look", "direction": direction})

    @mcp.tool()
    def face(mood: str) -> str:
        """Change the face: sleep, idle, listen, think, talk, happy or alert."""
        return _do({"cmd": "face", "mood": mood})

    @mcp.tool()
    def events(last: int = 20, type: str = "") -> str:
        """Read the event log (person_entered, person_left, office_empty, motion_after_hours, heard, said...)."""
        payload = {"cmd": "events", "last": last}
        if type:
            payload["type"] = type
        return _do(payload)

    class KeyCheck(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            # Header first. ?key= in the URL is a fallback for clients that can't set headers.
            got = request.headers.get("x-elonman-key", "") or request.query_params.get("key", "")
            if not hmac.compare_digest(got, key):
                return JSONResponse({"error": "bad key"}, status_code=401)
            return await call_next(request)

    app = mcp.streamable_http_app()   # serves /mcp
    app.add_middleware(KeyCheck)
    print("[mcp] elonman MCP on http://127.0.0.1:8000/mcp  (put a tunnel in front of it)")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
