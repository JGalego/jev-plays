"""Run one Jev player: observe, ask Jev, press what it said, repeat."""

from __future__ import annotations

import argparse
import os
import random
import sys
from datetime import UTC, datetime
from pathlib import Path

import mgba.log
from dotenv import load_dotenv
from typesafe_sdk import TypeSafeClient

import games
from emulator import Emulator
from emulator.observe import Observer
from games import roms
from jev.player import choose_action
from jev.runlog import RunLog
from jev.viewer import compose, save_gif

ROOT = Path(__file__).resolve().parent.parent
# Three GIF frames per decision keeps the animation readable and the file small.
CAPTURES_PER_DECISION = 3
# Let the screen settle after a press so the next look is not taken mid-fade.
SETTLE_FRAMES = 8


def play(game: games.Game, rom: Path, steps: int, out: Path, rng: random.Random | None) -> dict:
    """Play one session and return its statistics."""

    emulator = Emulator(rom)
    emulator.run_frames(game.boot_frames)
    log = RunLog(directory=out, game=game.slug, rom=str(rom))
    observer = Observer(game)
    criteria = game.criteria()
    frames: list = []
    captured_frames: list[int] = []

    with TypeSafeClient(timeout=30) as client:
        for step in range(1, steps + 1):
            observation = observer.look(emulator)
            decision = choose_action(client, observation, criteria, rng)
            buttons = game.actions[decision.action].buttons
            observer.note(decision.action, buttons, decision.hold_frames)
            log.record(step, emulator.frame, observation, decision, buttons)
            print(
                f"  {step:3}/{steps}  {decision.action:<12} {'+'.join(buttons) or '-':<12}"
                f" {decision.confidence:>5.0%}{'*' if decision.sampled else ' '}"
                f" hold {decision.hold_frames:>2}f  {decision.latency_ms:>6.0f} ms"
            )

            panel = [
                f"{decision.action}  ->  {'+'.join(buttons) or 'no buttons'}",
                f"confidence {decision.confidence:.0%}, held for {decision.hold_frames} frames",
                f"{decision.model} answered in {decision.latency_ms:.0f} ms",
            ]
            # Capture through the press so the GIF shows the input taking effect.
            for chunk in range(CAPTURES_PER_DECISION):
                done = decision.hold_frames * chunk // CAPTURES_PER_DECISION
                held = decision.hold_frames * (chunk + 1) // CAPTURES_PER_DECISION - done
                emulator.press(buttons, held, release=0)
                captured_frames.append(held)
                frames.append(
                    compose(
                        emulator.screen(), f"JEV PLAYS {game.title.upper()}", f"step {step}/{steps}", observation, panel
                    )
                )
            emulator.run_frames(SETTLE_FRAMES)
            captured_frames[-1] += SETTLE_FRAMES
            emulator.screen().save(out / "frames" / f"{step:03}.png")

    save_gif(frames, captured_frames, out / "run.gif")
    return log.finish(emulator.frame)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Let Jev play a GBA game.")
    parser.add_argument("game", choices=games.SLUGS)
    parser.add_argument("--steps", type=int, default=30, help="how many decisions Jev makes")
    parser.add_argument("--rom", type=Path, help="override the ROM path for this run")
    parser.add_argument("--out", type=Path, help="where to write the run (default: runs/<game>-<time>)")
    parser.add_argument(
        "--argmax",
        action="store_true",
        help="always press Jev's most likely input instead of drawing from its distribution",
    )
    parser.add_argument("--seed", type=int, default=0, help="seed for the draw (default: 0)")
    args = parser.parse_args(argv)

    load_dotenv(ROOT / ".env")
    if not os.environ.get("TYPESAFE_API_KEY"):
        print("TYPESAFE_API_KEY is not set. Copy .env.example to .env and add your key.", file=sys.stderr)
        return 1

    mgba.log.silence()
    game = games.load(args.game)
    rom = args.rom or roms.resolve(game)
    if not rom.is_file():
        print(
            f"No ROM at {rom}.\n"
            f"  licence: {game.rom.licence}\n"
            f"  {game.rom.note or 'Run scripts/fetch_roms.py to download it.'}\n"
            f"  Or set {roms.env_var(game)} to your own copy.",
            file=sys.stderr,
        )
        return 1

    stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    out = args.out or ROOT / "runs" / f"{game.slug}-{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    print(f"{game.title} <- {rom.name}  ({args.steps} decisions) -> {out}")

    rng = None if args.argmax else random.Random(args.seed)
    stats = play(game, rom, args.steps, out, rng)
    print(
        f"\n  {stats['decisions']} decisions over {stats['seconds_of_gameplay']}s of play, "
        f"mean confidence {stats['mean_confidence']:.0%}, mean latency {stats['mean_latency_ms']:.0f} ms"
    )
    print(f"  {', '.join(f'{k} x{v}' for k, v in stats['actions'].items())}")
    if not args.argmax:
        print(f"  {stats['drawn_below_top']} of them were not Jev's most likely input (*)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
