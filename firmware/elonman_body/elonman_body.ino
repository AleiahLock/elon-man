// Elon Man body firmware
// Board: ESP32-S3 (Arduino core 3.x), "USB CDC On Boot: Enabled"
// Libraries: ESP32Servo, ArduinoJson (7.x), GFX Library for Arduino (Arduino_GFX)
//
// Protocol: one JSON object per line over USB serial at 115200.
//   {"cmd":"ping"}
//   {"cmd":"look","pan":30,"nod":-5,"tilt":0,"ms":400}
//   {"cmd":"face","mood":"happy"}          moods: sleep idle listen think talk happy alert
//   {"cmd":"trim","pan":2,"left":-3,"right":0}   center offsets in degrees, kept until reboot
// Reply: {"ok":true,...} or {"ok":false,"err":"..."}

#include <Arduino.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>
#include "config.h"
#include "face.h"

// ---------- servos ----------
Servo sPan, sLeft, sRight;

struct Axis {
  float from, to, now;
  uint32_t t0, dur;
};
Axis aPan = {0, 0, 0, 0, 1}, aNod = {0, 0, 0, 0, 1}, aTilt = {0, 0, 0, 0, 1};
int trimPan = TRIM_PAN, trimLeft = TRIM_LEFT, trimRight = TRIM_RIGHT;

static float clampf(float v, float lo, float hi) { return v < lo ? lo : (v > hi ? hi : v); }

static void startMove(Axis &a, float target, uint32_t ms) {
  a.from = a.now;
  a.to = target;
  a.t0 = millis();
  a.dur = ms < 1 ? 1 : ms;
}

static void stepAxis(Axis &a) {
  float p = (float)(millis() - a.t0) / (float)a.dur;
  if (p >= 1.0f) { a.now = a.to; return; }
  float e = p * p * (3.0f - 2.0f * p);  // smoothstep: eased start and stop
  a.now = a.from + (a.to - a.from) * e;
}

static void writeServos() {
  // Two push rods make nod and tilt: both up = nod, opposite = tilt.
  float left  = aNod.now + aTilt.now;
  float right = aNod.now - aTilt.now;
  sPan.write(90 + PAN_SIGN * (int)aPan.now + trimPan);
  sLeft.write(90 + LEFT_SIGN * (int)left + trimLeft);
  sRight.write(90 + RIGHT_SIGN * (int)right + trimRight);
}

// ---------- serial ----------
String line;

static void reply(JsonDocument &out) {
  serializeJson(out, Serial);
  Serial.print('\n');
}

static void replyErr(const char *err) {
  JsonDocument out;
  out["ok"] = false;
  out["err"] = err;
  reply(out);
}

static void handle(const String &s) {
  JsonDocument doc;
  DeserializationError e = deserializeJson(doc, s);
  if (e) { replyErr("bad_json"); return; }
  const char *cmd = doc["cmd"] | "";
  JsonDocument out;
  out["ok"] = true;

  if (!strcmp(cmd, "ping")) {
    out["fw"] = FW_VERSION;
    out["pan"] = aPan.to;
    out["nod"] = aNod.to;
    out["tilt"] = aTilt.to;
    out["mood"] = faceMoodName();
  } else if (!strcmp(cmd, "look")) {
    uint32_t ms = doc["ms"] | 400;
    float pan  = clampf(doc["pan"]  | aPan.to,  PAN_MIN,  PAN_MAX);
    float nod  = clampf(doc["nod"]  | aNod.to,  NOD_MIN,  NOD_MAX);
    float tilt = clampf(doc["tilt"] | aTilt.to, TILT_MIN, TILT_MAX);
    startMove(aPan, pan, ms);
    startMove(aNod, nod, ms);
    startMove(aTilt, tilt, ms);
    out["pan"] = pan; out["nod"] = nod; out["tilt"] = tilt;
  } else if (!strcmp(cmd, "face")) {
    const char *mood = doc["mood"] | "";
    if (!faceSet(mood)) { replyErr("unknown_mood"); return; }
    out["mood"] = mood;
  } else if (!strcmp(cmd, "trim")) {
    trimPan = doc["pan"] | trimPan;
    trimLeft = doc["left"] | trimLeft;
    trimRight = doc["right"] | trimRight;
    out["pan"] = trimPan; out["left"] = trimLeft; out["right"] = trimRight;
  } else {
    replyErr("unknown_cmd");
    return;
  }
  reply(out);
}

static void readSerial() {
  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      line.trim();
      if (line.length()) handle(line);
      line = "";
    } else if (c != '\r') {
      line += c;
      if (line.length() > 300) { line = ""; replyErr("line_too_long"); }
    }
  }
}

void setup() {
  Serial.begin(115200);
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  for (Servo *s : {&sPan, &sLeft, &sRight}) s->setPeriodHertz(50);
  sPan.attach(PIN_PAN, 500, 2400);
  sLeft.attach(PIN_LEFT, 500, 2400);
  sRight.attach(PIN_RIGHT, 500, 2400);
  writeServos();  // everything to center on boot
  faceBegin();
  faceSet("sleep");
}

void loop() {
  readSerial();
  stepAxis(aPan);
  stepAxis(aNod);
  stepAxis(aTilt);
  writeServos();
  faceTick();
  delay(10);
}
