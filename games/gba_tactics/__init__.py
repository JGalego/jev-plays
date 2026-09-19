"""GBA Tactics: turn-based squad combat, driven entirely through menus and a cursor."""

from games.spec import Game, Rom, pad

GAME = Game(
    slug="gba_tactics",
    title="GBA Tactics",
    machine="gba",
    rom=Rom(
        filename="gbatactics.gba",
        licence="GPL-2.0-or-later",
        provenance="retrobrews/gba-games (David Galvez Roca, 2006)",
        url="https://raw.githubusercontent.com/retrobrews/gba-games/master/gbatactics.gba",
        sha256="34967b4b0542c42631cc5f783bd4b553d8b430fbade05001acd303ed41455a94",
        companions=(
            ("gbatactics.txt", "https://raw.githubusercontent.com/retrobrews/gba-games/master/gbatactics.txt"),
        ),
        note=(
            "GPLv2 binary. We fetch it rather than bundle it: redistributing the binary "
            "would oblige us to ship the corresponding source, which upstream never published."
        ),
    ),
    objective=(
        "You command a squad on a grid and must defeat every unit on the other side. The "
        "game opens on a title screen and a menu you have to get through first. In play, "
        "you move the cursor over a unit, select it, and work through the action menus."
    ),
    actions=pad(
        UP="Move the cursor or menu selection up.",
        DOWN="Move the cursor or menu selection down.",
        LEFT="Move the cursor or menu selection left.",
        RIGHT="Move the cursor or menu selection right.",
        A="Confirm: pick the unit, tile or menu entry under the cursor.",
        B="Back out of the current selection or menu.",
        START="Start the game from the title screen, or open the turn menu.",
        NOTHING="Send no input for this step.",
    ),
    boot_frames=420,
)
