#!/usr/bin/env python3
"""THE WORLD TODAY - Thursday 19 November 2026, on one page.

A program that draws a one-page newspaper front page summing up the
world's news of Thursday 19 November 2026: 12 main stories with supplied
illustrations (art/sceneN.png), a world map drawn from real
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
PAPER_TOP = (250, 238, 210)
PAPER_BOT = (245, 228, 192)
INK = (30, 36, 48)
NAVY = (28, 58, 96)
RED = (179, 39, 46)
GOLD = (232, 180, 40)
CREAM = (255, 255, 255)
ROSE = (242, 218, 140)
OCEAN = (110, 165, 210)
GRID = (200, 210, 220)

REGION = {
    "ASIA": (225, 45, 45),
    "EUROPE": (45, 110, 205),
    "MIDEAST": (200, 125, 0),
    "AMERICAS": (30, 160, 80),
    "AFRICA": (190, 105, 35),
    "OCEANIA": (140, 80, 190),
    "GLOBAL": (28, 58, 96),
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
"g": (".....", ".####", "#...#", "#...#", ".####", "....#", ".###."),
"h": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
"i": ("..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
"j": ("...#.", ".....", "..##.", "...#.", "...#.", "#..#.", ".##.."),
"k": ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
"l": (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
"m": (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
"n": (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
"o": (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
"p": (".....", "####.", "#...#", "#...#", "####.", "#....", "#...."),
"q": (".....", ".####", "#...#", "#...#", ".####", "....#", "....#"),
"r": (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
"s": (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
"t": (".#...", ".#...", "####.", ".#...", ".#...", ".#...", "..##."),
"u": (".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"),
"v": (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
"w": (".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
"x": (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
"y": (".....", "#...#", "#...#", "#...#", ".####", "....#", ".###."),
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


# ------------------------------------------------------------ supplied art
# The 12 main-story pictures are supplied artwork, chosen by Sari from
# three AI-rendered versions of this page: image 1 for scenes 1-4 and
# 6-12, image 3 for the GTA scene 5, whose logo in image 1 came out
# garbled. They live in art/sceneN.png, pre-sized to the exact scene
# rectangles, so the program only has to decode and paste them. No text
# is drawn inside any picture.

def load_png(path):
    """Decode a small 8-bit non-interlaced PNG (RGB or RGBA) to
    (width, height, rgb bytes). Standard library only."""
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG: %s" % path
    pos = 8
    w = h = None
    bitdepth = ctype = None
    idat = b""
    while pos < len(data):
        ln = struct.unpack(">I", data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, bitdepth, ctype = struct.unpack(">IIBB", chunk[:10])
            assert bitdepth == 8 and ctype in (2, 6), "need 8-bit RGB/RGBA PNG"
        elif typ == b"IDAT":
            idat += chunk
        elif typ == b"IEND":
            break
        pos += 12 + ln
    raw = zlib.decompress(idat)
    ch = 3 if ctype == 2 else 4
    stride = w * ch
    out = bytearray(w * h * 3)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        f = raw[p]
        p += 1
        line = bytearray(raw[p:p + stride])
        p += stride
        if f == 1:
            for i in range(ch, stride):
                line[i] = (line[i] + line[i - ch]) & 255
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                a = line[i - ch] if i >= ch else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i - ch] if i >= ch else 0
                b = prev[i]
                c = prev[i - ch] if i >= ch else 0
                pp = a + b - c
                pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        for x in range(w):
            o = (y * w + x) * 3
            s = x * ch
            out[o] = line[s]
            out[o + 1] = line[s + 1]
            out[o + 2] = line[s + 2]
        prev = line
    return w, h, bytes(out)


def blit(img, x, y, w, h, art):
    """Paste a decoded picture onto img, scaled to (w, h) by nearest
    neighbour. The supplied art is already the exact size, so this is a
    straight copy."""
    aw, ah, rgb = art
    for yy in range(h):
        sy = min(ah - 1, yy * ah // h)
        dy = y + yy
        if dy < 0 or dy >= img.h:
            continue
        for xx in range(w):
            sx = min(aw - 1, xx * aw // w)
            dx = x + xx
            if dx < 0 or dx >= img.w:
                continue
            o = (dy * img.w + dx) * 3
            s = (sy * aw + sx) * 3
            img.pix[o] = rgb[s]
            img.pix[o + 1] = rgb[s + 1]
            img.pix[o + 2] = rgb[s + 2]



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


def draw_clock(img, cx, cy, r, hour, minute):
    """A small clock face showing hour:minute."""
    import math
    img.circle(cx, cy, r, (255, 255, 255))
    img.ring(cx, cy, r, INK, 2)
    for a in range(0, 360, 30):
        long = (a % 90 == 0)
        x1 = cx + int((r - 2) * math.cos(math.radians(a)))
        y1 = cy + int((r - 2) * math.sin(math.radians(a)))
        x2 = cx + int((r - (7 if long else 4)) * math.cos(math.radians(a)))
        y2 = cy + int((r - (7 if long else 4)) * math.sin(math.radians(a)))
        img.line(x1, y1, x2, y2, INK)
    ha = math.radians((hour % 12 + minute / 60.0) * 30 - 90)
    ma = math.radians(minute * 6 - 90)
    hx = cx + int((r * 0.55) * math.cos(ha))
    hy = cy + int((r * 0.55) * math.sin(ha))
    img.line(cx, cy, hx, hy, INK)
    img.line(cx + 1, cy, hx + 1, hy, INK)
    img.line(cx, cy + 1, hx, hy + 1, INK)
    img.line(cx, cy, cx + int((r * 0.85) * math.cos(ma)), cy + int((r * 0.85) * math.sin(ma)), INK)
    img.circle(cx, cy, 2, (200, 30, 30))


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
        img.circle(cx, cy, 8, (255, 255, 255))
        img.circle(cx, cy, 7, REGION[region])
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
     "First-ever trilateral summit adopts a joint Peace Declaration - but no deal on Ukraine or Iran.",
     "summit", (114.05, 22.55)),
    (2, "THE HAGUE", "EUROPE", "MYANMAR GUILTY OF ROHINGYA GENOCIDE",
     "World court rules 9-6, the first genocide verdict against a state; orders reparations and return.",
     "justice", (4.3, 52.08)),
    (3, "KERCH", "EUROPE", "CRIMEAN BRIDGE HIT A THIRD TIME",
     "Neptune missiles strike the rail section; train traffic halted, road span already down.",
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
    (13, "SHENZHEN", "ASIA", "APEC closes with Shenzhen Outlook"),
    (14, "SHENZHEN", "ASIA", "APEC CEOs issue Shenzhen Initiative"),
    (15, "TOKYO", "ASIA", "India-Japan fast-track naval mast deal"),
    (16, "ANTALYA", "ASIA", "COP31 draft drops fossil-fuel mentions"),
    (17, "ODISHA", "ASIA", "80,000+ evacuated as Akvan nears"),
    (18, "DHAKA", "ASIA", "Awami League lockdown; Yunus home torched"),
    (19, "KUALA LUMPUR", "ASIA", "Malaysia ends visa-free for Indians"),
    (20, "SHENZHEN", "ASIA", "Trump-Xi agree on Hormuz oil flow"),
    (21, "SHENZHEN", "ASIA", "Trump-Putin meet 40 minutes"),
    (22, "HANGZHOU", "ASIA", "Alibaba revenue +10%, AI cloud +53%"),
    (23, "PATIALA", "ASIA", "60m bridge collapses; drivers safe"),
    (24, "SHENZHEN", "ASIA", "Takaichi raises detained Japanese"),
    (25, "JAKARTA", "ASIA", "Parliament passes asset-forfeiture law"),
    (26, "MANILA", "ASIA", "US unveils $2B defence loans"),
    (27, "GAZA", "MIDEAST", "Israel ends central Gaza operation"),
    (28, "WEST BANK", "MIDEAST", "Israel delays E1 settlement"),
    (29, "HORMUZ", "MIDEAST", "Iran says three tankers hit mines"),
    (30, "PARIS", "EUROPE", "Data centres to emit 70% more by 2030"),
    (31, "MADRID", "EUROPE", "Migrants drove half of Spain's GDP growth"),
    (32, "FRANKFURT", "EUROPE", "Deutsche hid EUR 800m for a decade"),
    (33, "FRANKFURT", "EUROPE", "Deutsche handled $582m Epstein deals"),
    (34, "ZURICH", "EUROPE", "Infantino faces first FIFA challengers"),
    (35, "TURIN", "EUROPE", "Shelton beats Jodar, nears semi-final"),
    (36, "KYIV", "EUROPE", "Russia fires Oniks missiles, 98 drones"),
    (37, "BERLIN", "EUROPE", "UK gives GBP 260m winter aid to Kyiv"),
    (38, "BENTONVILLE", "AMERICAS", "Walmart Q3 beats estimates"),
    (39, "WELLINGTON", "OCEANIA", "NZ 243/5; Nicholls 113 not out"),
    (40, "SUVA", "OCEANIA", "Fiji declares disaster over drought"),
]

COUNTS = {"ASIA": 17, "EUROPE": 11, "MIDEAST": 5, "AMERICAS": 2,
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
    art_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art")
    art = [load_png(os.path.join(art_dir, "scene%d.png" % n)) for n in range(1, 13)]
    img = Img(W, H, PAPER_TOP, PAPER_BOT)

    # masthead band in dark blue, with the red date box, gold count box,
    # and a short tagline under the title
    img.rect(14, 12, 740, 52, NAVY)
    img.rect(14, 12, 150, 52, RED)
    draw_text(img, 14 + (150 - text_width("THURSDAY", 2)) // 2, 20, "THURSDAY", 2, (255, 255, 255))
    draw_text(img, 14 + (150 - text_width("19 NOV 2026", 2)) // 2, 44, "19 NOV 2026", 2, (255, 255, 255))
    img.rect(604, 12, 150, 52, GOLD)
    draw_text(img, 604 + (150 - text_width("40", 3)) // 2, 14, "40", 3, NAVY)
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

    # world clocks: one face per main-story city, the local time its news broke
    draw_text(img, 14, 74, "WHEN THE", 1, INK)
    draw_text(img, 14, 83, "NEWS", 1, INK)
    draw_text(img, 14, 92, "BROKE", 1, (90, 100, 115))
    for i, (city, hour, minute) in enumerate(CLOCKS):
        cx = 190 + i * 96
        draw_clock(img, cx, 86, 13, hour, minute)
        label = "%s %02d:%02d" % (city, hour, minute)
        draw_text(img, cx - text_width(label, 1) // 2, 103, label, 1, INK)

    # the day in numbers: six big stats, one per top story
    for i, (num, l1, l2, region) in enumerate(STATS):
        x0 = 14 + i * 123
        card(img, x0, 114, 118, 40, tint(REGION[region], 0.88))
        img.rect(x0, 114, 118, 3, (200, 30, 30))
        draw_text(img, x0 + (118 - text_width(num, 2)) // 2, 118, num, 2, (200, 30, 30))
        draw_text(img, x0 + (118 - text_width(l1, 1)) // 2, 134, l1, 1, INK)
        draw_text(img, x0 + (118 - text_width(l2, 1)) // 2, 143, l2, 1, (90, 90, 96))

    # region chips, counts sum to exactly 40, fitted to the full width
    widths = []
    base = (740 - 6 * 6) // 7
    rem = (740 - 6 * 6) % 7
    for i in range(7):
        widths.append(base + 1 if i < rem else base)
    cx = 14
    for i, region in enumerate(("ASIA", "EUROPE", "MIDEAST", "AMERICAS", "AFRICA", "OCEANIA", "GLOBAL")):
        label = "%s %d" % (REGION_NAME[region], COUNTS[region])
        img.rect(cx, 160, widths[i], 22, REGION[region])
        draw_text(img, cx + (widths[i] - text_width(label, 1)) // 2, 166, label, 1, (255, 255, 255))
        cx += widths[i] + 6

    # the three big main stories, side by side and level, with roomy scenes
    for k in range(3):
        num, place, region, head, stand, _scene, _ll = MAINS[k]
        x0 = 14 + k * 250
        card(img, x0, 188, 244, 176, tint(REGION[region], 0.88))
        img.rect(x0, 188, 244, 4, REGION[region])
        blit(img, x0 + 7, 196, 230, 88, art[num - 1])
        pline = "%d. %s" % (num, place)
        if place in CLOCK_MAP:
            pline += " - " + CLOCK_MAP[place]
        draw_text(img, x0 + 8, 288, pline, 1, REGION[region])
        for i, ln in enumerate(wrap_text(head, 228, 2)[:2]):
            draw_text(img, x0 + 8, 300 + i * 17, ln, 2, INK)
        for i, ln in enumerate(wrap_text(stand, 228, 1)[:3]):
            draw_text(img, x0 + 8, 336 + i * 9, ln, 1, (90, 90, 96))

    # nine mini stories, 3 x 3
    for k in range(3, 12):
        num, place, region, head, stand, _scene, _ll = MAINS[k]
        r, c = (k - 3) // 3, (k - 3) % 3
        x0 = 14 + c * 250
        y0 = 370 + r * 86
        card(img, x0, y0, 244, 80, tint(REGION[region], 0.88))
        img.rect(x0, y0, 244, 4, REGION[region])
        blit(img, x0 + 6, y0 + 10, 70, 64, art[num - 1])
        pline = "%d. %s" % (num, place)
        if place in CLOCK_MAP:
            pline += " - " + CLOCK_MAP[place]
        draw_text(img, x0 + 84, y0 + 10, pline, 1, REGION[region])
        for i, ln in enumerate(wrap_text(head, 152, 1)[:3]):
            draw_text(img, x0 + 84, y0 + 22 + i * 9, ln, 1, INK)
        for i, ln in enumerate(wrap_text(stand, 152, 1)[:2]):
            draw_text(img, x0 + 84, y0 + 50 + i * 9, ln, 1, (90, 90, 96))

    # the world map, on the left; the other 28 stories, plain coloured
    # text in one column on the right, no shapes
    draw_text(img, 14, 628, "THE WORLD IN ONE LOOK - 12 MAIN STORIES MARKED", 1, NAVY)
    draw_text(img, 414, 628, "ALSO ON THURSDAY 19 NOVEMBER 2026", 1, NAVY)
    markers = [(m[0], m[6][0], m[6][1], m[2]) for m in MAINS if m[6] is not None]
    draw_map(img, 14, 640, 390, 176, markers, BADGES)
    for i, (num, place, region, head) in enumerate(REST):
        y0 = 640 + i * 11
        num_s = "%d" % num
        pw = text_width(num_s, 1) + 6
        pill(img, 414, y0 - 1, pw, 10, REGION[region])
        draw_text(img, 414 + 3, y0, num_s, 1, (255, 255, 255))
        px = 414 + pw + 4
        draw_text(img, px, y0, place, 1, REGION[region])
        draw_text(img, px + text_width(place, 1), y0, " - %s" % head, 1, INK)

    # map key, under the map
    card(img, 14, 822, 390, 144)
    draw_text(img, 22, 830, "MAP KEY", 1, NAVY)
    lx, ly = 22, 844
    for region in ("ASIA", "EUROPE", "MIDEAST", "AMERICAS"):
        img.rect(lx, ly, 8, 8, REGION[region])
        lx += 11
        draw_text(img, lx, ly + 1, REGION_NAME[region], 1, INK)
        lx += text_width(REGION_NAME[region], 1) + 10
    lx, ly = 22, 860
    for region in ("AFRICA", "OCEANIA", "GLOBAL"):
        img.rect(lx, ly, 8, 8, REGION[region])
        lx += 11
        draw_text(img, lx, ly + 1, REGION_NAME[region], 1, INK)
        lx += text_width(REGION_NAME[region], 1) + 10
    draw_text(img, 22, 884, "Numbers on the map match the 12 main stories.", 1, (90, 90, 96))
    draw_text(img, 22, 893, "All 40 stories are from 19 November 2026.", 1, (90, 90, 96))
    draw_text(img, 22, 902, "Wires: Reuters, AP, BBC, AFP, Xinhua, IMD.", 1, (90, 90, 96))
    draw_text(img, 22, 911, "Pictures and map: original, drawn in code.", 1, (90, 90, 96))

    # date check + sources
    img.rect(14, 972, 740, 24, ROSE)
    dc = "DATE CHECK - Every story is from 19 November 2026 wires and briefs; 'says' means the claim is unconfirmed."
    draw_text(img, (W - text_width(dc, 1)) // 2, 980, dc, 1, INK)
    foot = "Sources: Reuters, AP, BBC, AFP, Xinhua, IMD, ESPNcricinfo and the day's wires - 19 November 2026"
    draw_text(img, (W - text_width(foot, 1)) // 2, 1002, foot, 1, (70, 80, 95))
    return img


def main():
    out = os.environ.get("OUTPUT", "/output/entry.png")
    img = build()
    n = write_png(img, out)
    print("wrote %s (%d bytes)" % (out, n))


if __name__ == "__main__":
    main()



