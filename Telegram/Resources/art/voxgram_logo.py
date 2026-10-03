#!/usr/bin/env python3
# Generates every app icon / logo raster from the Voxgram vector logo.
# Requires: pip install pillow cairosvg
# Usage:    python3 Telegram/Resources/art/voxgram_logo.py
import io
import os

import cairosvg
from PIL import Image, ImageChops

ART = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(ART)
MAC = os.path.join(RES, '..', 'Telegram', 'Images.xcassets', 'AppIcon.appiconset')
UWP = os.path.join(RES, 'uwp', 'AppX', 'Assets')
ICONS = os.path.join(RES, 'icons')

# The logo is drawn in a 640x640 box: a circle of radius 320 with a white
# speech bubble and a zigzag cut through it.
GRADIENT = '''<linearGradient id="g" gradientUnits="userSpaceOnUse"
    x1="0" y1="0" x2="0" y2="640">
  <stop offset="0" stop-color="#3BB1F1"/>
  <stop offset="1" stop-color="#1E88D2"/>
</linearGradient>'''
BUBBLE = ('<rect x="131" y="201" width="378" height="228" rx="40"/>'
          '<path d="M211 420 L300 420 L211 496 Z"/>')
ZIGZAG_POINTS = '220,314 272,264 324,322 376,264 428,314'
ZIGZAG_WIDTH = 30
BUBBLE_BOX = (131, 201, 509, 496)  # left, top, right, bottom


def svg(body, view, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}">'
            f'<defs>{defs}</defs>{body}</svg>')


def zigzag(color):
    return (f'<polyline points="{ZIGZAG_POINTS}" fill="none" '
            f'stroke="{color}" stroke-width="{ZIGZAG_WIDTH}" '
            'stroke-linecap="round" stroke-linejoin="round"/>')


def glyph_on(background):
    # White bubble with the zigzag painted in the background fill.
    return f'<g fill="#fff">{BUBBLE}</g>{zigzag(background)}'


def circle_svg():
    return svg('<circle cx="320" cy="320" r="320" fill="url(#g)"/>'
               + glyph_on('url(#g)'), '0 0 640 640', GRADIENT)


def mac_svg():
    # macOS icon grid: 824x824 rounded square inside 1024x1024.
    s = 824 / 640
    return svg('<rect x="100" y="100" width="824" height="824" rx="185" '
               'fill="url(#mg)"/>'
               f'<g transform="translate(100 100) scale({s})">'
               + glyph_on('url(#g)') + '</g>',
               '0 0 1024 1024',
               GRADIENT + GRADIENT.replace('id="g"', 'id="mg"')
               .replace('y1="0"', 'y1="100"').replace('y2="640"', 'y2="924"'))


def glyph_svgs():
    # White bubble and the zigzag as separate layers: the zigzag is then
    # punched out of the bubble alpha (cairosvg masks are unreliable).
    l, t, r, b = BUBBLE_BOX
    view = f'{l} {t} {r - l} {b - t}'
    return (svg(f'<g fill="#fff">{BUBBLE}</g>', view),
            svg(zigzag('#fff'), view))


def render(svg_text, width, height=None):
    height = height or width
    if isinstance(svg_text, tuple):
        bubble, hole = (render(part, width, height) for part in svg_text)
        alpha = ImageChops.subtract(bubble.getchannel('A'),
                                    hole.getchannel('A'))
        bubble.putalpha(alpha)
        return bubble
    data = cairosvg.svg2png(bytestring=svg_text.encode(),
                            output_width=width, output_height=height)
    return Image.open(io.BytesIO(data)).convert('RGBA')


def padded(svg_text, size, margin):
    image = Image.new('RGBA', (size, size))
    inner = size - 2 * margin
    image.alpha_composite(render(svg_text, inner), (margin, margin))
    return image


def fitted(svg_text, size, ratio):
    # Glyph scaled to `ratio` of the canvas width, centered.
    l, t, r, b = BUBBLE_BOX
    w = round(size * ratio)
    h = round(w * (b - t) / (r - l))
    image = Image.new('RGBA', (size, size))
    image.alpha_composite(render(svg_text, w, h),
                          ((size - w) // 2, (size - h) // 2))
    return image


def save(image, path):
    image.save(path, optimize=True)
    print('wrote', os.path.relpath(path, os.path.join(RES, '..', '..')))


def margin_for(size):
    # Telegram keeps a 10/256 transparent margin around the circle.
    return 0 if size <= 16 else round(size * 10 / 256)


def main():
    circle = circle_svg()
    with open(os.path.join(ART, 'voxgram_logo.svg'), 'w') as f:
        f.write(circle)

    for base in (16, 32, 48, 64, 128, 256, 512):
        save(padded(circle, base, margin_for(base)),
             os.path.join(ART, f'icon{base}.png'))
        save(padded(circle, base * 2, margin_for(base * 2)),
             os.path.join(ART, f'icon{base}@2x.png'))
    save(padded(circle, 256, 10), os.path.join(ART, 'logo_256.png'))
    save(padded(circle, 256, 0), os.path.join(ART, 'logo_256_no_margin.png'))
    save(padded(circle, 1024, 50), os.path.join(ART, 'icon_round512@2x.png'))

    ico = padded(circle, 256, margin_for(256))
    ico.save(os.path.join(ART, 'icon256.ico'),
             sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (256, 256)])
    print('wrote icon256.ico')

    mac = mac_svg()
    for name in os.listdir(MAC):
        if name.endswith('.png'):
            size = Image.open(os.path.join(MAC, name)).size[0]
            save(render(mac, size), os.path.join(MAC, name))

    glyph = glyph_svgs()
    for folder, ratio in (('logo', 0.68), ('logo150', 0.68), ('logo44', 0.86)):
        path = os.path.join(UWP, folder)
        for name in sorted(os.listdir(path)):
            size = Image.open(os.path.join(path, name)).size[0]
            if 'altform-unplated' in name:
                image = padded(circle, size, 0)
            else:
                image = fitted(glyph, size, ratio)
            save(image, os.path.join(path, name))

    # Intro screen cover: white bubble mask, colored by the style.
    l, t, r, b = BUBBLE_BOX
    # codegen_style requires @2x/@3x to be exact multiples of 1x.
    width = round(120 * (r - l) / (b - t))
    for scale, suffix in ((1, ''), (2, '@2x'), (3, '@3x')):
        h = 120 * scale
        w = width * scale
        save(render(glyph, w, h),
             os.path.join(ICONS, f'intro_voxgram_logo{suffix}.png'))


if __name__ == '__main__':
    main()
