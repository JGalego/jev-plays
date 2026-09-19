# Jev is a player!

[Jev](https://docs.typesafe.ai) picks the controller inputs for open-source Game Boy Advance games running in [mGBA](https://mgba.io). Nothing else decides anything: there is no policy, planner or heuristic in this repository. The emulator presses whatever Jev answers.

Jev is a System One model — it returns a typed choice, not text — so each frame is described to it as compact text and it answers with one button and how long to hold it.

## Quick start

```bash
uv venv --python 3.13 .venv          # 1. a virtualenv
uv pip install -e .                  # 2. the package
./scripts/build_mgba.sh              # 3. mGBA + its Python bindings (~3 min, not on PyPI)
./scripts/fetch_roms.py              # 4. the ROMs we may legally fetch
cp .env.example .env                 # 5. add your TYPESAFE_API_KEY
jev-plays anguna --steps 80
```

Each run writes `runs/<game>-<time>/` with `run.jsonl` (every decision), `stats.json`,
`frames/` and `run.gif`.

## How it works

```
GBA ROM ──► mGBA ──► observer ──► compact text ──► Jev ──► choice + hold ──► buttons ──► mGBA
            │        │                                     ▲                            │
         emulator/   emulator/observe.py                   │                            │
         gba.py      + games/<game>/ (optional decoder)   jev/player.py                 │
            └───────────────────────────────────────────────────────────────────────────┘
```

`emulator/` loads ROMs, holds buttons and reads back the framebuffer, OAM and memory.
`emulator/observe.py` turns that into text — a brightness grid at one character per 8×8
tile, dominant colours, how much moved, the enabled sprites, and what the last few
inputs did. It is strictly descriptive. `jev/` asks Jev and logs the answer. Each
`games/<game>/` supplies only the ROM's provenance, the objective, the pad vocabulary
Jev chooses from, and an optional game-specific decoder.

Adding a game: drop a `games/<slug>/__init__.py` with a `Game(...)`, add the slug to
`games/__init__.py`. That is the whole change.

## The players

The panel on the right of each GIF is the text Jev was given; the line under the screen
is what it answered.

| Game | Command | ROM | 80 decisions | How far Jev got |
|---|---|---|---|---|
| [Anguna](#anguna) | `jev-plays anguna` | fetched | 31% mean confidence, 328 ms | fighting in the dungeon |
| [GBA Tactics](#gba-tactics) | `jev-plays gba_tactics` | fetched | 28% mean confidence, 325 ms | moved a unit, opened its attack range |
| [Skyland](#skyland) | `jev-plays skyland` | fetched | 34% mean confidence, 310 ms | flew the sky map into zone 1 |
| [Solar Guard](#solar-guard) | `jev-plays solar_guard` | fetched | 33% mean confidence, 330 ms | launched a mission, flying it |
| Duster | `jev-plays duster` | you supply `DUSTER_ROM` | not run | — |
| NucularScience | `jev-plays nucular_science` | you supply `NUCULAR_SCIENCE_ROM` | not run | — |

The GIFs play emulated time at about 1.7× speed. The wait for Jev's answer is not shown.

### Anguna

![Jev plays Anguna](docs/anguna.gif)

Through the intro, into the dungeon, and fighting. 36 presses of A, 20 of start, 18 no
input, and a scattering of movement.

### GBA Tactics

![Jev plays GBA Tactics](docs/gba_tactics.gif)

Started a battle, selected a unit, moved it, and reached the attack menu — the action
list drops from `MOVE/ATTACK/END` to `ATTACK/END` once a unit has moved.

### Skyland

![Jev plays Skyland](docs/skyland.gif)

Out of the menus, onto the sky map, and through a zone-1 encounter before backing out to
the title again. Still the most cautious of the four: 43 of 80 decisions were no input.

### Solar Guard

![Jev plays Solar Guard](docs/solar_guard.gif)

Cleared the title, picked *Orbit Tidying* off the mission list, and flew it — the last
frames are the cockpit HUD with fuel, heat and radar.

## ROMs and licences

**No ROM is committed here.** RetroBrews states its collection is "approved for free
distribution on this site/project only", so that permission does not travel to this
repository. Each game was checked against its own upstream instead, and
`scripts/fetch_roms.py` downloads only the four with a licence that allows it.

| Game | Licence | Source |
|---|---|---|
| Anguna | Author grants free binary redistribution, with `anguna.txt` | [retrobrews/gba-games](https://github.com/retrobrews/gba-games) — Nathan Tolbert, 2008 |
| GBA Tactics | GPL-2.0-or-later | [retrobrews/gba-games](https://github.com/retrobrews/gba-games) — David Galvez Roca, 2006 |
| Skyland | MPL-2.0 | [evanbowman/skyland-gba](https://github.com/evanbowman/skyland-gba) release 2022.1.7.0 |
| Solar Guard | GPL-3.0-only | [Deft-Spade/Solar-Guard](https://github.com/Deft-Spade/Solar-Guard) release GBA-JAM-2021 |
| NucularScience | Zlib | [LiquidFenrir/NucularScience](https://github.com/LiquidFenrir/NucularScience) — source only, no published binary |
| Duster | **Unknown** | `bmchtech/duster`, later `redthing1/duster` — both removed from GitHub |

We fetch rather than bundle even where the licence would permit it: the copyleft ROMs
would oblige us to ship corresponding source we do not have. NucularScience has a
permissive licence but no published build, so build it with butano and devkitARM.
Duster's upstream is gone and no licence survives anywhere we could check, so its
redistribution status is unclear and it is neither fetched nor shipped. Both run from a
ROM you supply:

```bash
DUSTER_ROM=/path/to/Duster.gba jev-plays duster
```

## Why the input is drawn, not taken

Jev returns a probability over the buttons. Pressing its single most likely one gets
stuck: on Solar Guard's "Press START" screen, `START` averaged 17% and peaked at 25%, so
it never topped the distribution and was never pressed once in 80 decisions. More steps
cannot help when the argmax is stable.

So the input is drawn in proportion to Jev's own probabilities. The numbers are entirely
Jev's — there is no policy, ranking or veto on this side of the wire, and a draw is not a
decision-maker. `run.jsonl` records the full distribution and `top_action` for every
step, and the terminal marks a draw that differed from the top label with `*`.
`--argmax` restores the deterministic behaviour, `--seed` makes a draw reproducible.

## Notes

- Jev takes text only; there is no vision input, which is why the observer describes the
  frame rather than sending it.
- Buttons are named after the hardware (`A`, `START`, `UP`, `NOTHING`), not after game
  verbs. An earlier version called Solar Guard's A button `FIRE`, which read wrong on a
  menu screen; the description carries the meaning instead.
- Latency ran 240–900 ms per decision, so turn-based games fit the loop better than
  action games.
- mGBA is built from a pinned 0.10.5 checkout with `scripts/mgba-0.10.5-headless.patch`,
  which only guards e-reader symbols that exist solely in an ffmpeg build.

The code here is MIT (see `LICENSE`). mGBA is MPL-2.0. The games are under their own
licences, listed above.
