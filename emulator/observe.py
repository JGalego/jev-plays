"""Turn a frame into compact text.

Everything here is descriptive. It reports what the hardware is showing -- brightness
cells, dominant colours, enabled sprites, how much moved -- and never ranks, scores or
recommends anything. A game may append its own decoded lines, but they follow the same rule.
"""

from __future__ import annotations

from collections import deque

from emulator.gba import HEIGHT, WIDTH, Sprite

# Five brightness steps, darkest first. Enough to make shapes legible as text.
_RAMP = " .:+#"
_COLOURS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "grey": (128, 128, 128),
    "red": (200, 40, 40),
    "green": (40, 170, 60),
    "blue": (50, 80, 200),
    "yellow": (220, 200, 60),
    "cyan": (60, 200, 210),
    "magenta": (190, 60, 190),
    "orange": (220, 130, 40),
    "brown": (120, 80, 40),
}


def screen_grid(image, cols: int = 30, rows: int = 20) -> list[str]:
    """Downsample the frame to a brightness grid, one character per cell."""

    small = image.convert("L").resize((cols, rows))
    pixels = list(small.getdata())
    lines = []
    for row in range(rows):
        cells = pixels[row * cols : (row + 1) * cols]
        lines.append("".join(_RAMP[min(value * len(_RAMP) // 256, len(_RAMP) - 1)] for value in cells))
    return lines


def motion(previous: list[str] | None, current: list[str]) -> float:
    """Share of grid cells that changed since the previous observation."""

    if previous is None or len(previous) != len(current):
        return 0.0
    pairs = zip(previous, current, strict=True)
    changed = sum(a != b for before, now in pairs for a, b in zip(before, now, strict=True))
    total = sum(len(line) for line in current)
    return changed / total if total else 0.0


def dominant_colours(image, top: int = 3) -> list[tuple[str, float]]:
    """Name the colours covering most of the screen, largest share first."""

    small = image.resize((60, 40))
    tally: dict[str, int] = {}
    for pixel in small.getdata():
        tally[_nearest_colour(pixel)] = tally.get(_nearest_colour(pixel), 0) + 1
    total = 60 * 40
    ranked = sorted(tally.items(), key=lambda item: (-item[1], item[0]))
    return [(name, count / total) for name, count in ranked[:top]]


def _nearest_colour(pixel: tuple[int, int, int]) -> str:
    red, green, blue = pixel[:3]
    return min(
        _COLOURS,
        key=lambda name: (
            (red - _COLOURS[name][0]) ** 2 + (green - _COLOURS[name][1]) ** 2 + (blue - _COLOURS[name][2]) ** 2
        ),
    )


def describe_sprites(sprites: list[Sprite], limit: int = 12) -> list[str]:
    """List the on-screen sprites, grouping identical artwork under one kind label."""

    visible = [s for s in sprites if -s.width < s.x < WIDTH and -s.height < s.y < HEIGHT]
    if not visible:
        return ["none on screen"]
    kinds: dict[tuple[int, int], str] = {}
    lines = []
    for sprite in visible[:limit]:
        key = (sprite.tile, sprite.palette)
        kind = kinds.setdefault(key, f"k{len(kinds)}")
        lines.append(f"{kind} at ({sprite.x},{sprite.y}) size {sprite.width}x{sprite.height}")
    if len(visible) > limit:
        lines.append(f"... and {len(visible) - limit} more")
    return lines


class Observer:
    """Looks at the emulator and writes down what it sees.

    It remembers the previous frame and the last few inputs so it can report what
    changed, which is a statement of fact about the past, not a suggestion about the
    future. It never inspects an action to judge whether it was a good one, and never
    says what to press next.
    """

    HISTORY = 5
    # Below this share of changed cells the frame is the same picture, just animated.
    STILL = 0.03

    def __init__(self, game) -> None:
        self._game = game
        self._grid: list[str] | None = None
        self._history: deque[tuple[str, float]] = deque(maxlen=self.HISTORY)
        self._pending: str | None = None

    def note(self, action: str, buttons: tuple[str, ...], hold_frames: int) -> None:
        """Record the input just sent; its effect is measured at the next look."""

        pressed = "+".join(buttons) or "no buttons"
        self._pending = f"{action} ({pressed}) held {hold_frames} frames"

    def _effects(self) -> list[str]:
        """Report what the recent inputs did, and say plainly when they did nothing."""

        if not self._history:
            return []
        lines = ["RECENT INPUTS, oldest first:"]
        for entry, changed in self._history:
            effect = "nothing visibly changed" if changed < self.STILL else f"{changed:.0%} of the screen then changed"
            lines.append(f"  - {entry} -> {effect}")
        dead = [entry.split(" ")[0] for entry, changed in self._history if changed < self.STILL]
        if len(dead) == len(self._history) and len(dead) > 1:
            unique = sorted(set(dead))
            lines.append(f"NOTHING HAS CHANGED for {len(dead)} looks in a row, after sending: {', '.join(unique)}.")
        return lines

    def look(self, emulator) -> str:
        """Describe the screen right now, as the text Jev is given."""

        image = emulator.screen()
        grid = screen_grid(image)
        changed = motion(self._grid, grid)
        if self._pending is not None:
            self._history.append((self._pending, changed))
            self._pending = None
        self._grid = grid

        colours = ", ".join(f"{name} {share:.0%}" for name, share in dominant_colours(image))
        lines = [
            f"GAME: {self._game.title}",
            f"OBJECTIVE: {self._game.objective}",
            "",
            f"FRAME: {emulator.frame} ({emulator.frame / 59.7:.0f}s since the game booted)",
            "SCREEN, one character per 8x8 tile, ' ' darkest to '#' brightest:",
            *(f"  |{line}|" for line in grid),
            f"COLOURS: {colours}",
            f"MOTION: {changed:.0%} of the screen changed since the last look",
            "SPRITES (moving objects the hardware is drawing):",
            *(f"  - {line}" for line in describe_sprites(emulator.sprites())),
            *self._effects(),
        ]
        if self._game.observe is not None:
            lines += self._game.observe(emulator)
        return "\n".join(lines)
