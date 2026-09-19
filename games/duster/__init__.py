"""Duster: a strategy board game. Simple, turn-based, and forgiving of slow decisions."""

from games.spec import Action, Game, Rom

GAME = Game(
    slug="duster",
    title="Duster",
    rom=Rom(
        filename="Duster.gba",
        licence="Unknown",
        provenance="bmchtech/duster, later redthing1/duster -- both now removed from GitHub",
        url=None,
        note=(
            "Upstream is gone and no licence survives anywhere we could check, so its "
            "redistribution status is unclear and we do not fetch or ship it."
            "Point DUSTER_ROM at your own copy."
        ),
    ),
    objective=(
        "You play a turn-based battle on a board of tiles. Move the cursor to one of your "
        "pieces, select it, and move or attack with it."
    ),
    actions={
        "UP": Action(("UP",), "Move the cursor up."),
        "DOWN": Action(("DOWN",), "Move the cursor down."),
        "LEFT": Action(("LEFT",), "Move the cursor left."),
        "RIGHT": Action(("RIGHT",), "Move the cursor right."),
        "CONFIRM": Action(("A",), "Confirm: select a piece, a destination or a menu entry."),
        "CANCEL": Action(("B",), "Back out of the current selection."),
        "START": Action(("START",), "Press start to begin, or to open the menu."),
        "WAIT": Action((), "Send no input and let the game run on."),
    },
    boot_frames=500,
)
