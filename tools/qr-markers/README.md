# QR Markers

Generate vector QR markers, printable PDF label sheets and a CSV manifest for the game's rooms and physical objects.

## Requirements

- Python 3.12 or newer and [uv](https://docs.astral.sh/uv/).
- A TOML file defining the game, rooms, objects, label layout and export settings.

## Setup

Run all commands from the repository root.

```bash
uv sync --locked --project tools/qr-markers
```

## Usage

Use [config.standard.toml](../../assets/markers/config.standard.toml) for 30 mm Avery labels and [config.large.toml](../../assets/markers/config.large.toml) for 100 mm calibration markers on A4 sheets.

Set the export path in `[output]` and the label layout in `[labels]`. Use
`[labels.grid]` to set the grid dimensions for `a4_grid` or `[labels.custom]`
for a measured sheet. Relative output paths are resolved from the TOML file.

```bash
uv run --locked --project tools/qr-markers markers --config assets/markers/config.standard.toml
uv run --locked --project tools/qr-markers markers --config assets/markers/config.large.toml
```

## Development

```bash
uv run --locked --project tools/qr-markers poe -C tools/qr-markers format
uv run --locked --project tools/qr-markers poe -C tools/qr-markers check
```

## Build

```bash
uv build tools/qr-markers
```
