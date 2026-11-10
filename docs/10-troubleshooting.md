# 10. Troubleshooting

| Symptom | Fix |
|---|---|
| Board resets when servos move | Servos are powered from USB. Move servo red wires to the 5V 4A supply, add the 1000 uF capacitor, tie grounds |
| Servos jitter at rest | Common ground missing, or a cheap supply. Check GND between supply and ESP32 |
| Head twitches or sits crooked | Horn mounted off-center. Re-seat it at boot center, then trim in `config.h` |
| One rod moves the wrong way | Flip `LEFT_SIGN` or `RIGHT_SIGN` in `config.h` |
| Screen stays black | Check `TFT_BL`, then the SPI pins in `config.h`. Big-face boards need the vendor's display setup in `face.h` |
| `no reply from the body` | Wrong `ELONMAN_PORT` (`ls /dev/cu.usbmodem*`), USB CDC On Boot disabled, or a charge-only cable |
| `core is not running` | Start `elonman daemon` in another terminal or load the LaunchAgent |
| `'xyz' is not in policy.yaml cli.allowed` | Working as intended. Add it to the allowlist only if you mean it |
| He turns away from faces | `PAN_SIGN=-1` in `core/.env` |
| `camera did not open` | Try `CAMERA_INDEX=1`. Allow camera access for Terminal in System Settings > Privacy |
| Wake word never fires | Check the mic in System Settings > Sound. Lower `WAKE_THRESHOLD` to 0.35. Say "hey Jarvis" until your own model is trained |
| He interrupts himself | No echo cancelling. Use a speakerphone, or lower the speaker volume |
| `My brain link is down` | `XAI_API_KEY` or `XAI_MODEL` empty or wrong in `core/.env` |
| Grok Bot says `elonman: command not found` | It runs in a shell without your venv. Make the symlink in [08-connect.md](08-connect.md#way-1-local-execution) |
| MCP: Bot can't connect | localhost URL. Use the tunnel's https address and include `/mcp` at the end |
| MCP: `bad key` | Header name is `X-Elonman-Key`, value must match `ELONMAN_MCP_KEY` exactly |
| Mail bridge: nothing is read aloud | `BOT_REPLY_FROM` doesn't match the sender. Check `elonman events --type mail_ignored` |
| Mail bridge: login fails | Gmail needs an app password, not your normal password |
| Night routine never finished | It waited for an approval that expired (~30 min). End night routines with a draft |
| Usage runs out midweek | A routine runs too often. Ask: "List every routine, its runs and how often it found nothing. Recommend what to slow down." |

Still stuck: run `elonman events --last 50` and paste it to Grok Bot with "this is my robot's event log, what's wrong?"
