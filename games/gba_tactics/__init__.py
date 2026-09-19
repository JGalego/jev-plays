"""GBA Tactics: turn-based squad combat, driven entirely through menus and a cursor."""

from games.spec import Action, Game, Rom

GAME = Game(
    slug="gba_tactics",
    title="GBA Tactics",
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
        "You command a squad on a grid. Defeat every unit on the other side. Move the "
        "cursor over a unit, confirm to select it, and work through the menus."
    ),
    actions={
        "UP": Action(("UP",), "Move the cursor or menu selection up."),
        "DOWN": Action(("DOWN",), "Move the cursor or menu selection down."),
        "LEFT": Action(("LEFT",), "Move the cursor or menu selection left."),
        "RIGHT": Action(("RIGHT",), "Move the cursor or menu selection right."),
        "CONFIRM": Action(("A",), "Confirm the selection: pick a unit, a tile or a menu entry."),
        "CANCEL": Action(("B",), "Back out of the current selection or menu."),
        "START": Action(("START",), "Start the game from the title screen, or open the turn menu."),
        "WAIT": Action((), "Send no input and let the game run on."),
    },
    boot_frames=420,
)
