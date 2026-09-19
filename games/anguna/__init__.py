"""Anguna: a top-down action RPG. The simplest loop to validate -- move, hit things."""

from games.spec import Action, Game, Rom

GAME = Game(
    slug="anguna",
    title="Anguna",
    rom=Rom(
        filename="anguna.gba",
        licence="Free binary redistribution granted by the author",
        provenance="retrobrews/gba-games (Nathan Tolbert, 2008)",
        url="https://raw.githubusercontent.com/retrobrews/gba-games/master/anguna.gba",
        sha256="cd3b969d5ed6b38b2039c11b894d6db2fc3fad209a7fd046bee241cc66069851",
        companions=(("anguna.txt", "https://raw.githubusercontent.com/retrobrews/gba-games/master/anguna.txt"),),
        note="anguna.txt carries the author's terms and must travel with the ROM.",
    ),
    objective=(
        "You are a hero exploring a dungeon from above. Get off the title screen, then "
        "explore new rooms, attack the monsters you meet and stay alive."
    ),
    actions={
        "UP": Action(("UP",), "Walk north, or move the cursor up a menu."),
        "DOWN": Action(("DOWN",), "Walk south, or move the cursor down a menu."),
        "LEFT": Action(("LEFT",), "Walk west, or move the cursor left."),
        "RIGHT": Action(("RIGHT",), "Walk east, or move the cursor right."),
        "ATTACK": Action(("A",), "Swing the sword, or confirm the highlighted menu entry."),
        "ITEM": Action(("B",), "Use the equipped second item, or cancel."),
        "SWITCH_ITEM": Action(("R",), "Cycle to the next second item."),
        "MENU": Action(("START",), "Open or close the pause and inventory screen."),
        "WAIT": Action((), "Send no input and let the game run on."),
    },
    boot_frames=420,
)
