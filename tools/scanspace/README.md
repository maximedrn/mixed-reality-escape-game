# ScanSpace Architecture Cleaner

_Keep the original wall, floor and door meshes from a ScanSpace floorplan GLB and fill window openings using the transforms in its `.scanspace` archive._

## Requirements

- Python 3.12+ and [uv](https://docs.astral.sh/uv/).
- The original ScanSpace floorplan `.glb` and its matching `.scanspace` archive.

## Setup

From the root of the game repository:

```bash
uv sync --project tools/scanspace
```

## Usage

```bash
uv run --project tools/scanspace scanspace clean \
  --input assets/scanspace/room.glb \
  --scan assets/scanspace/room.scanspace \
  --output assets/scanspace/room-cleaned.glb
```

Or from this directory:

```bash
uv run scanspace clean --input room.glb --scan room.scanspace --output room-cleaned.glb
```

## Development

```bash
uv run --project tools/scanspace poe -C tools/scanspace format
uv run --project tools/scanspace poe -C tools/scanspace check
```
