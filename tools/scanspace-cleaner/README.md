# ScanSpace Cleaner

Keep the walls, floor and doors from a ScanSpace GLB and fill window openings using the matching room metadata.

## Requirements

- Python 3.12 or newer and [uv](https://docs.astral.sh/uv/).
- A ScanSpace floorplan GLB and its matching `.scanspace` archive.

## Setup

Run all commands from the repository root.

```bash
uv sync --locked --project tools/scanspace-cleaner
```

## Usage

In [config.toml](../../assets/scanspace/config.toml), set both input paths, the output GLB path and the patch dimensions in metres. `window_overlap_m` adds to the width and height of each opening. `window_depth_m` sets the patch thickness.

```bash
uv run --locked --project tools/scanspace-cleaner scanspace clean --config assets/scanspace/config.toml
```

## Development

```bash
uv run --locked --project tools/scanspace-cleaner poe -C tools/scanspace-cleaner format
uv run --locked --project tools/scanspace-cleaner poe -C tools/scanspace-cleaner check
```

## Build

```bash
uv build tools/scanspace-cleaner
```
