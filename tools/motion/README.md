# Humanoid Motion

_Convert a humanoid rig and motion JSON files into animated GLBs, preserving the source geometry, skinning and textures._

## Prerequisites

- Python 3.12+.
- [uv](https://docs.astral.sh/uv/) for dependencies and development commands.

## Development

### 1. Install dependencies

```bash
uv sync --locked --project tools/motion
```

### 2. Configure the inputs and output

Edit [`config.toml`](../../assets/motion/config.toml): `[inputs]` defines the rig and optional joint constraints, `[outputs]` selects `format = "glb"`, and each `[[animations]]` entry defines a `name`, JSON `input` and GLB `output`. Paths are relative to this file.

Motion JSON version 2 includes local translations (`translation_bone_names`, `translations_xyz`) alongside rotations. Version 1 remains readable; `export-json` writes version 2.

### 3. Export the animated GLB

```bash
uv run --locked --project tools/motion motion build --config assets/motion/config.toml
```

List available commands with:

```bash
uv run --locked --project tools/motion motion --help
```

### 4. Format and lint

```bash
uv run --locked --project tools/motion poe -C tools/motion format
uv run --locked --project tools/motion poe -C tools/motion check
```

### 5. Build the package

```bash
uv build --project tools/motion
```
