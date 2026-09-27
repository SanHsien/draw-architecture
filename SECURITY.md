# 安全政策

> **SanHsien 維護型 fork。** 產品漏洞（viewer 模板、scene 注入、安裝器覆寫、npm publish）請回報上游 [`yulonghe97/draw-architecture`](https://github.com/yulonghe97/draw-architecture/security/advisories/new)；若該入口不可用，改開上游 private contact，不要先建立公開 Issue。本 fork overlay（`tools/`、`docs/fork/`、workflow）開 [`SanHsien/draw-architecture`](https://github.com/SanHsien/draw-architecture/security/advisories/new) 的 Security tab。維護規則見 [`FORK.md`](FORK.md)。

## 支援範圍

安全修正以本 fork 的最新 `main` 為主；上游版本的問題也會視需要回報原作者。本線不承擔官方 SLA。

## 私下回報

請使用 GitHub Security Advisories 的 **Report a vulnerability** 私下回報。不要先建立公開 Issue。

回報請包含影響範圍、重現步驟、受影響版本與最小必要證據。請勿附上真實 API key、npm token、cookie 或帳號資料。

## 特別注意

- `scripts/build.js` 把 `scene.js` 注入 `assets/template.html` 的 `{{SCENE}}` 區塊。本 fork 會拒絕含 `</script>` 的 scene，並對 `TITLE`／`KICKER` 做 HTML escape。`{{SUB_HTML}}` 仍允許 strapline 裡的少量 HTML。scene 是由宿主 Agent 撰寫的本機資料，不是遠端 HTML。不要把產生的 canvas 當成已消毒的受信任來源去嵌入第三方站點。
- `bin/cli.js` 預設拒絕覆寫無法識別為本 skill 的目錄；`--force` 會覆寫。不要在自動化裡對未知路徑開 `--force`。本 fork 另提供 `--cursor` 裝到 `~/.cursor/skills`。
- 產生的 HTML 會向 Google Fonts 要 JetBrains Mono。離線／鎖網環境請自行改模板或接受系統字體回退。
- 本 fork 不代管 artifact.cafe、不發 npm。官方套件仍屬上游 `draw-architecture`。
