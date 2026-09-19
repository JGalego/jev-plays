"""Space Invaders: shuffle, shoot, and hide behind the bunkers."""

from games.spec import Game, Rom, pad

GAME = Game(
    slug="a2600_space_invaders",
    title="Space Invaders",
    machine="atari",
    rom=Rom(
        filename="space_invaders.bin",
        licence="Commercial (Atari) -- redistribution status unclear",
        provenance="shipped inside your own ale-py install",
        ale_id="space_invaders",
        note=(
            "A commercial Atari title. ale-py has shipped the ROMs inside its wheel since "
            "v0.9.0 without publishing any permission from the rights holders, so we treat "
            "its redistribution status as unclear: nothing here downloads or ships it. The "
            "runner reads the copy your own ale-py install already put on disk."
        ),
    ),
    objective=(
        "Rows of aliens descend towards you while you move along the bottom of the screen. "
        "Shoot them before they land, and use the bunkers for cover from their fire."
    ),
    actions=pad(
        LEFT="Move left.",
        RIGHT="Move right.",
        FIRE="Fire upwards.",
        LEFTFIRE="Move left and fire at the same time.",
        RIGHTFIRE="Move right and fire at the same time.",
        NOOP="Send no input for this step.",
    ),
    boot_frames=120,
)
