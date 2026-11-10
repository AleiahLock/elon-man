// Elon Man printed parts. Parametric OpenSCAD.
// Pick a part, press F6, export STL. All sizes in mm.
// Look: tapered red body, two gold chest chevrons, black base, red head with a gray face bezel.

part = "body"; // [body, chevron, base, head, bezel, yoke, all]

$fn = 72;

// ---- body ----
body_w_bottom = 100;   // width at the waist
body_w_top    = 120;   // width at the shoulders
body_d        = 80;    // depth
body_h        = 180;
corner_r      = 10;
wall          = 2.4;
neck_hole_d   = 30;
channel_depth = 1.2;   // chevron channel cut into the front

// ---- head ----
head_w      = 110;
head_h      = 95;
head_d      = 90;
face_d      = 62;      // hole for the round display (1.28in GC9A01 = ~39 mm active, 2.1in board ~ 60 mm)
cam_slot    = [34, 14];
neck_col_d  = 26;

// ---- base ----
base_w = 150; base_d = 110; base_h = 28;

module rounded_rect(w, d, r) {
  offset(r = r) square([w - 2 * r, d - 2 * r], center = true);
}

module body_solid(inset = 0) {
  s = (body_w_top - 2 * inset) / (body_w_bottom - 2 * inset);
  linear_extrude(height = body_h - inset, scale = [s, 1])
    rounded_rect(body_w_bottom - 2 * inset, body_d - 2 * inset, max(1, corner_r - inset));
}

// A chevron (V pointing down) on the front, in the X-Z plane.
module chevron_shape(z, width = 70, thick = 9, drop = 22) {
  polygon([
    [-width / 2, z], [0, z - drop], [width / 2, z],
    [width / 2, z + thick], [0, z - drop + thick], [-width / 2, z + thick]
  ]);
}

module chevron_prism() {
  // extrude toward the front (-Y) from the middle of the body
  rotate([90, 0, 0]) linear_extrude(height = body_d) {
    chevron_shape(body_h * 0.72);
    chevron_shape(body_h * 0.56);
  }
}

module body() {
  difference() {
    body_solid();
    translate([0, 0, -0.01]) body_solid(wall);            // hollow, open bottom for access
    translate([0, 0, body_h - wall - 1]) cylinder(d = neck_hole_d, h = wall + 3);
    // chevron channels: only the outer skin, only where the prism hits it
    intersection() {
      difference() { body_solid(); body_solid(channel_depth); }
      chevron_prism();
    }
    // cable hole at the back bottom
    translate([0, body_d / 2, 18]) rotate([90, 0, 0]) cylinder(d = 14, h = 10, center = true);
  }
}

module chevron() {
  // print flat in gold, glue into the channel. 0.2 mm smaller than the channel all round.
  linear_extrude(height = channel_depth - 0.1) offset(delta = -0.2) chevron_shape(0);
}

module base() {
  difference() {
    linear_extrude(height = base_h) rounded_rect(base_w, base_d, 12);
    translate([0, 0, 2.4]) linear_extrude(height = base_h) rounded_rect(base_w - 4.8, base_d - 4.8, 10);
    // lip the body sits in
    translate([0, 0, base_h - 4]) linear_extrude(height = 5) rounded_rect(body_w_bottom + 0.6, body_d + 0.6, corner_r);
    // power + USB at the back
    translate([0, base_d / 2, base_h / 2]) cube([40, 10, 14], center = true);
  }
}

module head_solid(inset = 0) {
  scale([(head_w - 2 * inset) / head_w, (head_d - 2 * inset) / head_w, (head_h - 2 * inset) / head_w])
    sphere(d = head_w);
}

module head() {
  difference() {
    head_solid();
    head_solid(wall);
    // face hole, front
    translate([0, -head_d / 2, 0]) rotate([90, 0, 0]) cylinder(d = face_d, h = 30, center = true);
    // camera slot, top
    translate([0, -10, head_h / 2 - 4]) cube([cam_slot[0], cam_slot[1], 20], center = true);
    // neck column, bottom
    translate([0, 0, -head_h / 2]) cylinder(d = neck_col_d + 0.6, h = 20, center = true);
    // flat bottom so it prints
    translate([0, 0, -head_h / 2 - 50 + 4]) cube([200, 200, 100], center = true);
  }
}

module bezel() {
  difference() {
    cylinder(d = face_d + 12, h = 3);
    translate([0, 0, -1]) cylinder(d = face_d - 4, h = 5);
  }
  // locating ring that slides into the face hole
  difference() {
    cylinder(d = face_d - 0.4, h = 6);
    translate([0, 0, -1]) cylinder(d = face_d - 4, h = 8);
  }
}

module yoke() {
  // U-yoke on the pan servo horn, holds the neck column. Print in PETG, 4 walls, 40% infill.
  arm_h = 40; gap = 30; t = 5;
  difference() {
    union() {
      cylinder(d = 44, h = t);
      for (x = [-1, 1]) translate([x * (gap / 2 + t / 2), 0, arm_h / 2]) cube([t, 20, arm_h], center = true);
    }
    translate([0, 0, -1]) cylinder(d = 7, h = t + 2);                 // horn screw + spline clearance
    for (a = [0, 90, 180, 270]) rotate(a) translate([8, 0, -1]) cylinder(d = 2.2, h = t + 2); // horn screws
    for (x = [-1, 1]) translate([x * (gap / 2 + t / 2), 0, arm_h - 8]) rotate([0, 90, 0]) cylinder(d = 3.2, h = t + 2, center = true);
  }
}

if (part == "body") body();
if (part == "chevron") chevron();
if (part == "base") base();
if (part == "head") head();
if (part == "bezel") bezel();
if (part == "yoke") yoke();
if (part == "all") {
  color("black") base();
  color("red") translate([0, 0, base_h - 4]) body();
  color("red") translate([0, 0, base_h - 4 + body_h + head_h / 2 + 10]) head();
}
