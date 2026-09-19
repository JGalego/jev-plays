"""Thin wrapper over the mGBA Python bindings.

This module knows how to load a ROM, hold buttons for a number of frames, and read
back the screen, the sprite table and raw memory. It knows nothing about any game and
makes no decisions: everything here is either an instruction from the caller or an
observation handed back to it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import mgba.core
import mgba.image
from mgba.gba import GBA

# The ten physical GBA inputs, plus the empty action.
BUTTONS = ("A", "B", "SELECT", "START", "RIGHT", "LEFT", "UP", "DOWN", "R", "L")
NOTHING = "NONE"

_KEYS = {name: getattr(GBA, f"KEY_{name}") for name in BUTTONS}

WIDTH, HEIGHT = 240, 160

# OAM holds 128 objects of four 16-bit attributes each; we read the first three.
_OAM_ENTRIES = 128
_OAM_STRIDE = 8
_OBJ_DISABLED = 0x0200
_OBJ_MODE_MASK = 0x0300
# Object pixel sizes, indexed by attr0 shape then attr1 size (GBA hardware table).
_OBJ_SIZES = (
    ((8, 8), (16, 16), (32, 32), (64, 64)),
    ((16, 8), (32, 8), (32, 16), (64, 32)),
    ((8, 16), (8, 32), (16, 32), (32, 64)),
    ((8, 8), (8, 8), (8, 8), (8, 8)),
)


@dataclass(frozen=True, slots=True)
class Sprite:
    """One enabled hardware object, as the GBA itself describes it."""

    index: int
    x: int
    y: int
    width: int
    height: int
    tile: int
    palette: int


class Emulator:
    """One running GBA. Construct it, press things, look at it."""

    def __init__(self, rom_path: str | Path) -> None:
        self.rom_path = Path(rom_path)
        if not self.rom_path.is_file():
            raise FileNotFoundError(f"ROM not found: {self.rom_path}")
        core = mgba.core.load_path(str(self.rom_path))
        if core is None:
            raise RuntimeError(f"mGBA could not load {self.rom_path}")
        self._core = core
        self._image = mgba.image.Image(*core.desired_video_dimensions())
        core.set_video_buffer(self._image)
        core.reset()
        self.title = core.game_title

    @property
    def frame(self) -> int:
        """Frames emulated since reset (the GBA runs at ~59.7 of them per second)."""

        return self._core.frame_counter

    def run_frames(self, count: int) -> None:
        """Advance the emulation with no input held."""

        self._core.clear_keys(*_KEYS.values())
        for _ in range(count):
            self._core.run_frame()

    def press(self, buttons: tuple[str, ...], hold: int, release: int = 2) -> None:
        """Hold `buttons` for `hold` frames, then let go for `release` frames."""

        unknown = set(buttons) - set(BUTTONS)
        if unknown:
            raise ValueError(f"not GBA buttons: {sorted(unknown)}")
        keys = [_KEYS[name] for name in buttons]
        self._core.clear_keys(*_KEYS.values())
        if keys:
            self._core.set_keys(*keys)
        for _ in range(hold):
            self._core.run_frame()
        self._core.clear_keys(*_KEYS.values())
        for _ in range(release):
            self._core.run_frame()

    def screen(self):
        """The current framebuffer as a PIL image."""

        return self._image.to_pil().convert("RGB")

    def sprites(self) -> list[Sprite]:
        """Every enabled hardware object, decoded straight out of OAM.

        We read the attribute words rather than going through mGBA's sprite helper,
        which would build a tile cache we have no use for.
        """

        oam = self._core.memory.oam.u16
        found = []
        for index in range(_OAM_ENTRIES):
            base = index * _OAM_STRIDE
            attr0, attr1, attr2 = oam[base], oam[base + 2], oam[base + 4]
            if not (attr0 | attr1 | attr2):
                continue  # an OAM entry the game never wrote to
            if attr0 & _OBJ_MODE_MASK == _OBJ_DISABLED:
                continue
            width, height = _OBJ_SIZES[attr0 >> 14][attr1 >> 14]
            x, y = attr1 & 0x1FF, attr0 & 0xFF
            found.append(
                Sprite(
                    index=index,
                    # X is 9-bit signed and Y is 8-bit signed, so high values are off-screen.
                    x=x - 512 if x >= 256 else x,
                    y=y - 256 if y >= HEIGHT else y,
                    width=width,
                    height=height,
                    tile=attr2 & 0x3FF,
                    palette=attr2 >> 12,
                )
            )
        return found

    def read_u8(self, address: int) -> int:
        """Read one byte off the bus, for games with a known memory layout."""

        return self._core.memory.u8[address]

    def read_u16(self, address: int) -> int:
        """Read one halfword off the bus."""

        return self._core.memory.u16[address]
