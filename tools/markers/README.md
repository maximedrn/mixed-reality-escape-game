# Spatial QR markers

_Generate vector QR markers, printable PDF sheets and a CSV mapping for spatial objects._

## Prerequisites

- Python 3.12+.
- [uv](https://docs.astral.sh/uv/) for dependencies and development commands.

## Development

Run all commands from the repository root. The tool supports Windows, macOS
and Linux.

### 1. Install dependencies

```bash
uv sync --locked --project tools/markers
```

### 2. Configure and generate markers

Edit [`config.standard.toml`](../../assets/markers/config.standard.toml) to define room/object
identifiers and label geometry, then generate the standard 30 mm markers:

```bash
uv run --locked --project tools/markers markers --config assets/markers/config.standard.toml
```

For 100 mm calibration markers on A4 pages:

```bash
uv run --locked --project tools/markers markers --config assets/markers/config.large.toml
```

### 3. Format and lint

```bash
uv run --locked --project tools/markers poe -C tools/markers format
uv run --locked --project tools/markers poe -C tools/markers check
```

### 4. Run tests

```bash
uv run --locked --project tools/markers poe -C tools/markers test
```

### 5. Build the package

```bash
uv build --project tools/markers
```
