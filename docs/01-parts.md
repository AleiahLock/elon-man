# 1. Parts

Prices are rough, November 2026, AliExpress and Amazon. Machine-readable list: [../hardware/BOM.csv](../hardware/BOM.csv).

## Pick your face first

| Option | What it is | Price | Firmware |
|---|---|---|---|
| **Budget (recommended for a first build)** | ESP32-S3 DevKit + 1.28 inch GC9A01 round display, 240x240, SPI | ~$15 | Works with this repo as is |
| **Big face** | Round 2.1 inch 480x480 display with a built-in ESP32-S3 (Waveshare and others) | ~$35 | Swap the display lines in `face.h` for the vendor's Arduino_GFX example |

The big face looks better on camera. The budget one is easier because every pin is yours and the driver is one line.

## Head

| Part | Qty | ~USD | Notes |
|---|---|---|---|
| Face + controller (see above) | 1 | 15-35 | |
| USB webcam, 1080p | 1 | 15-40 | Take it out of its case so it fits the slot on top of the head |

## Neck

| Part | Qty | ~USD | Notes |
|---|---|---|---|
| MG996R servo | 1 | 8 | Pan (left/right). Lives in the body, not the neck |
| MG90S metal-gear micro servo | 2 | 8 | Left and right push rods |
| 2 mm steel or brass rod, 100 mm | 2 | 3 | Push rods |
| M2 ball link | 4 | 3 | One at each rod end |
| 608 bearing | 1 | 1 | Takes the weight off the pan servo |

Two push rods do nod and tilt together. Both up is a nod, one up and one down is a tilt. That's the movement that makes the head look alive.

## Voice

| Part | Qty | ~USD | Notes |
|---|---|---|---|
| USB speakerphone with echo cancelling | 1 | 25-60 | Mic and speaker in one. Echo cancelling is what lets you interrupt him without him hearing himself |

A USB mic plus a small USB speaker also works, but barge-in gets unreliable without echo cancelling.

## Power and cables

| Part | Qty | ~USD | Notes |
|---|---|---|---|
| 5V 4A power supply | 1 | 10 | Servos only. Servos pull current spikes that reset the board if you feed them from USB |
| 1000 uF capacitor, 10V or more | 1 | 1 | Across servo 5V and GND, close to the servos |
| Powered USB hub, 4 ports | 1 | 15 | Board, camera and speakerphone on one cable to the Mac |
| Dupont wires, small perfboard, heat-shrink | 1 | 5 | |

## Printed parts

| Part | Material | Weight |
|---|---|---|
| Body shell, head shell | Red PLA or PETG | ~350 g |
| Base | Black PLA | ~120 g |
| Chest chevrons | Gold or yellow PLA | ~20 g |
| Face bezel | Gray PLA | ~10 g |
| Neck yoke, servo mounts | PETG (stronger) | ~60 g |

Plus an M2/M3 screw kit and M3 heat-set inserts, about $10.

## Total

**$130 to $200**, depending on the face and the speaker. Filament is about $15 of it.

## Tools

A 3D printer (any 220 mm bed works if you split the body), a soldering iron, a small screwdriver set, a hot-glue gun, and a Mac.

Next: [2. Print the body](02-print.md)
