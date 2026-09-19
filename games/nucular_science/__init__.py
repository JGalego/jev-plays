"""NucularScience: slow reactor management, which suits a model answering over HTTP."""

from games.spec import Action, Game, Rom

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
        "You are building a nuclear reactor that must not overheat. Move the cursor over "
        "the grid, place and upgrade components, then run the reactor and sell the power."
    ),
    actions={
        "UP": Action(("UP",), "Move the cursor up."),
        "DOWN": Action(("DOWN",), "Move the cursor down."),
        "LEFT": Action(("LEFT",), "Move the cursor left."),
        "RIGHT": Action(("RIGHT",), "Move the cursor right."),
        "CONFIRM": Action(("A",), "Confirm: place or buy what is selected."),
        "CANCEL": Action(("B",), "Cancel, or sell what the cursor is over."),
        "PREV_TAB": Action(("L",), "Switch to the previous screen or component."),
        "NEXT_TAB": Action(("R",), "Switch to the next screen or component."),
        "START": Action(("START",), "Press start to advance the title screen or end the day."),
        "WAIT": Action((), "Send no input and let the reactor run."),
    },
    boot_frames=600,
)
