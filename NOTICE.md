# NOTICE

draw-architecture (SanHsien maintenance fork)
Copyright 2026 SanHsien

This project is derived from [`yulonghe97/draw-architecture`](https://github.com/yulonghe97/draw-architecture), licensed under the MIT License.

Original work:

- Project: draw-architecture / architecture-canvas
- Authors: Yulong He and contributors
- License: MIT
- Upstream: https://github.com/yulonghe97/draw-architecture

This repository keeps the MIT license text in [`LICENSE`](LICENSE). Modifications, documentation, and future project-specific changes in this fork are also licensed under MIT unless otherwise noted.

## License Notes

When redistributing this project or substantial parts of it:

- Keep [`LICENSE`](LICENSE) with the MIT text.
- Keep attribution to `yulonghe97/draw-architecture` and the original copyright holder.
- Add separate attribution for new third-party libraries when their licenses require it.

## Project Scope

This repository ships an agent skill that turns a system architecture into a single self-contained interactive HTML canvas: pan/zoom, click-to-isolate, dark/light switch, and 2× PNG export. The npm package name is `draw-architecture`; the skill name on disk is `architecture-canvas`. It is a maintenance fork, not a second official product site.

It does not include API keys, npm tokens, artifact.cafe credentials, or user-generated canvases. Do not commit `.env*` files or credentials.

## Credits

`draw-architecture` and `architecture-canvas` belong to the upstream project. The skill definition, viewer template, scene validator, builder, installer CLI, and Shoply example in this tree come from `yulonghe97/draw-architecture` unless a file in `docs/fork/` or the SanHsien overlay documents otherwise.

This project is not affiliated with, endorsed by, or sponsored by Anthropic, OpenAI, Google, GitHub, npm, Vercel, artifact.cafe, or any model vendor mentioned in examples.

Do not commit secrets, API keys, cookies, OAuth credentials, or account data.
