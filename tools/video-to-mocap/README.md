# Video to MoCap

Process synchronized multi-camera recordings with the FreeMoCap V2 post-hoc pipeline. Each animation produces native motion-capture data for separate retargeting to the game rig.

## Requirements

- Python 3.12 and [uv](https://docs.astral.sh/uv/).
- At least two synchronized videos per animation, with matching frame rates and frame counts.
- A FreeMoCap calibration TOML. Each recording must match its camera's calibration.

## Setup

Run all commands from the repository root. The lockfile pins the FreeMoCap V2 CPU dependency used by the batch processor.

```bash
uv sync --locked --project tools/video-to-mocap
```

## Usage

Use the [capture configuration](../../assets/motion/monster/animation/capture/config.toml) as a template. Set the calibration path, detector, RTMPose model, confidence threshold, output directory and named animations. TOML paths are relative to the configuration file.

List videos in calibration order. If a clip uses fewer cameras, its videos
correspond to the first calibrated cameras in that order. Set
`timeout_seconds`, `overwrite` and `continue_on_error` in `[processing]`.
To select a subset of clips, add a top-level `only = ["alert_1"]` above
`[capture]`.

```bash
uv run --locked --project tools/video-to-mocap freemocap-batch validate --config assets/motion/monster/animation/capture/config.toml
```

Choose a new output directory in your TOML before running `build` to produce
another set of captures:

```bash
uv run --locked --project tools/video-to-mocap freemocap-batch build --config assets/motion/monster/animation/capture/config.toml
```

## Development

```bash
uv run --locked --project tools/video-to-mocap poe -C tools/video-to-mocap format
uv run --locked --project tools/video-to-mocap poe -C tools/video-to-mocap check
```

## Build

```bash
uv build tools/video-to-mocap
```
