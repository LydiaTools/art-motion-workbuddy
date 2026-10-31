# Art Motion for WorkBuddy

[中文介绍](#中文介绍) · [Download the skill package](https://github.com/LydiaTools/art-motion-workbuddy/releases/tag/v0.1.1)

Turn an idea into an editable motion-graphics project with WorkBuddy or Codex. This adaptation builds on the open-source [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) workflow, adding host-specific setup, storyboard and motion guidance, and an explicit FFmpeg path option.

![Six-second whiteboard animation: an idea, a discussion, and the next small step are drawn on screen](examples/research-whiteboard.gif)

An original, silent six-second example rendered locally with this package. The pen and diagrams are part of the animation. [View the editable example parameters](examples/research-whiteboard.json).

## What it does

- Plan shots and animate graphic elements for faceless videos.
- Build editable local projects and render video using the included engine.
- Check movement, visual continuity, audio and output before delivery.

## Get started

For a **Codex project**, install the small entry-point Skill with the optional third-party skills CLI (Node 22.20+):

```sh
npx skills@1.7.4 add LydiaTools/art-motion-workbuddy --skill art-motion-workbuddy --agent codex
```

When you first use it, the Skill prepares the complete v0.1.1 package in a new directory: approximately 17 MB downloaded from this repository's release, checked against a pinned SHA-256. You can supply an already downloaded matching ZIP instead. Installation of the entry point alone does not install the engine or its dependencies. The entry point is from current repository source; it is separate from the fixed v0.1.1 ZIP.

Or install the full package manually:

1. Download `art-motion-workbuddy-v0.1.1.zip` from the [release page](https://github.com/LydiaTools/art-motion-workbuddy/releases/tag/v0.1.1) and extract it.
2. Copy the entire `art-motion-workbuddy` folder into your WorkBuddy or Codex skills directory and refresh the skill list. Keep `SKILL.md`, `scripts/` and `upstream/` together.
3. Install Python, Playwright, Pillow, NumPy, a supported browser, FFmpeg and FFprobe. Run `python scripts/local_engine.py doctor` to check available dependencies.
4. Give your agent a topic and assets, and ask it to read the skill, plan shots, build and render a project, and review the result.

`COOPER_BROWSER` and `COOPER_FFMPEG` can specify executable paths. Complex shots may need custom scene code and revision; provide or properly license music, voice and visual assets. Dependency checks do not by themselves verify a full video production run.

Version 0.1.1 fixes the adapter's clip rendering: both engine pages receive a data-URL icon, so a missing favicon does not cause an otherwise completed clip to be reported as failed. The adapter also resolves `--spec` relative to the caller before it changes into the project directory. Voice guidance now follows the current user's project choices instead of prescribing one voice for everyone. The [adapter source](scripts/local_engine.py) is available to inspect; use the complete release package to run it. The earlier ZIP remains available in the repository.

## Reproduce the whiteboard example

After installing the dependencies, run these commands from the extracted skill folder. Choose a new project path; the adapter refuses to overwrite an existing `production` directory. On Windows, use `python` in place of `python3`.

```sh
python3 scripts/local_engine.py init --project ~/art-motion-demo
python3 scripts/local_engine.py render --project ~/art-motion-demo --out ~/art-motion-demo/whiteboard.mp4 --spec examples/research-whiteboard.json
```

The example is silent. On the tested Mac, `COOPER_BROWSER` was set to the Chrome executable; set it to your browser path if it is not detected. The sample tests a local whiteboard clip, not every animation style or platform.

## Credits and licensing

Based on [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion), commit `8a0d7d72ca65fcce6f8ba82c4a6c8dfe35b8422c`. The upstream code license and authorship are included in the package. The adaptation is under [MIT](LICENSE); the example uses the upstream engine and LXGW WenKai font, whose [OFL license](https://github.com/lxgw/LxgwWenKai/blob/main/OFL.txt) remains in the package. Upstream showcase characters, demonstration videos and selected images are excluded; they are not covered for reuse by the code's MIT license. Fonts and other third-party data retain their own licenses. Supply your own visual assets as needed.

## 中文介绍

这是一个面向 WorkBuddy 和 Codex 的艺术动效 Skill 适配包，用于将选题与素材制作成可编辑的动态图形视频工程。它补充了分镜、动作设计和交付检查，并支持指定本地 FFmpeg。

上方是用此 Skill 在本机渲染的原创 6 秒无声白板示例；笔和图形来自动画本身。[查看可编辑的示例参数](examples/research-whiteboard.json)。

安装依赖后，可在解压的 Skill 目录运行上方“Reproduce the whiteboard example”中的两条命令；Windows 将 `python3` 改为 `python`，需要时用 `COOPER_BROWSER` 指定浏览器路径。示例只验证了本机白板片段，不代表所有动画风格和平台均已验收。

**安装方式：**Codex 用户也可在项目里运行上方 `npx skills` 命令安装轻量入口；首次使用时需要从发行页下载约 17 MB 的完整资源并校验哈希，也可使用已下载的同版本 ZIP。入口本身不包含引擎或渲染依赖。或者从 [v0.1.1 发行页](https://github.com/LydiaTools/art-motion-workbuddy/releases/tag/v0.1.1)下载完整 Skill 压缩包，解压后将整个 `art-motion-workbuddy` 文件夹放入对应 Skill 目录，刷新技能列表。请保留包内完整目录，不要只复制 `SKILL.md`。本版修复了片段渲染时缺少图标导致的误报，并让 `--spec` 相对路径按命令执行目录解析；原压缩包仍保留在仓库中。

**运行条件：**需要 Python、Playwright、Pillow、NumPy、浏览器、FFmpeg 和 FFprobe，可先运行 `python scripts/local_engine.py doctor` 检查。具体镜头可能需要编写场景、调整节奏，音乐、配音和画面素材请自行提供或使用有权使用的资源。

**来源与许可：**基于花叔的开源项目，保留上游许可与署名；角色示范素材和展示视频未纳入本包，字体和第三方资源遵循各自许可。


## 不出镜知识讲解类视频

适用于把已核实的知识点整理成可编辑的讲解动画，例如用图形解释日常工作中的流程或概念。建议先提供主题、目标观众、讲解文案、画幅与时长，要求助手先给出分镜和画面动作，再生成并检查成片。

**提示词示例：**请读取本 Skill，围绕「咖啡为什么会逐渐变凉」制作一条不出镜知识讲解视频。先列出热量传递的关键事实并标明依据，再给出 30 秒分镜、每镜的画面动作与旁白建议；确认后制作可编辑工程，使用已授权的配音和配乐，检查文字、画面与声音后导出。镜头如需自定义代码，请说明并按实际环境执行。
