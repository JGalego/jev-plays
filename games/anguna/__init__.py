"""Anguna: a top-down action RPG. The simplest loop to validate -- move, hit things."""

from games.spec import Game, Rom, pad

GAME = Game(
    slug="anguna",
    title="Anguna",
    machine="gba",
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
    actions=pad(
        UP="Walk north; moves the cursor up in a menu.",
        DOWN="Walk south; moves the cursor down in a menu.",
        LEFT="Walk west; moves the cursor left in a menu.",
        RIGHT="Walk east; moves the cursor right in a menu.",
        A="Swing the sword; confirms the highlighted entry in a menu and advances dialogue.",
        B="Use the equipped second item; cancels in a menu.",
        R="Cycle to the next second item.",
        START="Open or close the pause and inventory screen; starts the game from the title.",
        NOTHING="Send no input for this step.",
    ),
    boot_frames=420,
)
