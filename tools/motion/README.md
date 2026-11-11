# Humanoid Motion

_Convert a humanoid rig and motion JSON into a single animated GLB, preserving the source geometry, skinning and textures._

## Prerequisites

- Python 3.12+.
- [uv](https://docs.astral.sh/uv/) for dependencies and development commands.

## Development

### 1. Install dependencies

```bash
uv sync --locked --project tools/motion
```

### 2. Configure the inputs and output

Edit [`config.toml`](../../assets/motion/config.toml) with your rig, motion and destination paths.

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

### 5. Run tests

```bash
uv run --locked --project tools/motion poe -C tools/motion test
```

### 6. Build the package

```bash
uv build --project tools/motion
```
