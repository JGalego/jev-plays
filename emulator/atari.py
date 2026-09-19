"""Thin wrapper over the Arcade Learning Environment (Stella) for the Atari 2600.

Same contract as the mGBA adapter: load a ROM, hold an input for a number of frames,
read back the screen and memory. It makes no decisions.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import numpy as np
from ale_py import Action, ALEInterface, LoggerMode
from PIL import Image

# The 2600 pad is one stick and one button, which ALE enumerates as 18 combinations.
BUTTONS = tuple(action.name for action in Action)
NOOP = "NOOP"

WIDTH, HEIGHT = 160, 210
RAM_BASE = 0x80

# ALE only accepts ROMs whose MD5 is in its table of 108 commercial titles, and otherwise
# falls back to matching on the filename. No homebrew is in that table, so we hand it a
# copy named after a game it does know. The name only picks ALE's scoring and
# end-of-episode rules, which this repository never reads: Jev plays from the screen and
# RAM, and nothing here keeps score.
#
# A ROM ALE already recognises is loaded as-is. Aliasing one of those attaches the wrong
# game's reset logic, which for Space Invaders under Adventure's rules never returns.
_ALIAS = "adventure.bin"


class Emulator:
    """One running 2600. Construct it, press things, look at it."""

    # The 2600 draws a handful of tiny objects on flat colour, so averaging the frame
    # down to text loses the ball and the bat entirely. See `observe.screen_grid`.
    screen_pool = "max"

    def __init__(self, rom_path: str | Path) -> None:
        self.rom_path = Path(rom_path)
        if not self.rom_path.is_file():
            raise FileNotFoundError(f"ROM not found: {self.rom_path}")
        ALEInterface.setLoggerMode(LoggerMode.Error)
        self._ale = ALEInterface()
        self._workdir = None
        if self._ale.isSupportedROM(self.rom_path) is not None:
            self._ale.loadROM(self.rom_path)
        else:
            self._workdir = tempfile.TemporaryDirectory(prefix="jev-plays-")
            alias = Path(self._workdir.name) / _ALIAS
            shutil.copy(self.rom_path, alias)
            self._ale.loadROM(alias)
        self._ale.reset_game()
        self._actions = {action.name: action for action in Action}
        self.title = self.rom_path.stem

    @property
    def frame(self) -> int:
        """Frames emulated since reset (the 2600 runs at about 60 of them per second)."""

        return self._ale.getEpisodeFrameNumber()

    def run_frames(self, count: int) -> None:
        """Advance the emulation with the stick centred and the button up."""

        for _ in range(count):
            self._ale.act(self._actions[NOOP])

    def press(self, buttons: tuple[str, ...], hold: int, release: int = 2) -> None:
        """Hold `buttons` for `hold` frames, then let go for `release` frames."""

        name = buttons[0] if buttons else NOOP
        if name not in self._actions:
            raise ValueError(f"not a 2600 input: {name!r}")
        for _ in range(hold):
            self._ale.act(self._actions[name])
        self.run_frames(release)

    def screen(self) -> Image.Image:
        """The current frame as a PIL image."""

        return Image.fromarray(self._ale.getScreenRGB()).convert("RGB")

    def ram(self) -> np.ndarray:
        """All 128 bytes of console RAM, which on this machine is the whole game state."""

        return self._ale.getRAM()
