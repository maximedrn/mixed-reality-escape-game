# Tohannic: No Way Out

_A mixed-reality escape game on Meta Quest 3. The player explores a real-world location, interacts with virtual clues without controllers, and evades a monster animated using motion capture and controlled by artificial intelligence that navigates and pursues the player._

## Platform Compatibility

| Tool / Feature             | Windows | macOS  | Linux  |
|----------------------------|:-------:|:------:|:------:|
| **Unity 6.3 LTS**          |    ✅    |  ✅    |  ✅ ¹  |
| Unity Editor / Play Mode   |    ✅    |  ✅    |  ✅ ¹  |
| Android Build Support      |    ✅    |  ✅    |  ✅ ¹  |
| Meta Quest 3 Build (APK)   |    ✅    |  ✅    |  ✅ ¹  |
| OpenXR / Meta XR SDK       |    ✅    |  ✅    |  ✅ ¹  |
| Meta XR Simulator          |    ✅    |  ✅ ²  |  ❌    |
| Physical Quest 3 Testing   |    ✅    |  ✅    |  ✅ ¹  |
| **VS Code / C# Dev Kit**   |    ✅    |  ✅    |  ✅    |
| .NET SDK 10 / Roslyn       |    ✅    |  ✅    |  ✅    |
| CSharpier                  |    ✅    |  ✅    |  ✅    |
| CMake 3.20+                |    ✅    |  ✅    |  ✅    |
| uv / pre-commit            |    ✅    |  ✅    |  ✅    |
| Git / Git LFS              |    ✅    |  ✅    |  ✅    |
| Unity Test Framework       |    ✅    |  ✅    |  ✅ ¹  |
| **Blender**                |    ✅    |  ✅    |  ✅    |
| Python / Ruff              |    ✅    |  ✅    |  ✅    |

**Notes:**

1. **Linux:** Unity 6.3 officially supports Ubuntu 22.04/24.04 x64. Other distributions are not officially validated.
2. **macOS:** Meta XR Simulator requires Apple Silicon (M1 or newer).

## Prerequisites

Install the following tools before setting up the development environment.

### Required

- [Git](https://git-scm.com/downloads) — Version control.
- [Git LFS](https://git-lfs.com/) — Large asset management..
- [Unity Hub](https://unity.com/download) — Unity installation and project management.
- [Unity 6.3 LTS](https://unity.com/releases/lts) — Game engine.
- [.NET SDK 10](https://dotnet.microsoft.com/download/dotnet/10.0) — C# tooling, CSharpier and Roslyn.
- [CMake 3.20+](https://cmake.org/download/) — Cross-platform development task runner.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python tooling and pre-commit installation.

### Unity packages

The project uses the following packages, managed through Unity Package Manager:

- [OpenXR Plugin](https://docs.unity3d.com/Packages/com.unity.xr.openxr@latest) — XR runtime integration.
- [Meta XR SDK](https://developers.meta.com/horizon/develop/) — Quest 3 platform integration, passthrough and hand tracking.
- [Meta XR Interaction SDK](https://developers.meta.com/horizon/develop/) — Hand-based interactions.
- [Mixed Reality Utility Kit (MRUK)](https://developers.meta.com/horizon/develop/) — Scene understanding and room geometry.
- [AI Navigation](https://docs.unity3d.com/Packages/com.unity.ai.navigation@latest) — NavMesh navigation.
- [Unity Test Framework](https://docs.unity3d.com/Packages/com.unity.test-framework@latest) — EditMode and PlayMode testing.

### Development tools

- [Visual Studio Code](https://code.visualstudio.com/) with the [Unity extension](https://marketplace.visualstudio.com/items?itemName=VisualStudioToolsForUnity.vstuc) — Recommended IDE.
- [CSharpier](https://csharpier.com/docs/Installation) — C# formatter, installed through the project's .NET tool manifest.
- [Roslyn / dotnet format](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format) — C# static analysis and code-style checks.
- [pre-commit](https://pre-commit.com/) — Automatic formatting and validation before Git commits.

### Optional tools

- [Meta XR Simulator](https://developers.meta.com/horizon/develop/) — Standalone XR simulation for supported Windows and Apple Silicon macOS environments.
- [Android Debug Bridge (ADB)](https://developer.android.com/tools/adb) — Quest 3 debugging and APK deployment. Included with the Unity Android SDK.
- [Blender](https://www.blender.org/download/) — 3D modeling, rigging and animation.
- [FreeMoCap](https://freemocap.org/) — Markerless motion capture.

## Development

All commands are executed from the repository root using a Bash-compatible terminal (Bash, Zsh or Git Bash on Windows).

### 1. Clone the repository

```bash
git clone https://github.com/maximedrn/mixed-reality-escape-game.git
cd mixed-reality-escape-game

git lfs install
git lfs pull
```

### 2. Install development tools

Restore the project-local .NET tools, including CSharpier:

```bash
cmake -DTASK=setup -P cmake/Tasks.cmake
```

Install and configure pre-commit:

```bash
uv tool install pre-commit
pre-commit install
```

### 3. Configure Unity

1. Open **Unity Hub**.
2. Add the existing project located in `Unity/`.
3. Open it with the Unity version specified in `Unity/ProjectSettings/ProjectVersion.txt`.
4. Wait for Unity to import assets and resolve packages.
5. Open **File > Build Profiles** and activate the **Meta Quest** build profile.
6. Verify that OpenXR, Meta Quest and Meta XR feature groups are enabled for Android.
7. Open **Preferences > External Tools**, select your preferred IDE and click **Regenerate project files**.

### 4. Format and lint

Code quality is managed through CMake and is independent of the IDE.

```bash
# Format all project C# files.
cmake -DTASK=format -P cmake/Tasks.cmake

# Check formatting without modifying files.
cmake -DTASK=check-format -P cmake/Tasks.cmake

# Run Roslyn code-style and analyzer checks.
cmake -DTASK=lint -P cmake/Tasks.cmake

# Run all C# checks.
cmake -DTASK=check -P cmake/Tasks.cmake

# Enable detailed diagnostic output.
cmake -DTASK=lint -DVERBOSE=ON -P cmake/Tasks.cmake

# Install the motion processing environment and Python dependencies.
cmake -DTASK=motion-setup -P cmake/Tasks.cmake

# Validate motion Python code (formatting, lint and types).
cmake -DTASK=motion-check -P cmake/Tasks.cmake

# Test the shared Python rules and scan every Python project in the repository.
cmake -DTASK=python-lint -P cmake/Tasks.cmake
```

### 5. Run tests

Open Unity and navigate to: **Window > General > Test Runner**

Run the available test suites:

- **EditMode** — Unit tests for game logic, puzzle progression and monster behavior.
- **PlayMode** — Runtime tests for interactions, navigation and scene behavior.

### 6. Pre-commit hooks

The pre-commit hooks automatically run:

```bash
cmake -DTASK=format -P cmake/Tasks.cmake
cmake -DTASK=check -P cmake/Tasks.cmake
```

To execute all hooks manually:

```bash
pre-commit run --all-files
```

Hooks run automatically before each commit.

### 7. Commit changes

Before committing, format and validate the project:

```bash
cmake -DTASK=format -P cmake/Tasks.cmake
cmake -DTASK=check -P cmake/Tasks.cmake

git add -A
# See: https://www.conventionalcommits.org/en/v1.0.0/
git commit -m "<type>[optional scope]: <description>"
```

### 8. Build and run

Unity handles the application build; CMake is used only for development tooling.

To deploy to Meta Quest 3:

1. Connect the headset and enable developer mode.
2. Open **File > Build Profiles** in Unity.
3. Select the **Meta Quest** profile.
4. Use **Build and Run**.
