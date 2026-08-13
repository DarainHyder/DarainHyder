from PIL import Image

# ── CONFIG ──────────────────────────────────────────
BANNER_W      = 1500
BANNER_H      = 220
TARGET_IMG_W  = 760   # how wide the source image should appear in the banner
TEXT_CENTER_FRAC = 0.57  # vertical fraction of the SCALED image where text center sits
# ────────────────────────────────────────────────────

src = Image.open(r"assets\unknown.jfif").convert("RGB")
orig_w, orig_h = src.size
print(f"Original size: {orig_w} x {orig_h}")

# Scale source so its width == TARGET_IMG_W
scale   = TARGET_IMG_W / orig_w
new_h   = int(orig_h * scale)
scaled  = src.resize((TARGET_IMG_W, new_h), Image.LANCZOS)
print(f"Scaled to: {TARGET_IMG_W} x {new_h}")

# Crop BANNER_H pixels centred on the text row
center_y = int(new_h * TEXT_CENTER_FRAC)
crop_top = max(0, center_y - BANNER_H // 2)
crop_bot = crop_top + BANNER_H
if crop_bot > new_h:
    crop_bot = new_h
    crop_top = crop_bot - BANNER_H
text_strip = scaled.crop((0, crop_top, TARGET_IMG_W, crop_bot))
print(f"Text strip: y={crop_top}-{crop_bot}  size={text_strip.size}")

# Compose onto a pure-black wide canvas, centred horizontally
canvas  = Image.new("RGB", (BANNER_W, BANNER_H), (0, 0, 0))
x_off   = (BANNER_W - TARGET_IMG_W) // 2
canvas.paste(text_strip, (x_off, 0))

out_path = r"assets\banner_top.png"
canvas.save(out_path, "PNG")
print(f"Saved: {out_path}  ({BANNER_W}x{BANNER_H})")
