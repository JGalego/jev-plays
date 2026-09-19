"""Skyland: a realtime strategy game about keeping a flying castle in one piece."""

from games.spec import Game, Rom, pad

GAME = Game(
    slug="skyland",
    title="Skyland",
    rom=Rom(
        filename="Skyland.gba",
        licence="MPL-2.0",
        provenance="evanbowman/skyland-gba release 2022.1.7.0 (GBA Jam 2021)",
        url="https://github.com/evanbowman/skyland-gba/releases/download/2022.1.7.0/Skyland.gba",
        sha256="516f185f206366f9d44ed2df0d8afb2bc0e2f7d3adc2a2ed6e686c6c3eb4ac90",
    ),
    objective=(
        "You run a castle floating in the sky. The game opens on a title screen and a "
        "menu you have to get through first. In play, you move a cursor around the "
        "castle, place and repair rooms, and survive the raiders arriving from the right."
    ),
    actions=pad(
        UP="Move the cursor up.",
        DOWN="Move the cursor down.",
        LEFT="Move the cursor left, towards your own castle.",
        RIGHT="Move the cursor right, towards the opposing castle.",
        A="Confirm: choose the highlighted menu entry, or select what the cursor is over.",
        B="Back out, or deselect.",
        L="Switch to the previous menu or view.",
        R="Switch to the next menu or view.",
        START="Open the pause menu.",
        SELECT="Toggle the secondary view.",
        NOTHING="Send no input for this step.",
    ),
    boot_frames=700,
)
