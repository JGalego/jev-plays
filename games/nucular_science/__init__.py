"""NucularScience: slow reactor management, which suits a model answering over HTTP."""

from games.spec import Game, Rom, pad

GAME = Game(
    slug="nucular_science",
    title="NucularScience",
    rom=Rom(
        filename="NucularScience.gba",
        licence="Zlib",
        provenance="LiquidFenrir/NucularScience (GBA Jam 2021)",
        url=None,
        note=(
            "The zlib licence would let us redistribute a build, but upstream publishes "
            "source only and no binary. Build it yourself with butano and devkitARM."
        ),
    ),
    objective=(
        "You are building a nuclear reactor that must not overheat. The game opens on a "
        "title screen you have to get through first. In play, you move the cursor over a "
        "grid, place and upgrade components, then run the reactor and sell the power."
    ),
    actions=pad(
        UP="Move the cursor up.",
        DOWN="Move the cursor down.",
        LEFT="Move the cursor left.",
        RIGHT="Move the cursor right.",
        A="Confirm: place or buy what is selected.",
        B="Cancel, or sell what the cursor is over.",
        L="Switch to the previous screen or component.",
        R="Switch to the next screen or component.",
        START="Advance the title screen, or end the day and run the reactor.",
        NOTHING="Send no input for this step.",
    ),
    boot_frames=600,
)
