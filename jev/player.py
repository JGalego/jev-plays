"""Ask Jev what to press.

Jev is the only thing in this repository that decides anything. It is handed a text
description of the screen and the list of inputs the pad can send, and it answers with
one of them plus how long to hold it. Nothing here re-ranks, overrides or second-guesses
that answer; the caller presses whatever comes back.
"""

from __future__ import annotations

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
    confidence: float
    hold_frames: int
    hold_confidence: float
    probabilities: Mapping[str, float]
    model: str
    latency_ms: float
    input_tokens: int | None


def choose_action(client: TypeSafeClient, observation: str, actions: Mapping[str, str]) -> Decision:
    """Send one observation to Jev and return the input it picked."""

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
    action = response.choices["action"]
    hold = response.scores["hold"]
    level = max(0, min(round(hold.score), len(HOLD_FRAMES) - 1))
    return Decision(
        action=action.choice,
        confidence=action.confidence,
        hold_frames=HOLD_FRAMES[level],
        hold_confidence=hold.confidence,
        probabilities=dict(action.probabilities),
        model=response.model,
        latency_ms=latency_ms,
        input_tokens=response.usage.input_tokens,
    )
