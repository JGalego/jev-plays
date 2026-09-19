"""Skyland: a realtime strategy game about keeping a flying castle in one piece."""

from games.spec import Action, Game, Rom

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
        "You run a castle floating in the sky. Move the cursor around the castle, place "
        "and repair rooms, and survive the raiders that arrive from the right."
    ),
    actions={
        "UP": Action(("UP",), "Move the cursor up."),
        "DOWN": Action(("DOWN",), "Move the cursor down."),
        "LEFT": Action(("LEFT",), "Move the cursor left, towards your own castle."),
        "RIGHT": Action(("RIGHT",), "Move the cursor right, towards the opposing castle."),
        "CONFIRM": Action(("A",), "Confirm: select what the cursor is over, or accept a menu entry."),
        "CANCEL": Action(("B",), "Back out, or deselect."),
        "PREV_TAB": Action(("L",), "Switch to the previous menu or view."),
        "NEXT_TAB": Action(("R",), "Switch to the next menu or view."),
        "START": Action(("START",), "Press start: advance the title screen or open the pause menu."),
        "SELECT": Action(("SELECT",), "Press select, which toggles the secondary view."),
        "WAIT": Action((), "Send no input and let the game run on."),
    },
    boot_frames=700,
)
