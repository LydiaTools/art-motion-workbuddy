# Art Motion for WorkBuddy

[中文介绍](#中文介绍) · [Download the skill package](./art-motion-workbuddy-公开候选-v2.zip)

Turn an idea into an editable motion-graphics project with WorkBuddy or Codex. This adaptation builds on the open-source [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) workflow, adding host-specific setup, storyboard and motion guidance, and an explicit FFmpeg path option.

## What it does

- Plan shots and animate graphic elements for faceless videos.
- Build editable local projects and render video using the included engine.
- Check movement, visual continuity, audio and output before delivery.

## Get started

1. Download the [complete ZIP package](./art-motion-workbuddy-公开候选-v2.zip) and extract it.
2. Copy the entire `art-motion-workbuddy` folder into your WorkBuddy or Codex skills directory and refresh the skill list. Keep `SKILL.md`, `scripts/` and `upstream/` together.
3. Install Python, Playwright, Pillow, NumPy, a supported browser, FFmpeg and FFprobe. Run `python scripts/local_engine.py doctor` to check available dependencies.
4. Give your agent a topic and assets, and ask it to read the skill, plan shots, build and render a project, and review the result.

`COOPER_BROWSER` and `COOPER_FFMPEG` can specify executable paths. Complex shots may need custom scene code and revision; provide or properly license music, voice and visual assets. Dependency checks do not by themselves verify a full video production run.

## Credits and licensing

Based on [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion), commit `8a0d7d72ca65fcce6f8ba82c4a6c8dfe35b8422c`. The upstream code license is included in the package. Upstream showcase characters, demonstration videos and selected images are excluded; they are not covered for reuse by the code's MIT license. Fonts and other third-party data retain their own licenses. Supply your own visual assets as needed.

## 中文介绍

这是一个面向 WorkBuddy 和 Codex 的艺术动效 Skill 适配包，用于将选题与素材制作成可编辑的动态图形视频工程。它补充了分镜、动作设计和交付检查，并支持指定本地 FFmpeg。

**安装方式：**下载[完整 Skill 压缩包](./art-motion-workbuddy-公开候选-v2.zip)，解压后将整个 `art-motion-workbuddy` 文件夹放入对应 Skill 目录，刷新技能列表。请保留包内完整目录，不要只复制 `SKILL.md`。

**运行条件：**需要 Python、Playwright、Pillow、NumPy、浏览器、FFmpeg 和 FFprobe，可先运行 `python scripts/local_engine.py doctor` 检查。具体镜头可能需要编写场景、调整节奏，音乐、配音和画面素材请自行提供或使用有权使用的资源。

**来源与许可：**基于花叔的开源项目，保留上游许可与署名；角色示范素材和展示视频未纳入本包，字体和第三方资源遵循各自许可。
