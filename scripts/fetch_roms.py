#!/usr/bin/env python
"""Fetch the ROMs whose licences allow it. Run with no arguments to get all of them."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import games
from games import roms


def main() -> int:
    wanted = sys.argv[1:] or list(games.SLUGS)
    for slug in wanted:
        game = games.load(slug)
        try:
            path = roms.fetch(game)
        except PermissionError as error:
            # Expected for the games nobody publishes a redistributable binary for.
            print(f"skip  {slug:16} {error}")
        else:
            print(f"ok    {slug:16} {path} ({game.rom.licence})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
