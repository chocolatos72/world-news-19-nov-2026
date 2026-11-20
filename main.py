#!/usr/bin/env python3
"""THE WORLD TODAY - Thursday 19 November 2026, on one page.

A program that draws a one-page newspaper front page summing up the
world's news of Thursday 19 November 2026: 12 main stories with flat
vector illustrations drawn in code, a world map drawn from real
longitude/latitude outlines, and the remaining 28 stories as a two-column
list with coloured bullets.

Python 3.13, standard library only. No network, no clock, no randomness.
Two runs write byte-identical files.
"""

import os
import struct
import zlib

W, H = 768, 1024

# ---------------------------------------------------------------- palette
PAPER_TOP = (248, 236, 206)
PAPER_BOT = (248, 236, 206)
INK = (30, 36, 48)
NAVY = (28, 58, 96)
RED = (179, 39, 46)
GOLD = (232, 180, 40)
CREAM = (255, 255, 255)
ROSE = (242, 218, 140)
OCEAN = (110, 165, 210)
GRID = (200, 210, 220)

REGION = {
    "ASIA": (205, 60, 60),
    "EUROPE": (60, 110, 190),
    "MIDEAST": (185, 130, 40),
    "AMERICAS": (50, 150, 85),
    "AFRICA": (175, 110, 55),
    "OCEANIA": (135, 95, 180),
    "GLOBAL": (40, 65, 100),
}
REGION_NAME = {
    "ASIA": "ASIA", "EUROPE": "EUROPE", "MIDEAST": "MIDEAST",
    "AMERICAS": "AMERICAS", "AFRICA": "AFRICA", "OCEANIA": "OCEANIA",
    "GLOBAL": "GLOBAL",
}


# ------------------------------------------------------------------- font
# Fresh 5x7 bitmap font, drawn for this entry. Each glyph is 7 rows of
# 5 cells; '#' is ink, '.' is empty. Lowercase sits on the same 7 rows
# with descenders drawn into rows 6-7 where needed.
FONT = {
" ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
"A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
"B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
"C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
"D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
"E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
"F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
"G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
"H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
"I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
"J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
"K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
"L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
"M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
"N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
"O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
"P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
"Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
"R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
"S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
"T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
"U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
"V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
"W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
"X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
"Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
"Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
"0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
"1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
"2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
"3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
"4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
"5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
"6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
"7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
"8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
"9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
"a": (".....", ".....", ".####", "....#", ".####", "#...#", ".####"),
"b": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
"c": (".....", ".....", ".####", "#....", "#....", "#....", ".####"),
"d": ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
"e": (".....", ".....", ".###.", "#...#", "#####", "#....", ".###."),
"f": ("..##.", ".#...", ".#...", "####.", ".#...", ".#...", ".#..."),
"g": (".....", ".....", ".####", "#...#", ".####", "....#", ".###."),
"h": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
"i": ("..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
"j": ("...#.", ".....", "..##.", "...#.", "...#.", "#..#.", ".##.."),
"k": ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
"l": (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
"m": (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
"n": (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
"o": (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
"p": (".....", ".....", "####.", "#...#", "####.", "#....", "#...."),
"q": (".....", ".....", ".####", "#...#", ".####", "....#", "....#"),
"r": (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
"s": (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
"t": (".#...", ".#...", "####.", ".#...", ".#...", ".#...", "..##."),
"u": (".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"),
"v": (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
"w": (".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
"x": (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
"y": (".....", ".....", "#...#", "#...#", ".####", "....#", ".###."),
"z": (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
",": (".....", ".....", ".....", ".....", ".##..", "..#..", ".#..."),
";": (".....", ".##..", ".....", ".##..", ".##..", "..#..", ".#..."),
":": (".....", ".##..", ".....", ".....", ".##..", ".....", "....."),
"!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
"?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
"'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
"\u2019": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
'"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
"\u201c": (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
"\u201d": (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
"-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
"\u2013": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
"\u2014": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
"(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
"/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
"%": ("#...#", "#..#.", "...#.", "..#..", ".#...", "#..#.", "#...#"),
"$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
"&": (".###.", "#...#", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
"+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
"@": (".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".###."),
"*": (".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."),
"#": ("#.#.#", "#.#.#", "#####", "#.#.#", "#####", "#.#.#", "#.#.#"),
"=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
"_": (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
"\u00a3": ("..#..", ".#.#.", ".#...", "####.", ".#...", "#.#..", ".###."),
"\u20ac": (".###.", "#....", "#....", "####.", "#....", "#....", ".###."),
}

CHAR_W = 6  # glyph cell width incl. 1px gap, at scale 1


def text_width(s, scale=1):
    return len(s) * CHAR_W * scale - scale


def draw_text(img, x, y, s, scale=1, color=INK):
    """Draw s at (x, y); top-left of the first glyph cell."""
    cx = x
    for ch in s:
        g = FONT.get(ch)
        if g is None:
            cx += CHAR_W * scale
            continue
        for r in range(7):
            row = g[r]
            for c in range(5):
                if row[c] == "#":
                    img.rect(cx + c * scale, y + r * scale, scale, scale, color)
        cx += CHAR_W * scale


def wrap_text(s, max_w, scale=1):
    """Split s into lines that fit max_w pixels at the given scale."""
    words = s.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ canvas
class Img:
    def __init__(self, w, h, top, bot):
        self.w, self.h = w, h
        self.pix = bytearray(w * h * 3)
        for y in range(h):
            t = y / max(1, h - 1)
            r = round(top[0] + (bot[0] - top[0]) * t)
            g = round(top[1] + (bot[1] - top[1]) * t)
            b = round(top[2] + (bot[2] - top[2]) * t)
            base = y * w * 3
            for x in range(w):
                o = base + x * 3
                self.pix[o] = r
                self.pix[o + 1] = g
                self.pix[o + 2] = b

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = (y * self.w + x) * 3
            self.pix[o] = c[0]
            self.pix[o + 1] = c[1]
            self.pix[o + 2] = c[2]

    def rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            o = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                self.pix[o] = c[0]
                self.pix[o + 1] = c[1]
                self.pix[o + 2] = c[2]
                o += 3

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        if fill:
            for dy in range(-r, r + 1):
                dx = int((r * r - dy * dy) ** 0.5)
                self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, c)
        else:
            for a in range(360):
                import math
                x = round(cx + r * math.cos(math.radians(a)))
                y = round(cy + r * math.sin(math.radians(a)))
                self.set(x, y, c)

    def poly(self, pts, c):
        """Fill a polygon (scanline fill)."""
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                    xs.append(x)
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.rect(int(xs[i]), y, max(1, int(xs[i + 1]) - int(xs[i])), 1, c)

    def ring(self, cx, cy, r, c, w=2):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            for xx in (cx - dx, cx + dx):
                for k in range(w):
                    self.set(xx - k if xx < cx else xx + k, cy + dy, c)


def write_png(img, path):
    raw = bytearray()
    stride = img.w * 3
    for y in range(img.h):
        raw.append(0)
        raw += img.pix[y * stride:(y + 1) * stride]

    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", img.w, img.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ------------------------------------------------------------ illustrations
# Every scene is drawn from shapes only - no text inside any picture,
# so nothing can come out garbled. Each takes the box it may use.
SKY = (150, 195, 235)
PALE = (255, 240, 180)
SAND = (240, 200, 120)
SEA = (40, 120, 200)


def scene_summit(img, x, y, w, h):
    img.rect(x, y, w, h, SKY)
    # three flags behind the table: US (stripes + canton), China (red + star),
    # Russia (white-blue-red tricolour)
    fx = x + int(w * 0.16)
    img.rect(fx, y + int(h * 0.10), 3, int(h * 0.42), INK)
    for i, c in enumerate(((179, 39, 46), (255, 255, 255), (179, 39, 46))):
        img.rect(fx + 3, y + int(h * 0.10) + i * int(h * 0.055), int(w * 0.16), int(h * 0.055), c)
    img.rect(fx + 3, y + int(h * 0.10), int(w * 0.07), int(h * 0.08), (0, 40, 104))
    fx = x + int(w * 0.48)
    img.rect(fx, y + int(h * 0.10), 3, int(h * 0.42), INK)
    img.rect(fx + 3, y + int(h * 0.10), int(w * 0.16), int(h * 0.16), (222, 41, 16))
    img.circle(fx + 3 + int(w * 0.04), y + int(h * 0.16), 3, (255, 215, 0))
    fx = x + int(w * 0.80)
    img.rect(fx, y + int(h * 0.10), 3, int(h * 0.42), INK)
    for i, c in enumerate(((255, 255, 255), (0, 57, 166), (213, 0, 50))):
        img.rect(fx + 3, y + int(h * 0.10) + i * int(h * 0.055), int(w * 0.16), int(h * 0.055), c)
    # table
    img.rect(x + int(w * 0.08), y + int(h * 0.62), int(w * 0.84), int(h * 0.30), (120, 50, 40))
    img.rect(x + int(w * 0.08), y + int(h * 0.62), int(w * 0.84), 3, (150, 110, 70))
    # three seated figures
    for i, suit in enumerate(((27, 42, 74), (179, 39, 46), (70, 70, 78))):
        cx = x + int(w * (0.22 + 0.28 * i))
        img.circle(cx, y + int(h * 0.44), int(h * 0.11), (233, 196, 164))
        img.poly([(cx - int(w * 0.11), y + int(h * 0.62)), (cx + int(w * 0.11), y + int(h * 0.62)),
                  (cx + int(w * 0.07), y + int(h * 0.52)), (cx - int(w * 0.07), y + int(h * 0.52))], suit)
    # microphones, name plates and a gold emblem on the table
    for i, suit in enumerate(((27, 42, 74), (179, 39, 46), (70, 70, 78))):
        cx = x + int(w * (0.22 + 0.28 * i))
        mx = cx + int(w * 0.08)
        img.line(mx, y + int(h * 0.62), mx, y + int(h * 0.52), (40, 40, 48))
        img.circle(mx, y + int(h * 0.51), 3, (40, 40, 48))
        img.rect(cx - int(w * 0.05), y + int(h * 0.70), int(w * 0.10), int(h * 0.08), (255, 255, 255))
        img.rect(cx - int(w * 0.05), y + int(h * 0.70), int(w * 0.10), 2, suit)
    img.circle(x + w // 2, y + int(h * 0.86), 4, (255, 200, 0))
    img.rect(x + int(w * 0.08), y + int(h * 0.92), int(w * 0.84), int(h * 0.06), (179, 39, 46))
    img.rect(x, y, int(w * 0.05), h, (30, 50, 110))
    img.rect(x + w - int(w * 0.05), y, int(w * 0.05), h, (30, 50, 110))


def scene_justice(img, x, y, w, h):
    # deep navy court backdrop so the gold scales stand out
    img.rect(x, y, w, h, (45, 65, 115))
    img.circle(x + w // 2, y + int(h * 0.45), int(h * 0.38), (70, 95, 150))
    for sx, sy in ((0.12, 0.15), (0.88, 0.12), (0.20, 0.80), (0.85, 0.82), (0.08, 0.45)):
        img.circle(x + int(w * sx), y + int(h * sy), 2, (255, 255, 255))
    gold = (255, 200, 0)
    cx, top = x + w // 2, y + int(h * 0.14)
    img.rect(x + int(w * 0.30), y + int(h * 0.82), int(w * 0.40), int(h * 0.10), gold)
    img.rect(cx - 2, top, 4, int(h * 0.68), gold)
    img.rect(x + int(w * 0.16), top, int(w * 0.68), 4, gold)
    img.circle(cx, top, 4, gold)
    for sgn in (-1, 1):
        px = cx + sgn * int(w * 0.30)
        img.line(px, top + 4, px, top + int(h * 0.30), gold)
        img.line(px - int(w * 0.10), top + int(h * 0.30), px + int(w * 0.10), top + int(h * 0.30), gold)
        img.poly([(px - int(w * 0.11), top + int(h * 0.30)), (px + int(w * 0.11), top + int(h * 0.30)),
                  (px, top + int(h * 0.42))], (220, 160, 20))
    # gavel: head, handle and sound block, lower right
    img.rect(x + int(w * 0.72), y + int(h * 0.60), int(w * 0.16), 6, (150, 110, 40))
    img.line(x + int(w * 0.74), y + int(h * 0.60), x + int(w * 0.88), y + int(h * 0.48), (150, 110, 40))
    img.rect(x + int(w * 0.70), y + int(h * 0.74), int(w * 0.22), 4, (120, 82, 52))
    for sx in (0.02, 0.92):
        img.rect(x + int(w * sx), y + int(h * 0.20), int(w * 0.05), int(h * 0.62), (120, 140, 180))
        img.rect(x + int(w * sx) - 3, y + int(h * 0.18), int(w * 0.05) + 6, 5, (100, 120, 160))

def scene_bridge(img, x, y, w, h):
    img.rect(x, y, w, h, SKY)
    img.rect(x, y + int(h * 0.72), w, int(h * 0.28), SEA)
    for i in range(4):
        img.line(x + int(w * (0.05 + 0.25 * i)), y + int(h * 0.76), x + int(w * (0.20 + 0.25 * i)), y + int(h * 0.76), (255, 255, 255))
    deck = y + int(h * 0.55)
    img.rect(x + int(w * 0.04), deck, int(w * 0.34), 6, (90, 90, 96))
    img.rect(x + int(w * 0.62), deck, int(w * 0.34), 6, (90, 90, 96))
    img.line(x + int(w * 0.38), deck, x + int(w * 0.46), deck + int(h * 0.16), (90, 90, 96))
    img.line(x + int(w * 0.62), deck, x + int(w * 0.54), deck + int(h * 0.16), (90, 90, 96))
    for fx in (0.12, 0.72):
        img.rect(x + int(w * fx), y + int(h * 0.30), 5, int(h * 0.26), (70, 70, 78))
    img.rect(x + int(w * 0.08), deck - int(h * 0.12), int(w * 0.14), int(h * 0.12), (179, 39, 46))
    for wx in (0.10, 0.14, 0.18):
        img.rect(x + int(w * wx), deck - int(h * 0.09), int(w * 0.03), int(h * 0.05), (255, 255, 255))
    img.circle(x + int(w * 0.50), y + int(h * 0.42), 6, (200, 200, 200))
    img.circle(x + int(w * 0.52), y + int(h * 0.34), 5, (220, 220, 220))
    img.circle(x + int(w * 0.48), y + int(h * 0.28), 4, (235, 235, 235))
    img.line(x + int(w * 0.85), y + int(h * 0.10), x + int(w * 0.55), y + int(h * 0.45), (255, 255, 255))
    for dx, dy, r in ((0.50, 0.30, 9), (0.55, 0.22, 7), (0.46, 0.24, 6)):
        img.circle(x + int(w * dx), y + int(h * dy), r, (200, 200, 200))
    img.circle(x + int(w * 0.50), y + int(h * 0.40), 5, (255, 140, 0))
    img.rect(x + int(w * 0.66), y + int(h * 0.80), int(w * 0.18), 6, (60, 60, 70))
    img.rect(x + int(w * 0.72), y + int(h * 0.74), int(w * 0.05), int(h * 0.06), (60, 60, 70))
    img.line(x + int(w * 0.10), y + int(h * 0.88), x + int(w * 0.30), y + int(h * 0.88), (255, 255, 255))
    img.line(x + int(w * 0.45), y + int(h * 0.94), x + int(w * 0.65), y + int(h * 0.94), (255, 255, 255))


def scene_chart(img, x, y, w, h):
    img.rect(x, y, w, h, PALE)
    img.line(x + int(w * 0.10), y + int(h * 0.85), x + int(w * 0.92), y + int(h * 0.85), INK)
    img.line(x + int(w * 0.10), y + int(h * 0.85), x + int(w * 0.10), y + int(h * 0.10), INK)
    bars = [0.22, 0.38, 0.55, 0.78]
    for i, b in enumerate(bars):
        bx = x + int(w * (0.18 + 0.18 * i))
        bh = int(h * b)
        img.rect(bx, y + int(h * 0.85) - bh, int(w * 0.10), bh, (30, 120, 220) if i < 3 else (0, 180, 90))
    img.line(x + int(w * 0.16), y + int(h * 0.66), x + int(w * 0.84), y + int(h * 0.14), (179, 39, 46))
    img.line(x + int(w * 0.84), y + int(h * 0.14), x + int(w * 0.74), y + int(h * 0.14), (179, 39, 46))
    img.line(x + int(w * 0.84), y + int(h * 0.14), x + int(w * 0.84), y + int(h * 0.24), (179, 39, 46))
    img.circle(x + int(w * 0.86), y + int(h * 0.10), 5, (255, 200, 0))
    img.rect(x + int(w * 0.10), y + int(h * 0.92), int(w * 0.80), 2, (30, 120, 220))
    img.poly([(x + int(w * 0.12), y + int(h * 0.10)), (x + int(w * 0.16), y + int(h * 0.04)),
              (x + int(w * 0.20), y + int(h * 0.10))], (30, 132, 73))


def scene_controller(img, x, y, w, h):
    img.rect(x, y, w, h, (255, 130, 50))
    img.circle(x + int(w * 0.78), y + int(h * 0.18), int(h * 0.12), (255, 220, 120))
    for i, bh in enumerate((0.30, 0.45, 0.38, 0.55, 0.42)):
        bx = x + int(w * (0.06 + 0.19 * i))
        img.rect(bx, y + h - int(h * bh), int(w * 0.14), int(h * bh), (70, 45, 110))
        for wy in range(3):
            img.rect(bx + 2, y + h - int(h * bh) + 4 + wy * 6, 2, 2, (255, 220, 120))
    cy = y + int(h * 0.60)
    img.rect(x + int(w * 0.18), cy - int(h * 0.14), int(w * 0.64), int(h * 0.30), (230, 230, 235))
    img.circle(x + int(w * 0.18), cy, int(h * 0.14), (230, 230, 235))
    img.circle(x + int(w * 0.82), cy, int(h * 0.14), (230, 230, 235))
    img.rect(x + int(w * 0.26), cy - 3, 12, 6, INK)
    img.rect(x + int(w * 0.26) + 3, cy - 9, 6, 18, INK)
    for dx, dy, c in ((0.66, -0.05, (255, 90, 90)), (0.72, 0.02, (90, 200, 120)), (0.60, 0.02, (90, 140, 255)), (0.66, 0.09, (255, 200, 60))):
        img.circle(x + int(w * dx), cy + int(h * dy), 4, c)
    img.circle(x + int(w * 0.40), cy + int(h * 0.06), 5, (90, 90, 96))
    img.circle(x + int(w * 0.52), cy - int(h * 0.06), 5, (90, 90, 96))
    img.rect(x + int(w * 0.05), y + int(h * 0.06), int(w * 0.16), int(h * 0.20), (200, 200, 210))
    img.circle(x + int(w * 0.13), y + int(h * 0.16), 4, (90, 140, 255))
    img.rect(x + int(w * 0.05), y + int(h * 0.06), int(w * 0.16), 3, (179, 39, 46))


def scene_cyclone(img, x, y, w, h):
    import math
    img.rect(x, y, w, h, (150, 200, 245))
    cx, cy = x + w // 2, y + int(h * 0.42)
    for k in range(1, 5):
        r = int(h * 0.08 * k)
        img.ring(cx, cy, r, (255, 255, 255), 3)
    img.circle(cx, cy, int(h * 0.07), (90, 120, 150))
    img.rect(x, y + int(h * 0.78), w, int(h * 0.22), SEA)
    for i in range(5):
        px = x + int(w * (0.08 + 0.20 * i))
        img.line(px, y + int(h * 0.80), px + 8, y + int(h * 0.86), (255, 255, 255))
        img.line(px + 30, y + int(h * 0.90), px + 38, y + int(h * 0.96), (255, 255, 255))
    for i in range(6):
        rx = x + int(w * (0.10 + 0.15 * i))
        img.line(rx, y + int(h * 0.06), rx - 3, y + int(h * 0.12), (120, 150, 180))
    img.line(x + int(w * 0.12), y + int(h * 0.78), x + int(w * 0.15), y + int(h * 0.58), (120, 82, 52))
    img.line(x + int(w * 0.15), y + int(h * 0.58), x + int(w * 0.08), y + int(h * 0.54), (30, 132, 73))
    img.line(x + int(w * 0.15), y + int(h * 0.58), x + int(w * 0.22), y + int(h * 0.54), (30, 132, 73))
    img.line(x + int(w * 0.15), y + int(h * 0.58), x + int(w * 0.15), y + int(h * 0.50), (30, 132, 73))


def scene_tower(img, x, y, w, h):
    img.rect(x, y, w, h, SKY)
    for i, bh in enumerate((0.30, 0.45, 0.35)):
        bx = x + int(w * (0.05 + 0.30 * i))
        img.rect(bx, y + h - int(h * bh), int(w * 0.22), int(h * bh), (90, 100, 120))
    tx = x + int(w * 0.42)
    img.poly([(tx, y + int(h * 0.18)), (tx + int(w * 0.16), y + int(h * 0.18)),
              (tx + int(w * 0.13), y + h), (tx + int(w * 0.03), y + h)], (60, 70, 96))
    for r in range(6):
        for c in range(2):
            img.rect(tx + 3 + c * 7, y + int(h * 0.24) + r * 10, 4, 5, (255, 220, 120))
    bx, by = x + int(w * 0.50), y + int(h * 0.10)
    for ang in range(0, 360, 30):
        import math
        ex = bx + int(14 * math.cos(math.radians(ang)))
        ey = by + int(14 * math.sin(math.radians(ang)))
        img.line(bx, by, ex, ey, (255, 170, 60))
    img.circle(bx, by, 7, (255, 120, 40))
    for dx, dy, r in ((-0.10, 0.06, 8), (0.12, 0.14, 6), (0.02, 0.02, 5)):
        img.circle(bx + int(w * dx), by + int(h * dy), r, (190, 190, 190))
    img.rect(x + int(w * 0.06), y + int(h * 0.45), int(w * 0.12), int(h * 0.55), (80, 90, 110))
    for r in range(4):
        img.rect(x + int(w * 0.08), y + int(h * 0.50) + r * 10, 4, 5, (255, 220, 120))
    img.rect(x + int(w * 0.74), y + int(h * 0.12), int(w * 0.14), 5, (60, 60, 70))
    img.line(x + int(w * 0.72), y + int(h * 0.12), x + int(w * 0.90), y + int(h * 0.12), (60, 60, 70))


def scene_tents(img, x, y, w, h):
    img.rect(x, y, w, h, (120, 180, 235))
    img.rect(x, y + int(h * 0.72), w, int(h * 0.28), SAND)
    for i, tc in enumerate(((255, 120, 40), (0, 165, 175), (255, 255, 255))):
        tx = x + int(w * (0.10 + 0.30 * i))
        tw = int(w * 0.26)
        img.poly([(tx, y + int(h * 0.72)), (tx + tw, y + int(h * 0.72)), (tx + tw // 2, y + int(h * 0.40))], tc)
        img.poly([(tx + tw // 2 - 5, y + int(h * 0.72)), (tx + tw // 2 + 5, y + int(h * 0.72)),
                  (tx + tw // 2, y + int(h * 0.56))], (120, 82, 52))
    img.rect(x + int(w * 0.72), y + int(h * 0.58), int(w * 0.18), int(h * 0.14), (150, 110, 70))
    img.rect(x + int(w * 0.79), y + int(h * 0.58), 3, int(h * 0.14), (255, 255, 255))
    img.rect(x + int(w * 0.72), y + int(h * 0.63), int(w * 0.18), 3, (255, 255, 255))
    img.circle(x + int(w * 0.50), y + int(h * 0.20), 8, (255, 200, 0))
    img.circle(x + int(w * 0.86), y + int(h * 0.14), 8, (255, 240, 180))
    img.circle(x + int(w * 0.88), y + int(h * 0.12), 7, (120, 180, 235))
    for i in range(5):
        img.rect(x + int(w * (0.05 + 0.18 * i)), y + int(h * 0.86), 2, int(h * 0.10), (120, 82, 52))
    # minaret, a small tent behind, a water tank, an olive tree
    img.rect(x + int(w * 0.03), y + int(h * 0.30), int(w * 0.04), int(h * 0.42), (190, 170, 140))
    img.circle(x + int(w * 0.05), y + int(h * 0.28), 4, (190, 170, 140))
    img.rect(x + int(w * 0.02), y + int(h * 0.38), int(w * 0.06), 3, (160, 140, 110))
    img.poly([(x + int(w * 0.55), y + int(h * 0.60)), (x + int(w * 0.69), y + int(h * 0.60)),
              (x + int(w * 0.62), y + int(h * 0.44))], (170, 110, 210))
    img.rect(x + int(w * 0.90), y + int(h * 0.58), int(w * 0.07), int(h * 0.14), (90, 110, 145))
    img.rect(x + int(w * 0.90), y + int(h * 0.58), int(w * 0.07), 3, (90, 110, 130))
    img.line(x + int(w * 0.38), y + int(h * 0.72), x + int(w * 0.38), y + int(h * 0.60), (120, 82, 52))
    img.circle(x + int(w * 0.38), y + int(h * 0.56), 5, (60, 140, 80))


def scene_quake(img, x, y, w, h):
    img.rect(x, y, w, h, (255, 200, 150))
    img.rect(x, y + int(h * 0.70), w, int(h * 0.30), (150, 120, 90))
    bx, by = x + int(w * 0.28), y + int(h * 0.28)
    img.poly([(bx, by), (bx + int(w * 0.30), by - 6), (bx + int(w * 0.34), y + int(h * 0.70)),
              (bx + int(w * 0.04), y + int(h * 0.70))], (120, 120, 130))
    for r in range(3):
        for c in range(3):
            img.rect(bx + 5 + c * 14, by + 8 + r * 12, 7, 7, (255, 220, 120))
    img.line(bx + 8, by + 10, bx + 16, by + 22, INK)
    img.line(bx + 16, by + 22, bx + 10, by + 34, INK)
    cx = x + int(w * 0.60)
    for i, zz in enumerate(((0.78, 0.70), (0.74, 0.62), (0.70, 0.52), (0.66, 0.42), (0.62, 0.34))):
        img.line(x + int(w * zz[0]), y + int(h * zz[1]), x + int(w * (zz[0] + 0.06)), y + int(h * (zz[1] + 0.06)), INK)
    for r in (8, 16, 24):
        img.ring(cx, y + int(h * 0.55), r, (179, 39, 46), 2)
    img.line(x + int(w * 0.72), y + int(h * 0.70), x + int(w * 0.84), y + int(h * 0.44), (70, 70, 78))
    img.line(x + int(w * 0.80), y + int(h * 0.52), x + int(w * 0.88), y + int(h * 0.50), (70, 70, 78))
    zig = [(0.06, 0.88), (0.12, 0.82), (0.18, 0.90), (0.24, 0.84), (0.30, 0.88), (0.36, 0.82)]
    for i in range(len(zig) - 1):
        img.line(x + int(w * zig[i][0]), y + int(h * zig[i][1]),
                 x + int(w * zig[i + 1][0]), y + int(h * zig[i + 1][1]), (179, 39, 46))


def scene_arctic(img, x, y, w, h):
    img.rect(x, y, w, h, (70, 110, 180))
    # aurora ribbons across the night sky, behind the land
    for dy, c in ((0.05, (0, 230, 130)), (0.11, (180, 90, 220)), (0.17, (60, 220, 240))):
        xs = (0.05, 0.25, 0.45, 0.65, 0.85, 0.98)
        for i in range(len(xs) - 1):
            y1 = y + int(h * (dy + (0.02 if i % 2 == 0 else -0.02)))
            y2 = y + int(h * (dy + (0.02 if (i + 1) % 2 == 0 else -0.02)))
            img.line(x + int(w * xs[i]), y1, x + int(w * xs[i + 1]), y2, c)
    gl = [(0.30, 0.15), (0.45, 0.10), (0.62, 0.16), (0.70, 0.30), (0.66, 0.48),
          (0.55, 0.62), (0.42, 0.58), (0.34, 0.42), (0.28, 0.28)]
    pts = [(x + int(w * a), y + int(h * b)) for a, b in gl]
    img.poly(pts, (255, 255, 255))
    for i in range(len(pts)):
        img.line(pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], (120, 160, 190))
    fx = x + int(w * 0.50)
    img.rect(fx, y + int(h * 0.22), 2, int(h * 0.30), INK)
    img.rect(fx + 2, y + int(h * 0.22), int(w * 0.16), int(h * 0.10), (200, 16, 46))
    img.rect(fx + 2, y + int(h * 0.25), int(w * 0.16), 2, (255, 255, 255))
    img.rect(fx + 2 + int(w * 0.05), y + int(h * 0.22), 2, int(h * 0.10), (255, 255, 255))
    for i, (sx, sy) in enumerate(((0.15, 0.80), (0.80, 0.75), (0.25, 0.88), (0.70, 0.88))):
        img.circle(x + int(w * sx), y + int(h * sy), 3, (255, 255, 255))
    img.poly([(x + int(w * 0.10), y + int(h * 0.92)), (x + int(w * 0.26), y + int(h * 0.92)),
              (x + int(w * 0.18), y + int(h * 0.84))], (255, 255, 255))
    img.poly([(x + int(w * 0.72), y + int(h * 0.92)), (x + int(w * 0.88), y + int(h * 0.92)),
              (x + int(w * 0.80), y + int(h * 0.80))], (255, 255, 255))
    img.rect(x + int(w * 0.79), y + int(h * 0.72), 2, int(h * 0.08), INK)
    img.rect(x + int(w * 0.79), y + int(h * 0.72), int(w * 0.08), int(h * 0.04), (200, 16, 46))
    for sx, sy in ((0.45, 0.85), (0.60, 0.90), (0.35, 0.92)):
        img.circle(x + int(w * sx), y + int(h * sy), 2, (255, 255, 255))
    # a polar bear on the ice
    bx = x + int(w * 0.14)
    by = y + int(h * 0.80)
    bear = (235, 238, 242)
    img.rect(bx, by, int(w * 0.20), int(h * 0.09), bear)
    img.circle(bx, by + int(h * 0.045), int(h * 0.045), bear)
    img.circle(bx + int(w * 0.20), by + int(h * 0.045), int(h * 0.045), bear)
    img.circle(bx + int(w * 0.24), by - int(h * 0.02), int(h * 0.05), bear)
    img.circle(bx + int(w * 0.23), by - int(h * 0.06), 2, bear)
    img.circle(bx + int(w * 0.26), by - int(h * 0.06), 2, bear)
    img.circle(bx + int(w * 0.27), by - int(h * 0.03), 1, (40, 40, 48))
    img.circle(bx + int(w * 0.29), by - int(h * 0.01), 2, (40, 40, 48))
    img.rect(bx + int(w * 0.02), by + int(h * 0.09), 3, int(h * 0.06), bear)
    img.rect(bx + int(w * 0.15), by + int(h * 0.09), 3, int(h * 0.06), bear)


def scene_flags(img, x, y, w, h):
    img.rect(x, y, w, h, PALE)
    img.rect(x, y + int(h * 0.80), w, 3, INK)
    for i, pole in enumerate((0.24, 0.68)):
        px = x + int(w * pole)
        img.rect(px, y + int(h * 0.18), 3, int(h * 0.62), INK)
        fw = int(w * 0.22)
        if i == 0:
            img.rect(px + 3, y + int(h * 0.18), fw, int(h * 0.20), (65, 137, 221))
            img.circle(px + 3 + fw // 2, y + int(h * 0.28), 5, (255, 255, 255))
        else:
            img.rect(px + 3, y + int(h * 0.18), fw, int(h * 0.05), (0, 122, 61))
            img.rect(px + 3, y + int(h * 0.23), fw, int(h * 0.05), (255, 255, 255))
            img.rect(px + 3, y + int(h * 0.28), fw, int(h * 0.05), (0, 0, 0))
            img.rect(px + 3, y + int(h * 0.18), int(w * 0.05), int(h * 0.15), (200, 16, 46))
    mx = x + w // 2
    img.circle(mx - 8, y + int(h * 0.50), 6, (120, 120, 130))
    img.circle(mx + 8, y + int(h * 0.50), 6, (120, 120, 130))
    img.line(mx - 2, y + int(h * 0.50), mx + 2, y + int(h * 0.50), (179, 39, 46))
    img.line(mx - 4, y + int(h * 0.42), mx + 4, y + int(h * 0.58), (179, 39, 46))
    img.rect(x + int(w * 0.40), y + int(h * 0.62), int(w * 0.20), int(h * 0.12), (200, 200, 200))
    img.rect(x + int(w * 0.40), y + int(h * 0.62), int(w * 0.20), 2, (179, 39, 46))
    img.rect(x + int(w * 0.42), y + int(h * 0.64), int(w * 0.16), 2, (255, 255, 255))
    img.rect(x + int(w * 0.42), y + int(h * 0.68), int(w * 0.16), 2, (255, 255, 255))
    img.line(x + int(w * 0.30), y + int(h * 0.70), x + int(w * 0.38), y + int(h * 0.66), (30, 132, 73))
    img.line(x + int(w * 0.38), y + int(h * 0.66), x + int(w * 0.34), y + int(h * 0.62), (30, 132, 73))


def scene_drone(img, x, y, w, h):
    img.rect(x, y, w, h, (255, 190, 120))
    img.poly([(x, y + h), (x + int(w * 0.30), y + int(h * 0.45)), (x + int(w * 0.55), y + h)], (120, 100, 80))
    img.poly([(x + int(w * 0.45), y + h), (x + int(w * 0.75), y + int(h * 0.55)), (x + w, y + h)], (100, 85, 68))
    cx, cy = x + w // 2, y + int(h * 0.30)
    img.rect(cx - int(w * 0.08), cy - 5, int(w * 0.16), 10, (60, 60, 70))
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        ex, ey = cx + sx * int(w * 0.20), cy + sy * int(h * 0.14)
        img.line(cx, cy, ex, ey, (60, 60, 70))
        img.circle(ex, ey, 6, (90, 90, 100))
        img.line(ex - 10, ey, ex + 10, ey, (140, 140, 150))
    img.circle(cx, cy + 8, 3, (255, 80, 80))
    for ang in range(0, 360, 45):
        import math
        ex = cx + int(12 * math.cos(math.radians(ang)))
        ey = y + int(h * 0.80) + int(12 * math.sin(math.radians(ang)))
        img.line(cx, y + int(h * 0.80), ex, ey, (255, 140, 40))
    img.circle(cx, y + int(h * 0.80), 5, (255, 100, 30))
    img.ring(cx, y + int(h * 0.88), 9, (255, 255, 255), 2)
    img.ring(cx, y + int(h * 0.88), 5, (255, 100, 30), 2)
    img.rect(x + int(w * 0.10), y + int(h * 0.20), 10, 4, (60, 60, 70))
    img.line(x + int(w * 0.08), y + int(h * 0.20), x + int(w * 0.18), y + int(h * 0.20), (140, 140, 150))
    img.poly([(x + int(w * 0.86), y + int(h * 0.70)), (x + int(w * 0.94), y + int(h * 0.70)),
              (x + int(w * 0.90), y + int(h * 0.45))], (90, 90, 100))


SCENES = {
    "summit": scene_summit, "justice": scene_justice, "bridge": scene_bridge,
    "chart": scene_chart, "controller": scene_controller, "cyclone": scene_cyclone,
    "tower": scene_tower, "tents": scene_tents, "quake": scene_quake,
    "arctic": scene_arctic, "flags": scene_flags, "drone": scene_drone,
}


def tint(c, f=0.85):
    """Lighten a colour toward white (f = fraction of white)."""
    return (round(c[0] + (255 - c[0]) * f), round(c[1] + (255 - c[1]) * f),
            round(c[2] + (255 - c[2]) * f))


def pill(img, x, y, w, h, c):
    """A filled pill (rounded rectangle) with radius h/2."""
    r = h // 2
    img.rect(x + r, y, w - 2 * r, h, c)
    img.circle(x + r, y + r, r, c)
    img.circle(x + w - r - 1, y + r, r, c)


# Local times in the main-story cities at 12:00 UTC, 19 November 2026.
# Local time each story broke, 19 November 2026 (researched):
# Shenzhen 16:30 meeting began; The Hague 10:00 judgment read;
# Kerch 03:59 first report (overnight strike); New York 11:49 first trade;
# Gaza 12:38 first wire coverage; Kumamoto 02:22 quake struck (JMA).
CLOCKS = [
    ("SHENZHEN", 16, 30), ("THE HAGUE", 10, 0), ("KERCH", 3, 59),
    ("NEW YORK", 11, 49), ("GAZA", 12, 38), ("KUMAMOTO", 2, 22),
]
CLOCK_MAP = {city: "%02d:%02d" % (h, m) for city, h, m in CLOCKS}

# The day in numbers: six big stats, one per top story.
STATS = [
    ("3", "presidents", "at one table", "ASIA"),
    ("9-6", "ICJ genocide", "vote", "EUROPE"),
    ("$81.3bn", "Anthropic", "record IPO", "AMERICAS"),
    ("109-0", "Arctic pact", "vote", "EUROPE"),
    ("80,000+", "evacuated", "as Akvan nears", "ASIA"),
    ("22,133", "evacuated", "in Kumamoto", "ASIA"),
]


# --------------------------------------------------------------- world map
# Continents as longitude/latitude outlines, drawn on an equirectangular
# projection, so the map reads like a real world map rather than blobs.
# Latitudes run 90 (top) to -55 (bottom); Antarctica is left out.
MAP_LAT_TOP, MAP_LAT_BOT = 85.0, -55.0

NORTH_AMERICA = [
    (-168, 66), (-162, 60), (-155, 58), (-148, 60), (-141, 60), (-135, 57),
    (-130, 53), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-112, 27), (-110, 24), (-107, 22),
    (-105, 20), (-100, 17), (-95, 16), (-91, 14), (-87, 13), (-83, 9),
    (-79, 9), (-77, 7), (-80, 9), (-83, 10), (-86, 13), (-88, 15), (-88, 17),
    (-87, 16), (-90, 21), (-93, 19), (-96, 19), (-97, 22), (-97, 26),
    (-94, 29), (-90, 29), (-84, 30), (-82, 27), (-80, 25), (-81, 31),
    (-76, 35), (-74, 39), (-70, 42), (-68, 44), (-66, 45), (-60, 46),
    (-55, 47), (-53, 49), (-56, 52), (-60, 55), (-65, 58), (-68, 58),
    (-72, 62), (-78, 55), (-80, 52), (-85, 55), (-88, 60), (-90, 64), (-92, 66),
    (-95, 68), (-100, 68), (-110, 68), (-120, 69), (-130, 69), (-140, 70),
    (-150, 70), (-158, 71), (-165, 68), (-168, 66),
]
GREENLAND = [
    (-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-24, 70),
    (-20, 74), (-22, 76), (-28, 78), (-38, 80), (-48, 80), (-56, 77),
    (-60, 74), (-58, 70), (-58, 64),
]
SOUTH_AMERICA = [
    (-79, 9), (-77, 4), (-80, -3), (-81, -6), (-78, -12), (-73, -18),
    (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
    (-66, -55), (-68, -50), (-65, -45), (-62, -40), (-58, -35), (-52, -32),
    (-48, -28), (-41, -23), (-35, -20), (-35, -15), (-35, -8), (-40, -5),
    (-44, -2), (-50, 0), (-55, 5), (-60, 8), (-64, 10), (-69, 11),
    (-73, 11), (-76, 10), (-79, 9),
]
AFRICA = [
    (-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36), (10, 37),
    (11, 34), (15, 32), (20, 32), (25, 32), (30, 31), (32, 31), (34, 28),
    (35, 23), (37, 18), (39, 15), (43, 11), (48, 11), (51, 11), (49, 8), (46, 5),
    (42, 0), (40, -5), (40, -10), (38, -15), (35, -20), (32, -26),
    (28, -32), (20, -35), (17, -32), (15, -27), (12, -18), (12, -12),
    (9, -1), (9, 4), (-8, 5), (-13, 8), (-17, 12), (-17, 15),
]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (50, -20), (47, -24), (44, -25), (43, -21), (44, -16)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-3, 50), (-5, 50)]
JAPAN = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36), (141, 38),
         (142, 40), (143, 42), (145, 44), (142, 44), (140, 40), (138, 37), (136, 35),
         (133, 34), (130, 31)]
SUMATRA = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -5), (103, -6), (100, -3), (97, 1), (95, 5)]
BORNEO = [(109, 1), (111, 3), (114, 4), (117, 2), (118, -1), (116, -4), (112, -4), (110, -1), (109, 1)]
JAVA = [(105, -6), (108, -6), (111, -7), (114, -7), (112, -8), (108, -8), (105, -7), (105, -6)]
NEW_GUINEA = [(131, -1), (134, -2), (137, -3), (140, -4), (143, -6), (146, -8),
              (147, -9), (143, -8), (139, -6), (135, -4), (131, -1)]
AUSTRALIA = [
    (114, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
    (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
    (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
    (140, -17), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14),
    (122, -17), (118, -20), (114, -22),
]
NEW_ZEALAND = [(167, -45), (169, -43), (171, -41), (173, -40), (175, -38),
               (176, -37), (174, -39), (172, -41), (170, -43), (167, -45)]
# Europe and Asia share one border (Urals, then Caucasus); the two lists
# carry the same border points so no gap shows between them.
EUROPE = [
    (-9, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50), (0, 51),
    (3, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64),
    (12, 66), (18, 69), (25, 71), (30, 70), (35, 68), (40, 67), (45, 68),
    (50, 69), (55, 68), (60, 69), (60, 60), (55, 51), (50, 47), (45, 44),
    (40, 42), (38, 41), (36, 41), (33, 42), (30, 41), (28, 41), (27, 40),
    (26, 38), (23, 36), (22, 37), (23, 39), (21, 40), (19, 42), (16, 44),
    (14, 45), (12, 44), (14, 42), (17, 40), (16, 38), (15, 41), (13, 41),
    (11, 43), (8, 44), (3, 43), (0, 40), (-2, 37), (-5, 36), (-9, 37),
]
ASIA = [
    (60, 69), (65, 69), (70, 72), (75, 73), (80, 73), (85, 74), (90, 75),
    (95, 76), (100, 77), (105, 78), (110, 76), (115, 73), (120, 72),
    (125, 71), (130, 71), (135, 70), (140, 72), (145, 72), (150, 70),
    (155, 69), (158, 66), (162, 62), (162, 58), (158, 55), (155, 52),
    (150, 50), (145, 45), (142, 40), (140, 35), (138, 32), (135, 30),
    (132, 28), (130, 25), (128, 22), (125, 20), (122, 18), (120, 15),
    (118, 12), (115, 10), (112, 8), (110, 5), (108, 2), (105, 1), (103, 1),
    (100, 7), (98, 12), (95, 16), (92, 20), (91, 22), (88, 22), (85, 19),
    (80, 15), (79, 11), (77, 8), (75, 11), (73, 15), (72, 18), (70, 20), (67, 23),
    (66, 25), (61, 25), (57, 26), (54, 27), (51, 28), (50, 29), (48, 30),
    (48, 29), (50, 26), (55, 24), (58, 22), (59, 20), (55, 17), (52, 15),
    (48, 14), (44, 13), (43, 12), (42, 14), (40, 17), (39, 20), (38, 24), (36, 28),
    (34, 28), (35, 31), (36, 36), (40, 42), (45, 44), (50, 47), (55, 51),
    (60, 60), (60, 69),
]

LAND = [
    (NORTH_AMERICA, "AMERICAS"), (GREENLAND, "AMERICAS"), (SOUTH_AMERICA, "AMERICAS"),
    (AFRICA, "AFRICA"), (MADAGASCAR, "AFRICA"), (UK, "EUROPE"), (JAPAN, "ASIA"),
    (SUMATRA, "ASIA"), (BORNEO, "ASIA"), (JAVA, "ASIA"), (NEW_GUINEA, "OCEANIA"),
    (AUSTRALIA, "OCEANIA"), (NEW_ZEALAND, "OCEANIA"), (EUROPE, "EUROPE"), (ASIA, "ASIA"),
]


def project(x, y, w, h, lon, lat):
    px = x + int((lon + 180.0) / 360.0 * w)
    py = y + int((MAP_LAT_TOP - lat) / (MAP_LAT_TOP - MAP_LAT_BOT) * h)
    return (px, py)


def draw_map(img, x, y, w, h, markers, badges):
    """markers: list of (number, lon, lat, region); badges: list of (region, count, lon, lat)."""
    img.rect(x, y, w, h, OCEAN)
    for poly_ll, region in LAND:
        pts = [project(x, y, w, h, lon, lat) for lon, lat in poly_ll]
        img.poly(pts, REGION[region])
    # graticule, light
    for lon in range(-150, 151, 30):
        px = x + int((lon + 180.0) / 360.0 * w)
        for yy in range(y, y + h, 4):
            img.set(px, yy, (255, 255, 255))
    # story dots
    for num, lon, lat, region in markers:
        cx, cy = project(x, y, w, h, lon, lat)
        img.circle(cx, cy, 6, (255, 255, 255))
        img.circle(cx, cy, 5, REGION[region])
        s = str(num)
        draw_text(img, cx - text_width(s, 1) // 2, cy - 3, s, 1, (255, 255, 255))
    # ring badges: stories per region
    for region, count, lon, lat in badges:
        cx, cy = project(x, y, w, h, lon, lat)
        img.circle(cx, cy, 11, (255, 255, 255))
        img.ring(cx, cy, 11, REGION[region], 2)
        s = str(count)
        draw_text(img, cx - text_width(s, 1) // 2, cy - 3, s, 1, REGION[region])


# ------------------------------------------------------------------- data
# 12 main stories. Each: number, place, region, headline, standfirst,
# scene key, and (lon, lat) for the map marker (None = global, off map).
MAINS = [
    (1, "SHENZHEN", "ASIA", "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
     "First trilateral adopts a Peace Declaration - no Ukraine or Iran deal.",
     "summit", (114.05, 22.55)),
    (2, "THE HAGUE", "EUROPE", "MYANMAR GUILTY OF ROHINGYA GENOCIDE",
     "World court rules 9-6, first genocide verdict; orders reparations.",
     "justice", (4.3, 52.08)),
    (3, "KERCH", "EUROPE", "CRIMEAN BRIDGE HIT A THIRD TIME",
     "Neptune missiles hit the rail section; trains halted.",
     "bridge", (36.4, 45.3)),
    (4, "NEW YORK", "AMERICAS", "ANTHROPIC IPOS IN THE BIGGEST EVER",
     "Priced at $83; the AI firm raises $81.3B.",
     "chart", (-74.0, 40.7)),
    (5, "WORLDWIDE", "GLOBAL", "GTA VI LAUNCHES TO A 99",
     "Vice City returns on PS5 and Xbox; presales $1.6B.",
     "controller", None),
    (6, "BAY OF BENGAL", "ASIA", "CYCLONE AKVAN BEARS DOWN",
     "80,000+ evacuated; landfall at noon Friday.",
     "cyclone", (89.0, 16.0)),
    (7, "RIYADH", "MIDEAST", "MISSILE DAMAGES RIYADH'S PIF TOWER",
     "Windows out; second strike in 11 days.",
     "tower", (46.7, 24.7)),
    (8, "GAZA", "MIDEAST", "GAZA PEACE PLAN SCORES 4 OF 26",
     "Access zero; 1,650 killed since ceasefire.",
     "tents", (34.5, 31.5)),
    (9, "KUMAMOTO", "ASIA", "M5.7 QUAKE SHAKES KUMAMOTO",
     "22,133 evacuated; 8 Shinkansen halted.",
     "quake", (130.7, 32.8)),
    (10, "COPENHAGEN", "EUROPE", "DENMARK BACKS ARCTIC DEAL 109-0",
     "Denmark ratifies Arctic pact; US bases follow.",
     "arctic", (12.57, 55.68)),
    (11, "MOGADISHU", "AFRICA", "SOMALIA EXPELS UAE AMBASSADOR",
     "Envoy gets 72 hours; Somalia alleges invasion.",
     "flags", (45.3, 2.05)),
    (12, "BADME", "AFRICA", "ETHIOPIA-ERITREA BORDER FLARES",
     "Drone strikes; both armies massed.",
     "drone", (37.8, 14.7)),
]

# The other 28 stories: number, place, region, headline.
REST = [
    (13, "SHENZHEN", "ASIA", "APEC closes in Shenzhen"),
    (14, "TOKYO", "ASIA", "India-Japan naval mast deal"),
    (15, "ANTALYA", "ASIA", "COP31 drops fossil fuels"),
    (16, "ODISHA", "ASIA", "80,000+ flee as Akvan nears"),
    (17, "DHAKA", "ASIA", "Awami lockdown, Yunus hit"),
    (18, "KUALA LUMPUR", "ASIA", "Malaysia ends visa-free"),
    (19, "SHENZHEN", "ASIA", "Trump-Xi Hormuz oil deal"),
    (20, "SHENZHEN", "ASIA", "Trump-Putin meet 40 minutes"),
    (21, "HANGZHOU", "ASIA", "Alibaba +10%, AI cloud +53%"),
    (22, "PATIALA", "ASIA", "60m bridge falls, safe"),
    (23, "SHENZHEN", "ASIA", "Takaichi: free Japanese"),
    (24, "JAKARTA", "ASIA", "Parliament passes new law"),
    (25, "MANILA", "ASIA", "US unveils $2B defence loans"),
    (26, "GAZA", "MIDEAST", "Israel ends Gaza operation"),
    (27, "WEST BANK", "MIDEAST", "Israel delays E1 settlement"),
    (28, "HORMUZ", "MIDEAST", "Iran: tankers hit mines"),
    (29, "PARIS", "EUROPE", "Data centres +70% by 2030"),
    (30, "MADRID", "EUROPE", "Migrants drove GDP growth"),
    (31, "FRANKFURT", "EUROPE", "Deutsche hid EUR 800m"),
    (32, "FRANKFURT", "EUROPE", "Deutsche $582m Epstein"),
    (33, "ZURICH", "EUROPE", "Infantino faces challengers"),
    (34, "KYIV", "EUROPE", "Russia fires 98 drones"),
    (35, "BERLIN", "EUROPE", "UK gives GBP 260m Kyiv aid"),
    (36, "WELLINGTON", "OCEANIA", "NZ 243/5, Nicholls 113"),
    (37, "SUVA", "OCEANIA", "Fiji drought disaster"),
]

COUNTS = {"ASIA": 16, "EUROPE": 10, "MIDEAST": 5, "AMERICAS": 1,
          "AFRICA": 2, "OCEANIA": 2, "GLOBAL": 1}

BADGES = [
    ("ASIA", 17, 128, 28), ("EUROPE", 11, 8, 55), ("MIDEAST", 5, 46, 24),
    ("AMERICAS", 2, -100, 40), ("AFRICA", 2, 20, -2), ("OCEANIA", 2, 138, -26),
]


# ------------------------------------------------------------------ layout
def card(img, x, y, w, h, fill=(255, 255, 255)):
    img.rect(x, y, w, h, fill)
    img.rect(x, y, w, 1, GRID)
    img.rect(x, y + h - 1, w, 1, GRID)
    img.rect(x, y, 1, h, GRID)
    img.rect(x + w - 1, y, 1, h, GRID)


def build():
    img = Img(W, H, PAPER_TOP, PAPER_BOT)
    RULE = (150, 150, 150)

    # ---- header band in dark blue, colour unchanged: red date box,
    # ---- gold count box (now 37 stories), THE WORLD in white, TODAY gold
    img.rect(14, 12, 740, 52, NAVY)
    img.rect(14, 12, 150, 52, RED)
    draw_text(img, 14 + (150 - text_width("THURSDAY", 2)) // 2, 20, "THURSDAY", 2, (255, 255, 255))
    draw_text(img, 14 + (150 - text_width("19 NOV 2026", 2)) // 2, 44, "19 NOV 2026", 2, (255, 255, 255))
    img.rect(604, 12, 150, 52, GOLD)
    draw_text(img, 604 + (150 - text_width("37", 3)) // 2, 14, "37", 3, NAVY)
    draw_text(img, 604 + (150 - text_width("STORIES", 1)) // 2, 40, "STORIES", 1, NAVY)
    t1, t2 = "THE WORLD ", "TODAY"
    total = text_width(t1, 3) + text_width(t2, 3)
    mx = (W - total) // 2
    draw_text(img, mx, 14, t1, 3, (255, 255, 255))
    draw_text(img, mx + text_width(t1, 3), 14, t2, 3, GOLD)
    tag = "Trump, Xi, Putin meet - ICJ: Myanmar guilty - Akvan nears India"
    draw_text(img, (W - text_width(tag, 1)) // 2, 40, tag, 1, (255, 255, 255))
    img.rect(164, 54, 440, 3, RED)
    img.rect(164, 59, 440, 1, GOLD)

    # ---- the day in numbers: big red figures, no boxes, thin rules between
    widths = []
    base = 740 // 6
    rem = 740 % 6
    for i in range(6):
        widths.append(base + 1 if i < rem else base)
    cx = 14
    for i, (num, l1, l2, region) in enumerate(STATS):
        wcell = widths[i]
        draw_text(img, cx + (wcell - text_width(num, 2)) // 2, 74, num, 2, RED)
        draw_text(img, cx + (wcell - text_width(l1, 1)) // 2, 92, l1, 1, INK)
        draw_text(img, cx + (wcell - text_width(l2, 1)) // 2, 101, l2, 1, (90, 90, 96))
        cx += wcell
        if i < 5:
            img.rect(cx, 74, 1, 36, RULE)

    # ---- region chips, counts sum to exactly 37, fitted to the full width
    widths = []
    base = (740 - 6 * 6) // 7
    rem = (740 - 6 * 6) % 7
    for i in range(7):
        widths.append(base + 1 if i < rem else base)
    cx = 14
    for i, region in enumerate(("ASIA", "EUROPE", "MIDEAST", "AMERICAS", "AFRICA", "OCEANIA", "GLOBAL")):
        label = "%s %d" % (REGION_NAME[region], COUNTS[region])
        img.rect(cx, 120, widths[i], 22, REGION[region])
        draw_text(img, cx + (widths[i] - text_width(label, 1)) // 2, 126, label, 1, (255, 255, 255))
        cx += widths[i] + 6

    # ---- the three big main stories, each in its own 2px-bordered box:
    # ---- label bar, big illustration with its own sharp border, then text
    for k in range(3):
        num, place, region, head, stand, _scene, _ll = MAINS[k]
        x0 = 14 + k * 250
        y0 = 148
        img.rect(x0, y0, 244, 2, INK)
        img.rect(x0, y0 + 214, 244, 2, INK)
        img.rect(x0, y0, 2, 216, INK)
        img.rect(x0 + 242, y0, 2, 216, INK)
        lab = "%s - %s" % (place, {"SHENZHEN": "SUMMIT", "THE HAGUE": "JUSTICE", "KERCH": "BRIDGE"}[place])
        img.rect(x0 + 2, y0 + 2, 240, 16, REGION[region])
        draw_text(img, x0 + 2 + (240 - text_width(lab, 1)) // 2, y0 + 6, lab, 1, (255, 255, 255))
        SCENES[_scene](img, x0 + 7, y0 + 20, 230, 118)
        img.rect(x0 + 7, y0 + 20, 230, 1, INK)
        img.rect(x0 + 7, y0 + 137, 230, 1, INK)
        img.rect(x0 + 7, y0 + 20, 1, 118, INK)
        img.rect(x0 + 236, y0 + 20, 1, 118, INK)
        pline = "%d. %s" % (num, place)
        if place in CLOCK_MAP:
            pline += " - " + CLOCK_MAP[place]
        draw_text(img, x0 + 7, y0 + 144, pline, 1, REGION[region])
        for i, ln in enumerate(wrap_text(head, 230, 2)[:2]):
            draw_text(img, x0 + 7, y0 + 156 + i * 17, ln, 2, INK)
        for i, ln in enumerate(wrap_text(stand, 230, 1)[:2]):
            draw_text(img, x0 + 7, y0 + 192 + i * 9, ln, 1, (90, 90, 96))

    # ---- nine mini stories, each in its own bordered box with a label bar
    for k in range(3, 12):
        num, place, region, head, stand, _scene, _ll = MAINS[k]
        r, c = (k - 3) // 3, (k - 3) % 3
        x0 = 14 + c * 250
        y0 = 370 + r * 86
        img.rect(x0, y0, 244, 1, INK)
        img.rect(x0, y0 + 79, 244, 1, INK)
        img.rect(x0, y0, 1, 80, INK)
        img.rect(x0 + 243, y0, 1, 80, INK)
        lab = "%d. %s" % (num, place)
        if place in CLOCK_MAP:
            lab += " - " + CLOCK_MAP[place]
        img.rect(x0 + 1, y0 + 1, 242, 13, REGION[region])
        draw_text(img, x0 + 1 + (242 - text_width(lab, 1)) // 2, y0 + 4, lab, 1, (255, 255, 255))
        SCENES[_scene](img, x0 + 6, y0 + 18, 70, 56)
        img.rect(x0 + 6, y0 + 18, 70, 1, INK)
        img.rect(x0 + 6, y0 + 73, 70, 1, INK)
        img.rect(x0 + 6, y0 + 18, 1, 56, INK)
        img.rect(x0 + 75, y0 + 18, 1, 56, INK)
        for i, ln in enumerate(wrap_text(head, 152, 1)[:3]):
            draw_text(img, x0 + 84, y0 + 18 + i * 9, ln, 1, INK)
        for i, ln in enumerate(wrap_text(stand, 152, 1)[:2]):
            draw_text(img, x0 + 84, y0 + 48 + i * 9, ln, 1, (90, 90, 96))

    # ---- where it happened: map left, the other 25 stories right,
    # ---- two columns, each item in its own bordered box, two lines
    img.rect(14, 628, 740, 1, RULE)
    draw_text(img, 14, 634, "THE WORLD IN ONE LOOK - 12 MAIN STORIES MARKED", 1, NAVY)
    draw_text(img, 348, 634, "ALSO ON THURSDAY 19 NOVEMBER 2026", 1, NAVY)
    markers = [(m[0], m[6][0], m[6][1], m[2]) for m in MAINS if m[6] is not None]
    draw_map(img, 14, 646, 320, 200, markers, [])
    for i, (num, place, region, head) in enumerate(REST):
        col = i // 13
        row = i % 13
        x0 = 348 + col * 210
        y0 = 646 + row * 22
        num_s = "%d" % num
        pw = text_width(num_s, 1) + 6
        pill(img, x0, y0 - 1, pw, 10, REGION[region])
        draw_text(img, x0 + 3, y0, num_s, 1, (255, 255, 255))
        px = x0 + pw + 4
        draw_text(img, px, y0, place, 1, REGION[region])
        draw_text(img, px, y0 + 9, head, 1, INK)
    img.rect(341, 646, 1, 284, RULE)

    # ---- map key, compact, under the map (no card)
    draw_text(img, 14, 856, "MAP KEY", 1, NAVY)
    lx, ly = 14, 870
    for region in ("ASIA", "EUROPE", "MIDEAST", "AMERICAS"):
        img.rect(lx, ly, 8, 8, REGION[region])
        lx += 11
        draw_text(img, lx, ly + 1, REGION_NAME[region], 1, INK)
        lx += text_width(REGION_NAME[region], 1) + 10
    lx, ly = 14, 886
    for region in ("AFRICA", "OCEANIA", "GLOBAL"):
        img.rect(lx, ly, 8, 8, REGION[region])
        lx += 11
        draw_text(img, lx, ly + 1, REGION_NAME[region], 1, INK)
        lx += text_width(REGION_NAME[region], 1) + 10
    draw_text(img, 14, 910, "Numbers on the map match the 12 main stories.", 1, (90, 90, 96))
    draw_text(img, 14, 919, "All 37 stories are from 19 November 2026.", 1, (90, 90, 96))
    draw_text(img, 14, 928, "Wires: Reuters, AP, BBC, AFP, Xinhua, IMD.", 1, (90, 90, 96))
    draw_text(img, 14, 937, "Pictures and map: original, drawn in code.", 1, (90, 90, 96))

    # ---- date check box + left-out line + sources
    img.rect(14, 962, 740, 36, INK)
    img.rect(15, 963, 738, 34, PAPER_TOP)
    dc = "DATE CHECK - Every story on this page happened, or was first reported, on Thursday 19 November 2026."
    draw_text(img, 22, 970, dc, 1, INK)
    lo = "LEFT OUT AS OTHER DAYS' NEWS: 18 NOV - EU Ukraine loan, Iran fires, Nvidia results; 20 NOV - COP31 close, Akvan landfall."
    draw_text(img, 22, 982, lo, 1, (90, 90, 96))
    foot = "Sources: Reuters, AP, BBC, AFP, Xinhua, IMD, ESPNcricinfo and the day's wires - 19 November 2026"
    draw_text(img, (W - text_width(foot, 1)) // 2, 1006, foot, 1, (70, 80, 95))
    return img



def main():
    out = os.environ.get("OUTPUT", "/output/entry.png")
    img = build()
    n = write_png(img, out)
    print("wrote %s (%d bytes)" % (out, n))


if __name__ == "__main__":
    main()



