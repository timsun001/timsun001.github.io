#!/usr/bin/env python3
import base64, io, os
from PIL import Image, ImageFont, ImageDraw

font_path = os.path.join(os.path.dirname(__file__), 'NotoSerifTangut.ttf')
output_dir = os.path.join(os.path.dirname(__file__), 'images', 'tangut')
os.makedirs(output_dir, exist_ok=True)

chars = [
    ('\U00018736', 48, 'xia'),
    ('\U00017D02', 32, 't1'),
    ('\U00017E6D', 32, 't2'),
    ('\U00017D32', 32, 't3'),
    ('\U000170A7', 32, 't4'),
]

print("Loading font...")
font_cache = {}
for char, size, name in chars:
    if size not in font_cache:
        font_cache[size] = ImageFont.truetype(font_path, size)
    font = font_cache[size]
    
    bbox = font.getbbox(char)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = size // 4
    img_w = w + pad * 2
    img_h = h + pad * 2
    
    img = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((pad - bbox[0], pad - bbox[1]), char, font=font, fill=(0, 0, 0, 255))
    
    bbox_img = img.getbbox()
    if bbox_img:
        img = img.crop(bbox_img)
    
    png_path = os.path.join(output_dir, f'{name}.png')
    img.save(png_path)
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    uri = f'data:image/png;base64,{b64}'
    
    with open(os.path.join(output_dir, f'{name}.uri'), 'w') as f:
        f.write(uri)
    
    print(f"OK {name} {img.size[0]}x{img.size[1]}px {len(buf.getvalue())}B")

print("ALL DONE")
