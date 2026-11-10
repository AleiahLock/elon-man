#pragma once
// Seven faces drawn with Arduino_GFX. Redraws only when something changes.

#include <Arduino_GFX_Library.h>
#include "config.h"

#define C_BG    0x0000
#define C_EYE   0xFFFF
#define C_CYAN  0x07FF
#define C_GOLD  0xFE60
#define C_RED   0xF800
#define C_DIM   0x4208

Arduino_DataBus *faceBus = new Arduino_ESP32SPI(TFT_DC, TFT_CS, TFT_SCK, TFT_MOSI, GFX_NOT_DEFINED);
Arduino_GFX *gfx = new Arduino_GC9A01(faceBus, TFT_RST, 0, true);

enum Mood { M_SLEEP, M_IDLE, M_LISTEN, M_THINK, M_TALK, M_HAPPY, M_ALERT };
static const char *MOOD_NAMES[] = {"sleep", "idle", "listen", "think", "talk", "happy", "alert"};

static Mood mood = M_SLEEP;
static bool dirty = true;
static uint32_t nextBlink = 0, blinkUntil = 0, lastAnim = 0;
static int animStep = 0;
static int W = 240, H = 240;

const char *faceMoodName() { return MOOD_NAMES[mood]; }

void faceBegin() {
  if (TFT_BL >= 0) { pinMode(TFT_BL, OUTPUT); digitalWrite(TFT_BL, HIGH); }
  gfx->begin();
  W = gfx->width();
  H = gfx->height();
  gfx->fillScreen(C_BG);
}

bool faceSet(const char *name) {
  for (int i = 0; i < 7; i++) {
    if (!strcmp(name, MOOD_NAMES[i])) {
      mood = (Mood)i;
      dirty = true;
      animStep = 0;
      return true;
    }
  }
  return false;
}

static void eyes(uint16_t c, int h, int dy = 0) {
  int ew = W / 7, gap = W / 5, cy = H / 2 - H / 12 + dy;
  gfx->fillRoundRect(W / 2 - gap - ew / 2, cy - h / 2, ew, h, ew / 3, c);
  gfx->fillRoundRect(W / 2 + gap - ew / 2, cy - h / 2, ew, h, ew / 3, c);
}

static void ring(uint16_t c) {
  for (int i = 0; i < 4; i++) gfx->drawCircle(W / 2, H / 2, W / 2 - 3 - i, c);
}

static void drawMood(bool blink) {
  gfx->fillScreen(C_BG);
  int eh = blink ? 6 : H / 4;
  switch (mood) {
    case M_SLEEP:
      eyes(C_DIM, 6);
      gfx->setTextColor(C_DIM);
      gfx->setTextSize(3);
      gfx->setCursor(W * 2 / 3, H / 5);
      gfx->print("z");
      break;
    case M_IDLE:
      eyes(C_EYE, eh);
      break;
    case M_LISTEN:
      eyes(C_CYAN, blink ? 6 : H / 4 + 10);
      ring(C_CYAN);
      break;
    case M_THINK:
      eyes(C_EYE, H / 6, -H / 14);
      for (int i = 0; i < 3; i++)
        gfx->fillCircle(W / 2 - 24 + i * 24, H * 3 / 4, i == animStep % 3 ? 7 : 4, C_GOLD);
      break;
    case M_TALK: {
      eyes(C_EYE, eh);
      int mh = 6 + (animStep % 4) * 8;
      gfx->fillRoundRect(W / 2 - W / 8, H * 3 / 4 - mh / 2, W / 4, mh, 4, C_GOLD);
      break;
    }
    case M_HAPPY: {
      int gap = W / 5, cy = H / 2 - H / 12;
      for (int t = 0; t < 6; t++) {
        gfx->drawCircle(W / 2 - gap, cy + 14, 22 - t, C_GOLD);
        gfx->drawCircle(W / 2 + gap, cy + 14, 22 - t, C_GOLD);
      }
      gfx->fillRect(0, cy + 14, W, 30, C_BG);  // keep only the top arcs: ^ ^
      break;
    }
    case M_ALERT:
      eyes(C_RED, H / 4 + 10);
      ring(C_RED);
      break;
  }
}

void faceTick() {
  uint32_t now = millis();
  bool canBlink = (mood == M_IDLE || mood == M_LISTEN || mood == M_TALK);
  if (canBlink && now > nextBlink) {
    blinkUntil = now + 120;
    nextBlink = now + 2500 + random(3000);
    dirty = true;
  }
  if ((mood == M_TALK || mood == M_THINK) && now - lastAnim > 140) {
    lastAnim = now;
    animStep++;
    dirty = true;
  }
  static bool wasBlinking = false;
  bool blinking = now < blinkUntil;
  if (blinking != wasBlinking) { dirty = true; wasBlinking = blinking; }
  if (!dirty) return;
  dirty = false;
  drawMood(blinking);
}
