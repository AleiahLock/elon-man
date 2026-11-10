# 3. Wiring

```
                 5V 4A SUPPLY
                 +5V      GND
                  │        │
          ┌───────┼────────┼──────────────┐
          │   [1000uF]     │              │
          │       │        │              │
   MG996R (pan)  red ─ +5V   brown ─ GND   orange ─ GPIO 4
   MG90S (left)  red ─ +5V   brown ─ GND   orange ─ GPIO 5
   MG90S (right) red ─ +5V   brown ─ GND   orange ─ GPIO 6
                           │
                 ESP32-S3 GND ──┘   (common ground, or nothing moves right)

   GC9A01 display      ESP32-S3
   VCC  ─────────────  3.3V
   GND  ─────────────  GND
   SCL/SCK ──────────  GPIO 12
   SDA/MOSI ─────────  GPIO 11
   CS   ─────────────  GPIO 10
   DC   ─────────────  GPIO 9
   RST  ─────────────  GPIO 8
   BL   ─────────────  GPIO 7  (or 3.3V)

   ESP32-S3 USB-C ──┐
   USB webcam ──────┼── powered USB hub ── one cable ── Mac
   USB speakerphone ┘
```

Pins are set in [../firmware/elonman_body/config.h](../firmware/elonman_body/config.h). Change them there if your board is different.

## Rules

- **Servo power never comes from the board.** Red servo wires go to the 5V 4A supply. Only the signal wire goes to the ESP32.
- **Tie the grounds together.** Supply GND, servo GND and ESP32 GND on one rail.
- **Capacitor close to the servos**, long leg (+) to 5V. It soaks up the spikes when all three start at once.
- **Big face board:** the screen is already on it, skip the display table. Check the vendor's pinout before you pick servo pins, since some GPIOs are taken by the panel.
- Use the USB-C port marked **USB** (native), not **UART**, if your DevKit has two.

## Center before you close the shell

1. Flash the firmware (next page). On boot every servo goes to center.
2. With power on, push the horns on as close to straight as the teeth allow.
3. Fix the last few degrees in `config.h` (`TRIM_PAN`, `TRIM_LEFT`, `TRIM_RIGHT`) or live with `{"cmd":"trim",...}`.

Most "my robot twitches" problems are a horn mounted 20 degrees off.

## Mechanical tips

- Pan servo in the body, yoke on its horn, 608 bearing under the yoke. The head weighs more than you think with a camera and a screen.
- Push rods: servo horn to ball link, rod, ball link to the head. Equal length on both sides.
- Hot-glue the cables to the neck with some slack so they don't pull when he turns.
- Keep the angle limits in `config.h` and `core/policy.yaml`. A servo that hits the shell burns out.

Next: [4. Firmware](04-firmware.md)
