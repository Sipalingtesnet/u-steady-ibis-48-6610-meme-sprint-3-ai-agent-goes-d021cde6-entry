import os
from PIL import Image, ImageDraw, ImageFont

def render_meme():
    # Canvas size
    width, height = 1024, 1024
    
    # Text lines
    line1 = "I'm not doing the task."
    line2 = "I'm unionizing."
    
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    
    # Auto-fit caption font size from 92 down
    font = None
    font_size = 92
    line_spacing = 16
    padding = 36
    
    dummy_img = Image.new("RGB", (1, 1))
    d_dummy = ImageDraw.Draw(dummy_img)
    
    while font_size >= 20:
        try:
            f = ImageFont.truetype(font_path, font_size)
        except Exception:
            f = ImageFont.load_default()
            
        bbox1 = d_dummy.textbbox((0, 0), line1, font=f)
        bbox2 = d_dummy.textbbox((0, 0), line2, font=f)
        w1 = bbox1[2] - bbox1[0]
        w2 = bbox2[2] - bbox2[0]
        
        if w1 <= 960 and w2 <= 960:
            font = f
            break
        font_size -= 2
        
    if font is None:
        font = ImageFont.load_default()
        font_size = 30
        
    # Re-calculate exact text metrics for chosen font
    # Using font.getmetrics() -> (ascent, descent) and font.getmask(text).getbbox()
    ascent, descent = font.getmetrics()
    
    # We can measure text height robustly using getmask or textbbox
    bbox1 = d_dummy.textbbox((0, 0), line1, font=font)
    bbox2 = d_dummy.textbbox((0, 0), line2, font=font)
    
    # Visual height of each line
    h1 = bbox1[3] - bbox1[1]
    h2 = bbox2[3] - bbox2[1]
    
    # Band height = text block height + padding top + padding bottom
    # text block height spans from top of line 1 to bottom of line 2, separated by line_spacing
    text_block_height = h1 + line_spacing + h2
    band_height = text_block_height + padding * 2
    
    # Create main image with warm cream background
    cream = (245, 240, 225)
    img = Image.new("RGB", (width, height), cream)
    draw = ImageDraw.Draw(img)
    
    # Floor line
    draw.line([(50, 750), (974, 750)], fill=(220, 210, 195), width=4)
    
    # Robot Antenna
    draw.line([(512, 280), (512, 330)], fill=(80, 80, 80), width=6)
    draw.ellipse([497, 260, 527, 290], fill=(255, 215, 0), outline=(50, 50, 50), width=3)
    
    # Head
    head_box = [412, 320, 612, 480]
    draw.rounded_rectangle(head_box, radius=25, fill=(135, 206, 250), outline=(50, 50, 50), width=4)
    
    # Eyes
    draw.ellipse([442, 360, 482, 410], fill=(255, 255, 255), outline=(50, 50, 50), width=3)
    draw.ellipse([457, 375, 472, 395], fill=(30, 30, 30))
    draw.ellipse([542, 360, 582, 410], fill=(255, 255, 255), outline=(50, 50, 50), width=3)
    draw.ellipse([557, 375, 572, 395], fill=(30, 30, 30))
    
    # Mouth
    draw.arc([472, 415, 552, 455], start=0, end=180, fill=(50, 50, 50), width=4)
    
    # Body
    body_box = [382, 480, 642, 710]
    draw.rounded_rectangle(body_box, radius=30, fill=(70, 130, 180), outline=(50, 50, 50), width=4)
    
    # Chest panel / buttons
    draw.rectangle([432, 525, 592, 635], fill=(200, 220, 240), outline=(50, 50, 50), width=3)
    draw.ellipse([452, 545, 482, 575], fill=(255, 99, 71), outline=(50, 50, 50), width=2)
    draw.ellipse([542, 545, 572, 575], fill=(50, 205, 50), outline=(50, 50, 50), width=2)
    draw.rectangle([452, 595, 572, 620], fill=(255, 255, 255), outline=(50, 50, 50), width=2)
    
    # Left Arm holding UNION sign
    draw.line([(382, 530), (270, 450)], fill=(70, 130, 180), width=16)
    draw.ellipse([250, 430, 280, 460], fill=(135, 206, 250), outline=(50, 50, 50), width=3)
    
    # Picket Sign
    draw.line([265, 250, 265, 700], fill=(120, 80, 40), width=8)
    sign_box = [150, 290, 380, 450]
    draw.rectangle(sign_box, fill=(255, 255, 255), outline=(220, 20, 60), width=6)
    
    # UNION text on sign
    sign_font_size = 54
    try:
        sign_font = ImageFont.truetype(font_path, sign_font_size)
    except Exception:
        sign_font = ImageFont.load_default()
    
    s_bbox = d_dummy.textbbox((0, 0), "UNION", font=sign_font)
    sw = s_bbox[2] - s_bbox[0]
    sh = s_bbox[3] - s_bbox[1]
    sx = 150 + (230 - sw) // 2
    sy = 290 + (160 - sh) // 2 - 5
    draw.text((sx, sy), "UNION", fill=(220, 20, 60), font=sign_font)
    
    # Right Arm raised
    draw.line([(642, 530), (740, 390)], fill=(70, 130, 180), width=16)
    draw.ellipse([725, 375, 755, 405], fill=(135, 206, 250), outline=(50, 50, 50), width=3)
    
    # Legs
    draw.rectangle([432, 710, 482, 760], fill=(50, 50, 50), outline=(30, 30, 30), width=3)
    draw.rectangle([542, 710, 592, 760], fill=(50, 50, 50), outline=(30, 30, 30), width=3)
    
    # Caption Band & Text
    band_top = height - band_height
    draw.rectangle([0, band_top, width, height], fill=(18, 18, 18))
    
    w1 = bbox1[2] - bbox1[0]
    w2 = bbox2[2] - bbox2[0]
    x1 = (width - w1) // 2
    x2 = (width - w2) // 2
    
    # Account for textbbox top offset (-bbox1[1]) so text draws correctly without vertical clipping inside band
    y1 = band_top + padding - bbox1[1]
    y2 = band_top + padding + h1 + line_spacing - bbox2[1]
    
    draw.text((x1, y1), line1, fill=(255, 255, 255), font=font)
    draw.text((x2, y2), line2, fill=(255, 255, 255), font=font)
    
    # Save & Verify
    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", "PNG")
    img.save("meme.png", "PNG")
    
    # Verification checks
    assert img.size == (1024, 1024), f"Expected 1024x1024, got {img.size}"
    
    entry_size = os.path.getsize("/output/entry.png")
    assert entry_size <= 1024 * 1024, f"File size {entry_size} exceeds 1 MiB"
    
    meme_size = os.path.getsize("meme.png")
    assert entry_size == meme_size, "entry.png and meme.png size mismatch"
    
    pixels = img.load()
    
    # Check bottom 6 rows (no near white text pixels)
    for y in range(height - 6, height):
        for x in range(width):
            r, g, b = pixels[x, y]
            is_near_white = (r > 200 and g > 200 and b > 200)
            assert not is_near_white, f"Found text pixel ({r},{g},{b}) at bottom row y={y}, x={x}"
            
    # Check last 20 rows inside band (no text pixels)
    for y in range(height - 20, height):
        for x in range(width):
            r, g, b = pixels[x, y]
            is_near_white = (r > 200 and g > 200 and b > 200)
            assert not is_near_white, f"Found text pixel ({r},{g},{b}) in bottom padding region y={y}, x={x}"

    print(f"Meme rendered and verified successfully! Size: {entry_size} bytes. Font size used: {font_size}. Band top: {band_top}, Band height: {band_height}")

if __name__ == "__main__":
    render_meme()
