"""Pipes: lay pipe across a board from a tray of pieces. Unhurried, so latency is fine."""

from games.spec import Game, Rom, pad

GAME = Game(
    slug="a2600_pipes",
    title="Pipes",
    machine="atari",
    rom=Rom(
        filename="pipe2600.bin",
        licence="MIT",
        provenance="albf/pipes-2600 (Alexandre Luiz Brisighello Filho)",
        url="https://raw.githubusercontent.com/albf/pipes-2600/master/pipe2600.bin",
        sha256="5313fe8d2733d7d8e0ce5b53c4708552b8fb4daffe25fb5fb841cee350e7ff60",
    ),
    objective=(
        "A board you lay pipe across, with a tray of pieces along the bottom and a score "
        "at the foot of the screen. Move the cursor over the board and place pieces so "
        "they join into a connected run of pipe."
    ),
    actions=pad(
        UP="Move the cursor up the board.",
        DOWN="Move the cursor down the board.",
        LEFT="Move the cursor left, or step back through the tray of pieces.",
        RIGHT="Move the cursor right, or step forward through the tray of pieces.",
        FIRE="Press the button: place the selected piece where the cursor is.",
        UPFIRE="Push up with the button held.",
        DOWNFIRE="Push down with the button held.",
        NOOP="Send no input for this step.",
    ),
    boot_frames=400,
)
