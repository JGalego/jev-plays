"""Bounstryk: a real-time bat-and-ball duel, and the hardest latency fit of the three."""

from games.spec import Game, Rom, pad

GAME = Game(
    slug="a2600_bounstryk",
    title="Bounstryk",
    machine="atari",
    rom=Rom(
        filename="bounstryk.bin",
        licence="Apache-2.0",
        provenance="egar-garcia/bounstryk release v1.0.0",
        url="https://github.com/egar-garcia/bounstryk/releases/download/v1.0.0/bounstryk.bin",
        sha256="2cb5d87d356748948631fc592431f503ea29ee1855d02777d5d2ff9ff3c5ba44",
    ),
    objective=(
        "A duel across a walled arena. You control one of the two bats facing each other "
        "and have to strike the ball past your opponent while keeping it off your own "
        "side. The score sits at the foot of the screen."
    ),
    actions=pad(
        UP="Move your bat up.",
        DOWN="Move your bat down.",
        LEFT="Move left.",
        RIGHT="Move right.",
        FIRE="Press the button: strike, or start the game from the title screen.",
        UPFIRE="Move up with the button held.",
        DOWNFIRE="Move down with the button held.",
        NOOP="Send no input for this step.",
    ),
    boot_frames=400,
)
