# Humanoid Motion

Build animated GLBs from a humanoid rig and motion JSON. The exporter preserves the source geometry, skinning and textures and verifies the resulting animation.

## Requirements

- Python 3.12 or newer and [uv](https://docs.astral.sh/uv/).
- A humanoid rig in GLB format and a compatible motion JSON for each clip.
- An animated GLB and its source rig when exporting motion JSON.

## Setup

Run all commands from the repository root.

```bash
uv sync --locked --project tools/motion
```

## Usage

In [config.toml](../../assets/motion/config.toml), set the rig in `[inputs]`,
the output format in `[outputs]`, and the name, input JSON and output GLB for
each `[[animations]]` entry. TOML paths are relative to the configuration file.

The examples build [one clip](../../assets/motion/config.idle.toml), export it to
[motion JSON at 24 FPS](../../assets/motion/config.idle-export.toml), then
[validate the result](../../assets/motion/config.idle-validate.toml).

```bash
uv run --locked --project tools/motion motion build --config assets/motion/config.idle.toml
uv run --locked --project tools/motion motion export-json --config assets/motion/config.idle-export.toml
uv run --locked --project tools/motion motion validate --config assets/motion/config.idle-validate.toml
```

The build writes each `[[animations]]` entry to its configured destination.
A single-clip configuration can also declare `inputs.animation` and `outputs.glb`.
Motion JSON declares its schema version, coordinates, clip flags, ground
offset and translation arrays. Use empty arrays for clips without translated
joints.

## Development

```bash
uv run --locked --project tools/motion poe -C tools/motion format
uv run --locked --project tools/motion poe -C tools/motion check
```

## Build

Build the source distribution and wheel in `tools/motion/dist/`.

```bash
uv build tools/motion
```
