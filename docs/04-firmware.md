# 4. Firmware (ESP32-S3)

The body is dumb on purpose. It moves servos, draws a face and answers over USB. All the thinking happens on the Mac and in Grok Bot.

Code: [../firmware/elonman_body/](../firmware/elonman_body/)

## Flash it

1. Install Arduino IDE 2.x.
2. Boards Manager: install **esp32 by Espressif** (3.x).
3. Library Manager: install **ESP32Servo**, **ArduinoJson** (7.x) and **GFX Library for Arduino**.
4. Open `elonman_body.ino`. Board: your ESP32-S3 module. Set **USB CDC On Boot: Enabled**.
5. Edit `config.h` if your pins differ. Upload.

The face shows "z" (sleep) and the head centers.

Or with arduino-cli:

```bash
arduino-cli core install esp32:esp32
arduino-cli lib install ESP32Servo ArduinoJson "GFX Library for Arduino"
arduino-cli compile --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc firmware/elonman_body
arduino-cli upload  --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc -p /dev/cu.usbmodem1101 firmware/elonman_body
```

## Test it by hand

Open Serial Monitor at 115200, line ending "Newline", and send:

```
{"cmd":"ping"}
{"cmd":"face","mood":"happy"}
{"cmd":"look","pan":30,"nod":-5,"tilt":0,"ms":600}
{"cmd":"look","pan":0,"nod":0,"tilt":15,"ms":400}
{"cmd":"face","mood":"talk"}
{"cmd":"trim","pan":2,"left":-3,"right":0}
```

Every line gets one reply, `{"ok":true,...}` or `{"ok":false,"err":"..."}`.

## Protocol

| Command | Fields | What it does |
|---|---|---|
| `ping` | | Returns firmware version, current angles and mood |
| `look` | `pan`, `nod`, `tilt` (degrees), `ms` | Eased move over `ms`. Angles are clamped to `config.h` limits |
| `face` | `mood`: sleep, idle, listen, think, talk, happy, alert | Draws the face. idle/listen/talk blink, talk and think animate |
| `trim` | `pan`, `left`, `right` | Center offsets until reboot |

Moves use smoothstep easing, so the head starts and stops softly instead of snapping.

## Big face board (2.1 inch, 480x480)

These boards use an RGB panel driver, not SPI. In `face.h`, replace the two lines that create `faceBus` and `gfx` with the bus and panel setup from the vendor's Arduino_GFX example for your exact board. The drawing code scales to `gfx->width()` and works unchanged.

## Want it different?

Ask a Bot to change it with you:

> "Here is my ESP32-S3 sketch [attach the folder]. Add an 8th face called 'wink' that closes only the left eye for 300 ms. Show me the diff, don't flash anything."

Next: [5. The core on your Mac](05-core.md)
