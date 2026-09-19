"""Duster: a strategy board game. Simple, turn-based, and forgiving of slow decisions."""

from games.spec import Game, Rom, pad

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
        "You play a turn-based battle on a board of tiles. The game opens on a title "
        "screen and menus you have to get through first. In play, you move the cursor to "
        "one of your pieces, select it, and move or attack with it."
    ),
    actions=pad(
        UP="Move the cursor up.",
        DOWN="Move the cursor down.",
        LEFT="Move the cursor left.",
        RIGHT="Move the cursor right.",
        A="Confirm: select a piece, a destination or a menu entry.",
        B="Back out of the current selection.",
        START="Begin the game, or open the menu.",
        NOTHING="Send no input for this step.",
    ),
    boot_frames=500,
)
