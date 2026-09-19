"""Finding and fetching ROMs.

No ROM is committed to this repository. Four of the six are fetched from the upstream
that publishes them under a licence we checked; the other two only ever run from a copy
the user supplies. See the licence notes in each game module and in the README.
"""

from __future__ import annotations

import hashlib
import os
import urllib.request
from pathlib import Path

from games.spec import Game

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIR = Path(os.environ.get("JEV_PLAYS_ROMS", ROOT / "roms"))


def env_var(game: Game) -> str:
    """The per-game override, e.g. ANGUNA_ROM."""

    return f"{game.slug.upper()}_ROM"


def resolve(game: Game) -> Path:
    """Where this game's ROM is, checking the env override before the ROM directory."""

    override = os.environ.get(env_var(game))
    if override:
        path = Path(override).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"{env_var(game)} points at {path}, which is not a file")
        return path
    return DEFAULT_DIR / game.rom.filename


def fetch(game: Game, directory: Path = DEFAULT_DIR) -> Path:
    """Download the ROM if its licence lets us, and check the digest we recorded."""

    if game.rom.url is None:
        raise PermissionError(
            f"{game.title}: no ROM we may redistribute or fetch ({game.rom.licence}). "
            f"{game.rom.note} Set {env_var(game)} to your own copy."
        )
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / game.rom.filename
    for name, url in ((game.rom.filename, game.rom.url), *game.rom.companions):
        destination = directory / name
        if destination.exists():
            continue
        with urllib.request.urlopen(url) as response:
            destination.write_bytes(response.read())
    if game.rom.sha256:
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest != game.rom.sha256:
            raise ValueError(f"{target} has digest {digest}, expected {game.rom.sha256}")
    return target
