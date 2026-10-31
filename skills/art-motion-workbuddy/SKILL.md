---
name: art-motion-workbuddy
description: Plan and create editable motion-graphics videos from a user's topic and materials using the Art Motion WorkBuddy adapter. Use for storyboards and local whiteboard or other supported animation workflows; dependencies and any new visual assets must be available separately.
license: MIT
---

# Art Motion for WorkBuddy and Codex

Turn the user's idea into a storyboard and an editable local animation. Ask for or infer the topic, audience, length, aspect ratio, visual direction and sound from the current task. Do not substitute a sample for a finished user project. Honor the user's existing instructions and selected assets.

This small installable entry point prepares the full **v0.1.2** package when needed; it does not contain the rendering engine. The package is an adaptation of [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) and retains its license and attribution. Preparing it downloads approximately 17 MB from the public GitHub release, verifies its pinned SHA-256, and extracts it into a **new, caller-selected directory**. A previously downloaded matching ZIP can be supplied instead. The script refuses to overwrite an existing target.

## Prepare and make a project

Resolve the helper relative to this installed `SKILL.md`, not the current directory. Select a new absolute runtime path whose parent directory already exists, outside the installed skill, and a separate new project directory:

```sh
python3 /absolute/path/to/art-motion-workbuddy/scripts/prepare.py --target /absolute/path/to/new-runtime
```

To use an already downloaded `art-motion-workbuddy-v0.1.2.zip`, add `--archive /absolute/path/to/the.zip`. No credentials or model API are required for preparation. Use `python` where the host calls Python 3 that way.

Next read the prepared runtime's `SKILL.md`, then use its `scripts/local_engine.py doctor` and check the actual dependencies. For a first run, follow the repository's [whiteboard example](https://github.com/LydiaTools/art-motion-workbuddy#reproduce-the-whiteboard-example). Rendering requires Python, Playwright, a compatible browser and FFmpeg; other workflows can need additional packages or licensed assets. Configure the browser or FFmpeg path when the adapter cannot discover it. The local example has been tested on macOS; do not infer Windows or other styles have been tested.

Keep the editable project, source materials and requested output together. Distinguish a rendered clip from a reviewed final video; check the actual result and any requested audio. Do not publish or upload the user's material unless the user asks.

The v0.1.2 encoder-status guard is applied when initializing a new project. Existing copied engines are not updated automatically; check the project version. A successful render or nonempty file is not a playback or audio review.
