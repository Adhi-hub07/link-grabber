from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

S = 256
img = Image.new("RGB", (S, S), "#14101a")
draw = ImageDraw.Draw(img)

# rounded-square gradient background (pink -> deep purple)
for y in range(S):
    t = y / S
    r = int(40 + (18 - 40) * t)
    g = int(22 + (12 - 22) * t)
    b = int(52 + (30 - 52) * t)
    draw.line([(0, y), (S, y)], fill=(r, g, b))

mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([8, 8, S - 8, S - 8], radius=52, fill=255)

# glow
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-60, -60, 180, 180], fill=(255, 111, 165, 90))
gd.ellipse([110, 90, 320, 300], fill=(143, 211, 255, 70))
glow = glow.filter(ImageFilter.GaussianBlur(40))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
draw = ImageDraw.Draw(img)

# download arrow (white with pink outline)
c = S // 2
shaft_w, shaft_h = 36, 86
x0, y0 = c - shaft_w // 2, 56
draw.rounded_rectangle([x0, y0, x0 + shaft_w, y0 + shaft_h], radius=10, fill="#ffffff")
head_w = 120
hy = y0 + shaft_h - 8
draw.polygon([(c - head_w // 2, hy), (c + head_w // 2, hy), (c, hy + 74)], fill="#ffffff")

# small sparkle dots
draw.ellipse([48, 44, 64, 60], fill="#ff9ec7")
draw.ellipse([196, 176, 212, 192], fill="#8fd3ff")

img = Image.composite(img, Image.new("RGB", (S, S), (0, 0, 0)), mask)
img = img.convert("RGBA")
img.putalpha(mask)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.ico")
img.save(out, sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
print("saved:", out)