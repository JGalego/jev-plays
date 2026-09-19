"""Write down what Jev did, and add it up at the end."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean

from jev.player import Decision


@dataclass
class RunLog:
    """A directory holding one run: decisions as JSONL, frames as PNGs, stats as JSON."""

    directory: Path
    game: str
    rom: str
    decisions: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        (self.directory / "frames").mkdir(parents=True, exist_ok=True)
        self._stream = (self.directory / "run.jsonl").open("w")

    def record(self, step: int, frame: int, observation: str, decision: Decision, buttons: tuple[str, ...]) -> None:
        """Append one Jev decision and the input it turned into."""

        entry = {
            "step": step,
            "frame": frame,
            "action": decision.action,
            "top_action": decision.top_action,
            "buttons": list(buttons),
            "hold_frames": decision.hold_frames,
            "confidence": round(decision.confidence, 4),
            "hold_confidence": round(decision.hold_confidence, 4),
            "latency_ms": round(decision.latency_ms, 1),
            "input_tokens": decision.input_tokens,
            "model": decision.model,
            "probabilities": {k: round(v, 4) for k, v in decision.probabilities.items()},
            "observation": observation,
        }
        self.decisions.append(entry)
        self._stream.write(json.dumps(entry) + "\n")
        self._stream.flush()

    def finish(self, frames_emulated: int) -> dict:
        """Close the log and write the run summary."""

        self._stream.close()
        stats = {
            "game": self.game,
            "rom": self.rom,
            "model": self.decisions[0]["model"] if self.decisions else None,
            "decisions": len(self.decisions),
            "frames_emulated": frames_emulated,
            "seconds_of_gameplay": round(frames_emulated / 59.7, 1),
            "actions": dict(Counter(d["action"] for d in self.decisions).most_common()),
            "mean_confidence": round(mean(d["confidence"] for d in self.decisions), 3) if self.decisions else None,
            "mean_latency_ms": round(mean(d["latency_ms"] for d in self.decisions), 1) if self.decisions else None,
            "total_input_tokens": sum(d["input_tokens"] or 0 for d in self.decisions),
            "drawn_below_top": sum(d["action"] != d["top_action"] for d in self.decisions),
        }
        (self.directory / "stats.json").write_text(json.dumps(stats, indent=2) + "\n")
        return stats
