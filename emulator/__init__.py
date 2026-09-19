"""Deliberately dumb emulator adapters. They press buttons and report what is on screen.

Each console has its own module -- `gba` needs mGBA, `atari` needs ale-py -- and neither
is imported here, so a machine whose emulator is not installed costs nothing.
"""
