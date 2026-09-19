"""Turn a frame into compact text.

Everything here is descriptive. It reports what the hardware is showing -- brightness
cells, dominant colours, enabled sprites, how much moved -- and never ranks, scores or
recommends anything. A game may append its own decoded lines, but they follow the same rule.
"""

from __future__ import annotations

from collections import Counter, deque

from PIL import Image, ImageFilter

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


def screen_grid(image, cols: int = 30, rows: int = 20, pool: str = "average") -> list[str]:
    """Downsample the frame to a brightness grid, one character per cell.

    Averaging keeps dense tile art legible but erases anything small: a two-pixel ball
    contributes almost nothing to the mean of its cell and simply disappears. Consoles
    that draw a few tiny objects on flat backgrounds ask for `max` instead, which keeps
    the brightest pixel in each cell and so keeps the ball.
    """

    grey = image.convert("L")
    if pool == "max":
        grey = grey.filter(ImageFilter.MaxFilter(5))
    small = grey.resize((cols, rows))
    pixels = list(small.getdata())
    lines = []
    for row in range(rows):
        cells = pixels[row * cols : (row + 1) * cols]
        lines.append("".join(_RAMP[min(value * len(_RAMP) // 256, len(_RAMP) - 1)] for value in cells))
    return lines


def moved_cells(previous: list[str] | None, current: list[str], limit: int = 10) -> list[str]:
    """Name the grid cells that changed, so a moving object has a reported position."""

    if previous is None or len(previous) != len(current):
        return []
    cells = [
        f"({x},{y})"
        for y, (before, now) in enumerate(zip(previous, current, strict=True))
        for x, (a, b) in enumerate(zip(before, now, strict=True))
        if a != b
    ]
    return cells[:limit] + ([f"and {len(cells) - limit} more"] if len(cells) > limit else [])


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


def describe_sprites(sprites, screen: tuple[int, int], limit: int = 12) -> list[str]:
    """List the on-screen sprites, grouping identical artwork under one kind label."""

    width, height = screen
    visible = [s for s in sprites if -s.width < s.x < width and -s.height < s.y < height]
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


def find_objects(image, sample: int = 2, widest: int = 80, limit: int = 8) -> list[str]:
    """Pick out the small shapes drawn over the background, smallest first.

    A console with no sprite table still draws its ball and its bat as small blocks of
    one colour on a flat background, so they can be read back off the frame. This only
    reports what is there and how big it is; it does not say which one matters.
    """

    width, height = image.size
    cols, rows = width // sample, height // sample
    pixels = list(image.resize((cols, rows), Image.NEAREST).get_flattened_data())
    background = Counter(pixels).most_common(1)[0][0]

    seen = bytearray(cols * rows)
    found = []
    for start in range(cols * rows):
        if seen[start] or pixels[start] == background:
            continue
        colour = pixels[start]
        queue, cells = deque([start]), []
        seen[start] = 1
        while queue:
            index = queue.popleft()
            cells.append(index)
            x, y = index % cols, index // cols
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < cols and 0 <= ny < rows:
                    neighbour = ny * cols + nx
                    if not seen[neighbour] and pixels[neighbour] == colour:
                        seen[neighbour] = 1
                        queue.append(neighbour)
        xs = [c % cols for c in cells]
        ys = [c // cols for c in cells]
        box = ((max(xs) - min(xs) + 1) * sample, (max(ys) - min(ys) + 1) * sample)
        if box[0] <= widest:
            found.append((box[0] * box[1], min(xs) * sample, min(ys) * sample, *box))
    found.sort()
    return [f"{w}x{h} at ({x},{y})" for _, x, y, w, h in found[:limit]] or ["none found"]


def describe_ram(ram, previous, base: int = 0x80, limit: int = 12) -> list[str]:
    """Dump console RAM, and name the bytes that changed since the last look.

    The 2600 has 128 bytes in total, so the whole machine state fits in the observation
    and nothing has to be guessed at or interpreted here.
    """

    rows = [
        f"  {base + offset:02x}: " + " ".join(f"{value:02x}" for value in ram[offset : offset + 16])
        for offset in range(0, len(ram), 16)
    ]
    lines = []
    if previous is not None and len(previous) == len(ram):
        changed = [(i, int(previous[i]), int(ram[i])) for i in range(len(ram)) if previous[i] != ram[i]]
        if not changed:
            lines.append("RAM CHANGED: no byte changed since the last look")
        else:
            shown = ", ".join(f"{base + i:02x}: {was}->{now}" for i, was, now in changed[:limit])
            more = f", and {len(changed) - limit} more" if len(changed) > limit else ""
            lines.append(f"RAM CHANGED ({len(changed)} bytes): {shown}{more}")
    lines += [f"RAM, all {len(ram)} bytes, 16 per row from address {base:#04x}:", *rows]
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
        self._ram = None

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

    def _machine_state(self, emulator, image) -> list[str]:
        """Whatever this console can say about itself beyond the brightness grid."""

        lines: list[str] = []
        if hasattr(emulator, "sprites"):
            lines += [
                "SPRITES (moving objects the hardware is drawing):",
                *(f"  - {line}" for line in describe_sprites(emulator.sprites(), image.size)),
            ]
        else:
            lines += [
                f"OBJECTS on a {image.width}x{image.height} screen, smallest first:",
                *(f"  - {line}" for line in find_objects(image)),
            ]
        if hasattr(emulator, "ram"):
            ram = emulator.ram()
            lines += describe_ram(ram, self._ram)
            self._ram = ram.copy()
        return lines

    def look(self, emulator) -> str:
        """Describe the screen right now, as the text Jev is given."""

        image = emulator.screen()
        grid = screen_grid(image, pool=getattr(emulator, "screen_pool", "average"))
        changed = motion(self._grid, grid)
        moved = moved_cells(self._grid, grid)
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
            *([f"MOVED: cells at column,row {', '.join(moved)}"] if moved else []),
            *self._effects(),
            *self._machine_state(emulator, image),
        ]
        if self._game.observe is not None:
            lines += self._game.observe(emulator)
        return "\n".join(lines)
