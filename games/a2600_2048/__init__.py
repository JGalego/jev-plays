"""2048 on the 2600: turn-based, four inputs, and no clock. The best fit for Jev here."""

from games.spec import Game, Rom, pad

GAME = Game(
    slug="a2600_2048",
    title="2048",
    machine="atari",
    rom=Rom(
        filename="2048.bin",
        licence="MIT",
        provenance="chesterbr/2048-2600 (Carlos Duarte do Nascimento)",
        url="https://raw.githubusercontent.com/chesterbr/2048-2600/main/2048.bin",
        sha256="c85dc2204299b0a29209d3f80ae112678c171dab216719593625647d2436f1e1",
    ),
    objective=(
        "A 4x4 grid of numbered tiles. Push the whole grid one way and equal tiles that "
        "collide merge into their sum. Keep merging to build a 2048 tile; the game ends "
        "when the grid fills up with nothing left to merge."
    ),
    actions=pad(
        UP="Push every tile up.",
        DOWN="Push every tile down.",
        LEFT="Push every tile left.",
        RIGHT="Push every tile right.",
        FIRE="Press the button: starts a new game from the title or game-over screen.",
        NOOP="Send no input for this step.",
    ),
    boot_frames=400,
)
