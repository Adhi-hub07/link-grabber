from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1280, 320
img = Image.new("RGB", (W, H), "#14101a")
draw = ImageDraw.Draw(img)

# gradient background: deep purple -> dark
top = (20, 12, 28)
bottom = (34, 18, 44)
for y in range(H):
    t = y / H
    r = int(top[0] + (bottom[0] - top[0]) * t)
    g = int(top[1] + (bottom[1] - top[1]) * t)
    b = int(top[2] + (bottom[2] - top[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# glow circles (pink / blue)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-200, -150, 400, 250], fill=(255, 111, 165, 60))
gd.ellipse([1000, -100, 1500, 300], fill=(143, 211, 255, 50))
glow = glow.filter(ImageFilter.GaussianBlur(60))
img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))

draw = ImageDraw.Draw(img)

def font(size, bold=True):
    path = r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"
    if not os.path.exists(path):
        path = r"C:\Windows\Fonts\arialbd.ttf"
    return ImageFont.truetype(path, size)

# big title with shadow
f_title = font(96)
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.text((W // 2 + 4, 78 + 4), "ADHI-HUB", font=f_title, fill=(0, 0, 0, 200),
        anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, 200))
shadow = shadow.filter(ImageFilter.GaussianBlur(8))
img.paste(Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB"), (0, 0))
draw = ImageDraw.Draw(img)

draw.text((W // 2, 78), "ADHI-HUB", font=f_title, fill="#ff9ec7", anchor="mm",
          stroke_width=2, stroke_fill="#ff6fa5")

# subtitle
f_sub = font(30, bold=False)
draw.text((W // 2, 195), "⬇  THE ULTIMATE VIDEO & MUSIC DOWNLOADER  ⬇",
          font=f_sub, fill="#c9b8c4", anchor="mm")

# tag line
f_tag = font(22, bold=False)
draw.text((W // 2, 250), "YouTube  •  Instagram  •  TikTok  •  1000+ sites",
          font=f_tag, fill="#8fd3ff", anchor="mm")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "banner.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, "PNG")
print("saved:", out, img.size)