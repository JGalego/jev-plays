"""Pong: the original. Two bats, one ball, and nowhere for a slow decision to hide."""

from games.spec import Game, Rom, pad

GAME = Game(
    slug="a2600_pong",
    title="Pong",
    machine="atari",
    rom=Rom(
        filename="pong.bin",
        licence="Commercial (Atari) -- redistribution status unclear",
        provenance="shipped inside your own ale-py install",
        ale_id="pong",
        note=(
            "A commercial Atari title. ale-py has shipped the ROMs inside its wheel since "
            "v0.9.0 without publishing any permission from the rights holders, so we treat "
            "its redistribution status as unclear: nothing here downloads or ships it. The "
            "runner reads the copy your own ale-py install already put on disk."
        ),
    ),
    objective=(
        "You control the bat on the right, the console controls the one on the left. "
        "Move up and down to keep the ball in play and send it past your opponent. "
        "The score sits along the top."
    ),
    actions=pad(
        RIGHT="Move your bat up.",
        LEFT="Move your bat down.",
        FIRE="Press the button: serves the ball.",
        NOOP="Send no input for this step.",
    ),
    boot_frames=120,
)
