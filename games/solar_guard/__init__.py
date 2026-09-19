"""Solar Guard: an action shooter. The hardest fit for a model that answers over HTTP."""

from games.spec import Game, Rom, pad

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
        "You pilot a ship under attack. The game opens on a title screen, then a menu "
        "whose entries include starting a mission. In flight, you move to dodge what is "
        "coming at you and shoot back."
    ),
    actions=pad(
        UP="Fly up; moves the menu selection up.",
        DOWN="Fly down; moves the menu selection down.",
        LEFT="Fly left.",
        RIGHT="Fly right.",
        A="Fire your weapon in flight; confirms the highlighted entry in a menu.",
        B="Secondary action in flight; cancels or backs out in a menu.",
        START="Leave the title screen; pauses during a mission.",
        NOTHING="Send no input for this step.",
    ),
    boot_frames=700,
)
