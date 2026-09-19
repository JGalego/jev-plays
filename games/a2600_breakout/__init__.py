"""Breakout: a bat, a ball and a wall. Four inputs, which makes the choice very legible."""

from games.spec import Game, Rom, pad

GAME = Game(
    slug="a2600_breakout",
    title="Breakout",
    machine="atari",
    rom=Rom(
        filename="breakout.bin",
        licence="Commercial (Atari, 1978) -- redistribution status unclear",
        provenance="shipped inside your own ale-py install",
        ale_id="breakout",
        note=(
            "A commercial Atari title. ale-py has shipped the ROMs inside its wheel since "
            "v0.9.0 without publishing any permission from the rights holders, so we treat "
            "its redistribution status as unclear: nothing here downloads or ships it. The "
            "runner reads the copy your own ale-py install already put on disk."
        ),
    ),
    objective=(
        "A wall of bricks across the top, a bat you slide along the bottom, and a ball. "
        "Press the button to serve, then keep the bat under the ball so it rebounds and "
        "knocks out bricks. You lose a turn every time the ball gets past you."
    ),
    actions=pad(
        LEFT="Slide the bat left.",
        RIGHT="Slide the bat right.",
        FIRE="Press the button: serves the ball at the start of a turn.",
        NOOP="Send no input for this step.",
    ),
    boot_frames=120,
)
