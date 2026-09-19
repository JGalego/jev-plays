"""Freeway: three inputs and traffic that punishes hesitation. The cleanest ALE test."""

from games.spec import Game, Rom, pad

GAME = Game(
    slug="a2600_freeway",
    title="Freeway",
    machine="atari",
    rom=Rom(
        filename="freeway.bin",
        licence="Commercial (Activision, 1981) -- redistribution status unclear",
        provenance="shipped inside your own ale-py install",
        ale_id="freeway",
        note=(
            "A commercial Atari title. ale-py has shipped the ROMs inside its wheel since "
            "v0.9.0 without publishing any permission from the rights holders, so we treat "
            "its redistribution status as unclear: nothing here downloads or ships it. The "
            "runner reads the copy your own ale-py install already put on disk."
        ),
    ),
    objective=(
        "You are a chicken at the bottom of a ten-lane highway. Walk up to the top without "
        "being hit; traffic knocks you back down the screen. Every crossing scores a point."
    ),
    actions=pad(
        UP="Walk up, towards the far side of the road.",
        DOWN="Walk back down.",
        NOOP="Stand still and let the traffic pass.",
    ),
    boot_frames=120,
)
