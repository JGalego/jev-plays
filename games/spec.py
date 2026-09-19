"""What a game contributes to the loop: a ROM, an objective, and a set of inputs."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Action:
    """One entry in the pad vocabulary Jev chooses from."""

    buttons: tuple[str, ...]
    description: str


@dataclass(frozen=True, slots=True)
class Rom:
    """Where a ROM comes from and what its licence allows.

    `url` is None when nobody publishes a binary we are clearly allowed to redistribute;
    those games only run from a ROM the user supplies.
    """

    filename: str
    licence: str
    provenance: str
    url: str | None = None
    sha256: str | None = None
    companions: tuple[tuple[str, str], ...] = ()
    note: str = ""


@dataclass(frozen=True, slots=True)
class Game:
    """Everything game-specific in one place."""

    slug: str
    title: str
    rom: Rom
    objective: str
    actions: Mapping[str, Action]
    boot_frames: int
    # Optional game-specific observer. It receives the emulator and returns extra
    # descriptive lines to append -- decoded HP, a board, a menu -- never a suggestion.
    observe: Callable[..., list[str]] | None = field(default=None)

    def criteria(self) -> dict[str, str]:
        """The choice labels and descriptions handed to Jev."""

        return {label: action.description for label, action in self.actions.items()}
