"""Ask Jev what to press.

Jev is the only thing in this repository that decides anything. It is handed a text
description of the screen and the list of inputs the pad can send, and it answers with a
probability over those inputs plus how long to hold one. Nothing here re-ranks, vetoes or
second-guesses that answer.

By default the input is drawn from Jev's own distribution rather than taken from its top
label. Jev's probabilities are calibrated, and always pressing the argmax turns a stable
screen into a stuck run: a button Jev gives 20% to is never pressed, however long the
session. Sampling still uses only Jev's numbers -- there is no policy on this side of the
wire -- and `--argmax` restores the deterministic behaviour.
"""

from __future__ import annotations

import random
import time
from collections.abc import Mapping
from dataclasses import dataclass

from typesafe_sdk import Choice, Score, TypeSafeClient

# Jev scores the press length against this rubric; the index maps straight to frames.
HOLD_RUBRIC = (
    "a tap, the shortest press the pad can send",
    "a short press",
    "a long press",
    "a very long press, held down for about a second",
)
HOLD_FRAMES = (4, 10, 24, 56)

INSTRUCTIONS = (
    "You are playing a Game Boy Advance game. The state is a description of what is on "
    "screen right now. Choose the single controller input to send next."
)


@dataclass(frozen=True, slots=True)
class Decision:
    """One answer from Jev, with the numbers needed to log the run."""

    action: str
    top_action: str
    confidence: float
    hold_frames: int
    hold_confidence: float
    probabilities: Mapping[str, float]
    model: str
    latency_ms: float
    input_tokens: int | None

    @property
    def sampled(self) -> bool:
        """True when the drawn input was not Jev's most likely one."""

        return self.action != self.top_action


def _draw(probabilities: Mapping[str, float], rng: random.Random):
    """Draw one key in proportion to Jev's probabilities."""

    ranked = sorted(probabilities.items(), key=lambda item: (-item[1], str(item[0])))
    keys = [key for key, _ in ranked]
    weights = [max(0.0, value) for _, value in ranked]
    return rng.choices(keys, weights=weights, k=1)[0] if sum(weights) > 0 else keys[0]


def choose_action(
    client: TypeSafeClient,
    observation: str,
    actions: Mapping[str, str],
    rng: random.Random | None = None,
) -> Decision:
    """Send one observation to Jev and return the input it picked.

    Pass `rng` to draw from Jev's distribution, or None to always take its top label.
    """

    started = time.perf_counter()
    response = client.system_one(
        state=observation,
        questions={
            "action": Choice(instructions=INSTRUCTIONS, criteria=dict(actions)),
            "hold": Score(
                instructions="How long should that input be held down?",
                criteria=list(HOLD_RUBRIC),
            ),
        },
    )
    latency_ms = (time.perf_counter() - started) * 1000
    answer = response.choices["action"]
    hold = response.scores["hold"]
    # Without an rng we take Jev's own answer verbatim, not our own argmax of it.
    chosen = answer.choice if rng is None else _draw(answer.probabilities, rng)
    level = round(hold.score) if rng is None else _draw(hold.probabilities, rng)
    return Decision(
        action=chosen,
        top_action=answer.choice,
        confidence=answer.probabilities.get(chosen, 0.0),
        hold_frames=HOLD_FRAMES[max(0, min(int(level), len(HOLD_FRAMES) - 1))],
        hold_confidence=hold.confidence,
        probabilities=dict(answer.probabilities),
        model=response.model,
        latency_ms=latency_ms,
        input_tokens=response.usage.input_tokens,
    )
