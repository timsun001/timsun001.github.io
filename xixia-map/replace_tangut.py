#!/usr/bin/env python3
"""Replace all Tangut characters in xixia-map with PNG data URIs."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE, 'index.html')
URI_DIR = os.path.join(BASE, 'images', 'tangut')

# Read URIs
uris = {}
for name in ['xia', 't1', 't2', 't3', 't4', 'xia-terracotta']:
    with open(os.path.join(URI_DIR, f'{name}.uri'), 'r') as f:
        uris[name] = f.read().strip()

xia_black = uris['xia']
xia_terracotta = uris['xia-terracotta']

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Track changes
changes = 0

# === CSS for tangut images ===
tangut_css = '''
/* Tangut character images — zero font dependency, works on all devices */
.tangut-char { display: inline-block; vertical-align: middle; }
.tangut-h1   { height: 30px; width: auto; margin-right: 2px; }
.tangut-sub  { height: 14px; width: auto; }
.tangut-map  { height: 16px; width: auto; margin-right: 2px; }
'''

# Insert CSS before #header h1
if tangut_css.strip() not in html:
    html = html.replace('\n#header h1 {', f'\n{tangut_css}\n#header h1 {{')
    changes += 1
    print("+ Added tangut image CSS")

# === 1. Seal: CSS ===
old_seal_css = ".seal::after {\n  content: '𘜶';\n  position: absolute;\n  inset: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  transform: rotate(-45deg);\n  font-size: 26px;\n  font-weight: 400;\n  color: var(--terracotta);\n  font-family: 'Noto Serif Tangut', serif;\n}"
new_seal_css = ".seal .seal-img {\n  position: absolute;\n  inset: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  transform: rotate(-45deg);\n  width: 32px;\n  height: 32px;\n  margin: auto;\n}"
if old_seal_css in html:
    html = html.replace(old_seal_css, new_seal_css)
    changes += 1
    print("+ Updated seal CSS")
else:
    print("! Seal CSS not found (may have been already patched)")

# === 2. Seal: HTML ===
old_seal_html = '<div class="seal"></div>'
new_seal_html = f'<div class="seal"><img src="{xia_terracotta}" alt="夏" class="seal-img"></div>'
if old_seal_html in html:
    html = html.replace(old_seal_html, new_seal_html)
    changes += 1
    print("+ Updated seal HTML")
else:
    print("! Seal HTML not found")

# === 3. H1 title ===
old_h1 = '<h1>𘜶 西夏遗珍</h1>'
new_h1 = f'<h1><img src="{xia_black}" alt="夏" class="tangut-char tangut-h1"> 西夏遗珍</h1>'
if old_h1 in html:
    html = html.replace(old_h1, new_h1)
    changes += 1
    print("+ Updated H1 title")
else:
    print("! H1 not found")

# === 4. Subtitle ===
subtitle_imgs = (
    f'<img src="{uris["t1"]}" alt="" class="tangut-char tangut-sub">'
    f'<img src="{uris["t2"]}" alt="" class="tangut-char tangut-sub">'
    f'<img src="{xia_black}" alt="夏" class="tangut-char tangut-sub">'
    f'<img src="{uris["t3"]}" alt="" class="tangut-char tangut-sub">'
    f'<img src="{uris["t4"]}" alt="" class="tangut-char tangut-sub">'
)
old_sub = '<div class="subtitle">𗴂𗹭𘜶𗴲𗂧 · Western Xia</div>'
new_sub = f'<div class="subtitle">{subtitle_imgs} · Western Xia</div>'
if old_sub in html:
    html = html.replace(old_sub, new_sub)
    changes += 1
    print("+ Updated subtitle")
else:
    print("! Subtitle not found")

# === 5. Map label ===
old_map = '<span class="map-label">𘜶 疆域</span>'
new_map = f'<span class="map-label"><img src="{xia_black}" alt="夏" class="tangut-char tangut-map"> 疆域</span>'
if old_map in html:
    html = html.replace(old_map, new_map)
    changes += 1
    print("+ Updated map label")
else:
    print("! Map label not found")

# === 6. Font-family cleanups ===
for old_ff, new_ff, desc in [
    ('font-family: var(--font-tangut), var(--font-display);', 'font-family: var(--font-display);', 'h1'),
    ('font-family: var(--font-tangut), var(--font-en);', 'font-family: var(--font-en);', 'subtitle'),
]:
    if old_ff in html:
        html = html.replace(old_ff, new_ff)
        changes += 1
        print(f"+ Cleaned font-family: {desc}")
    else:
        print(f"! Font-family {desc} already clean")

# Write back
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone. {changes} changes made.")

# Verify
import re
remaining = set(re.findall(r'[\U00017000-\U00018AFF]', html))
if remaining:
    print(f"WARNING: {len(remaining)} Tangut chars still present!")
    for ch in remaining:
        lines = [i+1 for i, line in enumerate(html.split('\n')) if ch in line]
        print(f"  U+{ord(ch):05X} on lines: {lines}")
else:
    print("✓ Zero Tangut characters remaining in source")
