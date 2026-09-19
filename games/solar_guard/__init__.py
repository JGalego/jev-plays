"""Solar Guard: an action shooter. The hardest fit for a model that answers over HTTP."""

from games.spec import Action, Game, Rom

GAME = Game(
    slug="solar_guard",
    title="Solar Guard",
    rom=Rom(
        filename="Solar_Guard.gba",
        licence="GPL-3.0-only",
        provenance="Deft-Spade/Solar-Guard release GBA-JAM-2021",
        url="https://github.com/Deft-Spade/Solar-Guard/releases/download/GBA-JAM-2021/Solar_Guard_GBA_JAM_2021.gba",
        sha256="cfd07990e0fa05611fb36b3230d68cea4b65ae11482e822b5b6f97a32a8b88b0",
    ),
    objective=(
        "You pilot a ship under attack. Get past the title screen, then move to dodge "
        "what is coming at you and shoot back."
    ),
    actions={
        "UP": Action(("UP",), "Move up, or move the menu selection up."),
        "DOWN": Action(("DOWN",), "Move down, or move the menu selection down."),
        "LEFT": Action(("LEFT",), "Move left."),
        "RIGHT": Action(("RIGHT",), "Move right."),
        "FIRE": Action(("A",), "Fire, or confirm a menu entry."),
        "SECONDARY": Action(("B",), "Secondary action, or cancel."),
        "START": Action(("START",), "Press start to begin or to pause."),
        "WAIT": Action((), "Send no input and let the game run on."),
    },
    boot_frames=700,
)
