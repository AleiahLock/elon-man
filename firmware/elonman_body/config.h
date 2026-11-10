#pragma once
// Edit this file for your build. Everything else should not need changes.

#define FW_VERSION "0.1.0"

// Servo signal pins
#define PIN_PAN   4
#define PIN_LEFT  5
#define PIN_RIGHT 6

// Flip to -1 if a servo moves the wrong way
#define PAN_SIGN   1
#define LEFT_SIGN  1
#define RIGHT_SIGN -1

// Center trims in degrees (fix a horn mounted a few teeth off)
#define TRIM_PAN   0
#define TRIM_LEFT  0
#define TRIM_RIGHT 0

// Hard angle limits. A servo that hits the shell burns out.
#define PAN_MIN  -60
#define PAN_MAX   60
#define NOD_MIN  -20
#define NOD_MAX   25
#define TILT_MIN -20
#define TILT_MAX  20

// GC9A01 240x240 round display on SPI (budget build).
// For a board with a built-in screen, replace the display setup in face.h
// with the bus/panel lines from the vendor's Arduino_GFX example.
#define TFT_SCK  12
#define TFT_MOSI 11
#define TFT_CS   10
#define TFT_DC    9
#define TFT_RST   8
#define TFT_BL    7   // backlight, set to -1 if tied to 3.3V
