#!/usr/bin/env bash
# Build mGBA and its Python bindings into .mgba/ (gitignored).
# The bindings are not on PyPI, so they have to be compiled once against this venv.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PREFIX="$ROOT/.mgba"
SRC="$PREFIX/src"
BUILD="$SRC/build"
TAG="${MGBA_TAG:-0.10.5}"
# Pinned to the repo venv on purpose: an inherited VIRTUAL_ENV (conda, etc.)
# would link libmgba against the wrong libpython.
PY="${JEV_PLAYS_PYTHON:-$ROOT/.venv/bin/python}"

[ -x "$PY" ] || { echo "no venv python at $PY; run: uv venv --python 3.13 .venv" >&2; exit 1; }

if [ ! -d "$SRC" ]; then
  mkdir -p "$PREFIX"
  git clone --depth 1 --branch "$TAG" https://github.com/mgba-emu/mgba.git "$SRC"
fi

# Two small fixes, pinned to the tag above: the bindings reference e-reader symbols
# that only exist in an ffmpeg build, and setup.py pulls the long-dead pytest-runner.
git -C "$SRC" apply --reverse --check "$ROOT/scripts/mgba-$TAG-headless.patch" 2>/dev/null \
  || git -C "$SRC" apply "$ROOT/scripts/mgba-$TAG-headless.patch"

PYINC="$("$PY" -c 'import sysconfig; print(sysconfig.get_paths()["include"])')"
PYLIB="$("$PY" -c 'import sysconfig; print(sysconfig.get_config_var("LIBDIR") + "/" + sysconfig.get_config_var("LDLIBRARY"))')"

cmake -B "$BUILD" -S "$SRC" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_QT=OFF -DBUILD_SDL=OFF -DBUILD_PYTHON=ON \
  -DBUILD_SHARED=ON -DBUILD_STATIC=OFF \
  -DUSE_FFMPEG=OFF -DUSE_DISCORD_RPC=OFF -DUSE_LUA=OFF \
  -DPYTHON_EXECUTABLE="$PY" -DPYTHON_INCLUDE_DIR="$PYINC" -DPYTHON_LIBRARY="$PYLIB"

cmake --build "$BUILD" -j"$(nproc)"

# The extension links libmgba by RUNPATH into $BUILD, so just drop the package in place.
SITE="$("$PY" -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"
rm -rf "$SITE/mgba"
cp -r "$BUILD"/python/lib.*/mgba "$SITE/mgba"
"$PY" -c 'import mgba.core, mgba.gba; print("mgba bindings OK:", mgba.core.version if hasattr(mgba.core, "version") else "built")'
