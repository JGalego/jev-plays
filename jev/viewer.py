"""Render what Jev was given and what it pressed, beside the game, as one GIF frame."""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from emulator.gba import HEIGHT, WIDTH

SCALE = 2
SCREEN = (WIDTH * SCALE, HEIGHT * SCALE)
PANEL_WIDTH = 400
MARGIN = 14
LINE = 12
CANVAS = (SCREEN[0] + PANEL_WIDTH, 524)
WRAP = 62

_BACKGROUND = (17, 17, 21)
_RULE = (58, 58, 68)
_LABEL = (126, 128, 142)
_TEXT = (212, 214, 222)
_ACTION = (126, 224, 160)

_FONTS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono",
    "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular",
)


def _font(size: int, bold: bool = False):
    for stem in _FONTS:
        path = f"{stem}{'-Bold' if bold else ''}.ttf"
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def _wrapped(observation: str) -> list[str]:
    """Fold the observation to the panel width, leaving the screen grid intact."""

    lines: list[str] = []
    for line in observation.splitlines():
        lines.extend(textwrap.wrap(line, WRAP, subsequent_indent="  ") if len(line) > WRAP else [line])
    return lines


def compose(screen: Image.Image, title: str, step: str, observation: str, decision: list[str]) -> Image.Image:
    """One frame: the game and Jev's input on the left, the text Jev was given on the right."""

    small, mono, bold = _font(10), _font(10), _font(13, bold=True)
    canvas = Image.new("RGB", CANVAS, _BACKGROUND)
    canvas.paste(screen.resize(SCREEN, Image.NEAREST), (0, 40))
    draw = ImageDraw.Draw(canvas)

    draw.text((MARGIN, 13), title, font=bold, fill=_TEXT)
    draw.text((SCREEN[0] - MARGIN - 70, 15), step, font=small, fill=_LABEL)
    draw.line((0, 34, CANVAS[0], 34), fill=_RULE)
    draw.line((SCREEN[0], 0, SCREEN[0], CANVAS[1]), fill=_RULE)

    y = 40 + SCREEN[1] + 24
    draw.text((MARGIN, y), "WHAT JEV PRESSED", font=small, fill=_LABEL)
    draw.text((MARGIN, y + 20), decision[0], font=bold, fill=_ACTION)
    for offset, line in enumerate(decision[1:]):
        draw.text((MARGIN, y + 42 + offset * LINE), line, font=mono, fill=_TEXT)

    left = SCREEN[0] + MARGIN
    draw.text((left, 13), "WHAT JEV IS GIVEN", font=small, fill=_LABEL)
    y = 42
    for line in _wrapped(observation):
        if y > CANVAS[1] - LINE:
            draw.text((left, y), "...", font=mono, fill=_LABEL)
            break
        draw.text((left, y), line, font=mono, fill=_TEXT)
        y += LINE
    return canvas


def save_gif(frames: list[Image.Image], path: Path, frame_ms: int = 260) -> None:
    """Write the composed frames out as a looping GIF.

    Every frame is quantised against one shared palette. Per-frame palettes would make
    each frame self-contained and roughly triple the file.
    """

    if not frames:
        return
    sample = Image.new("RGB", (CANVAS[0], CANVAS[1] * min(len(frames), 8)))
    for index, frame in enumerate(frames[:: max(1, len(frames) // 8)][:8]):
        sample.paste(frame, (0, index * CANVAS[1]))
    shared = sample.quantize(colors=64, method=Image.MEDIANCUT)
    quantised = [frame.quantize(palette=shared, dither=Image.Dither.NONE) for frame in frames]
    quantised[0].save(path, save_all=True, append_images=quantised[1:], duration=frame_ms, loop=0, optimize=True)
