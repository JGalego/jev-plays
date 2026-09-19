"""The game registry. Adding a game means adding a module here and one line below."""

from __future__ import annotations

import importlib

from games.spec import Action, Game, Rom

SLUGS = (
    # Game Boy Advance, through mGBA
    "anguna",
    "gba_tactics",
    "duster",
    "nucular_science",
    "skyland",
    "solar_guard",
    # Atari 2600, through the Arcade Learning Environment
    "a2600_2048",
    "a2600_pipes",
    "a2600_bounstryk",
    # Atari 2600 classics, run from the copies ale-py put on your own disk
    "a2600_breakout",
    "a2600_pong",
    "a2600_space_invaders",
    "a2600_freeway",
)

__all__ = ["SLUGS", "Action", "Game", "Rom", "all_games", "load"]


def load(slug: str) -> Game:
    """Import one game module and hand back its definition."""

    if slug not in SLUGS:
        raise KeyError(f"unknown game {slug!r}; known: {', '.join(SLUGS)}")
    return importlib.import_module(f"games.{slug}").GAME


def all_games() -> list[Game]:
    """Every registered game, in registry order."""

    return [load(slug) for slug in SLUGS]
