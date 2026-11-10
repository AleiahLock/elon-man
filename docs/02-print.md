# 2. Print the body

All parts come from one parametric file: [../hardware/cad/elonman.scad](../hardware/cad/elonman.scad).

1. Install [OpenSCAD](https://openscad.org) (free).
2. Open `elonman.scad`. At the top, set `part = "body";`
3. Press F6 to render, then File > Export > STL.
4. Repeat for `chevron` (print 2), `base`, `head`, `bezel`, `yoke`.
5. `part = "all";` shows the assembled robot so you can check proportions before you print anything.

If your display is a different size, change `face_d`. If your bed is under 130 mm wide, lower `body_w_top` or cut the body in half in your slicer.

## Print settings

| Part | Material | Walls | Infill | Layer | Supports |
|---|---|---|---|---|---|
| Body | Red PLA/PETG | 3 | 15% | 0.2 mm | No (open bottom down) |
| Head | Red PLA/PETG | 3 | 15% | 0.2 mm | Tree supports for the face hole |
| Chevrons x2 | Gold PLA | 2 | 100% | 0.12 mm | No |
| Base | Black PLA | 3 | 15% | 0.2 mm | No |
| Bezel | Gray PLA | 3 | 100% | 0.12 mm | No |
| Yoke | PETG | 4 | 40% | 0.2 mm | No |

The yoke takes the whole head load. Don't print it in PLA.

## Finish

- Light sanding with 220 then 400 grit on the body takes the layer lines off the front.
- Glue the chevrons into their channels with a drop of CA glue. That's the look.
- Melt M3 heat-set inserts into the base lip and the head so you can open it later.

## Let a Bot do the CAD with you

The shapes are simple on purpose. If you want your own look, ask Grok Bot:

> "I'm designing a desk robot body. Here's a photo of the style I want [attach]. Here is my OpenSCAD file [attach elonman.scad]. Change the body to [what you want]. Show me the code first, then the changes I ask for."

OpenSCAD is plain text, so a Bot can write it, fix it, and explain every number.

Next: [3. Wiring](03-wiring.md)
