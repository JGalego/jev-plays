"""The game registry. Adding a game means adding a module here and one line below."""

from __future__ import annotations

import importlib

from games.spec import Action, Game, Rom

SLUGS = (
    "anguna",
    "gba_tactics",
    "duster",
    "nucular_science",
    "skyland",
    "solar_guard",
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
