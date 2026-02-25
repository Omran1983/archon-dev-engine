#!/usr/bin/env python3
"""
ARCHON Demo GIF Generator
Creates an animated terminal-style GIF showing the ARCHON veto in action.
"""
from PIL import Image, ImageDraw, ImageFont
import os

# --- Config ---
W, H = 720, 400
BG = (18, 18, 18)
GREEN = (80, 220, 100)
RED = (220, 60, 60)
YELLOW = (220, 180, 50)
GRAY = (140, 140, 140)
WHITE = (230, 230, 230)
FONT_SIZE = 16
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "demo.gif")

# Try to load a monospace font, fall back gracefully
def get_font(size=FONT_SIZE):
    paths = [
        "C:/Windows/Fonts/consola.ttf",  # Consolas (Windows)
        "C:/Windows/Fonts/cour.ttf",      # Courier New (Windows)
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

FONT = get_font()
FONT_BOLD = get_font(FONT_SIZE + 2)

def make_frame(lines):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # Header bar
    draw.rectangle([(0, 0), (W, 36)], fill=(30, 30, 30))
    draw.text((16, 10), "● ● ●", font=FONT, fill=GRAY)
    draw.text((W // 2 - 80, 10), "ARCHON Dev Engine v0.1.0", font=FONT, fill=GRAY)
    # Body lines
    y = 52
    for color, text in lines:
        draw.text((20, y), text, font=FONT, fill=color)
        y += 26
    return img

# --- Scene definitions ---
scenes = [
    # (duration_ms, lines)
    (800, [
        (GRAY, "$ python scripts/guard.py app/routes/user.py"),
        (GRAY, ""),
        (GRAY, "Scanning: app/routes/user.py ..."),
    ]),
    (600, [
        (GRAY, "$ python scripts/guard.py app/routes/user.py"),
        (GRAY, ""),
        (GREEN, "[ OK ] Config Discipline: No hardcoded secrets."),
    ]),
    (600, [
        (GRAY, "$ python scripts/guard.py app/routes/user.py"),
        (GRAY, ""),
        (GREEN, "[ OK ] Config Discipline: No hardcoded secrets."),
        (GREEN, "[ OK ] Structured Output: JSON schema detected."),
    ]),
    (900, [
        (GRAY, "$ python scripts/guard.py app/routes/user.py"),
        (GRAY, ""),
        (GREEN, "[ OK ] Config Discipline: No hardcoded secrets."),
        (GREEN, "[ OK ] Structured Output: JSON schema detected."),
        (RED,   "[ VETO ] Async-First Violation — Line 14"),
    ]),
    (1200, [
        (GRAY, "$ python scripts/guard.py app/routes/user.py"),
        (GRAY, ""),
        (GREEN, "[ OK ] Config Discipline: No hardcoded secrets."),
        (GREEN, "[ OK ] Structured Output: JSON schema detected."),
        (RED,   "[ VETO ] Async-First Violation — Line 14"),
        (RED,   "         requests.get() blocks the event loop."),
        (RED,   "         Use httpx.AsyncClient instead."),
        (GRAY,  ""),
        (YELLOW,"[ INFO ] ARCHON prevented a high-risk backend pattern."),
    ]),
    (1000, [
        (GRAY, "$ python scripts/guard.py app/routes/user.py"),
        (GRAY, ""),
        (GREEN, "[ OK ] Config Discipline: No hardcoded secrets."),
        (GREEN, "[ OK ] Structured Output: JSON schema detected."),
        (RED,   "[ VETO ] Async-First Violation — Line 14"),
        (RED,   "         requests.get() blocks the event loop."),
        (RED,   "         Use httpx.AsyncClient instead."),
        (GRAY,  ""),
        (YELLOW,"[ INFO ] ARCHON prevented a high-risk backend pattern."),
        (GRAY,  ""),
        (GRAY,  "Commit blocked. Fix violation to proceed."),
    ]),
    (2000, [
        (GRAY, "$ python scripts/guard.py app/routes/user.py"),
        (GRAY, ""),
        (GREEN, "[ OK ] Config Discipline: No hardcoded secrets."),
        (GREEN, "[ OK ] Structured Output: JSON schema detected."),
        (RED,   "[ VETO ] Async-First Violation — Line 14"),
        (RED,   "         requests.get() blocks the event loop."),
        (RED,   "         Use httpx.AsyncClient instead."),
        (GRAY,  ""),
        (YELLOW,"[ INFO ] ARCHON prevented a high-risk backend pattern."),
        (GRAY,  ""),
        (GRAY,  "Commit blocked. Fix violation to proceed."),
        (GRAY,  ""),
        (WHITE, "  github.com/Omran1983/archon-dev-engine"),
    ]),
]

frames = []
durations = []
for ms, lines in scenes:
    frames.append(make_frame(lines))
    durations.append(ms)

frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=False
)
print(f"[OK] Demo GIF saved to: {os.path.abspath(OUTPUT)}")
