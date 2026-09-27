# 倉庫審查（Windows-first）

- 審查日期：2026-08-28（第三輪：審查可修項落地，不回貢）
- overlay 落地：`62f720c3bdc54ed07aadbe726ef96bbcf8555ff7`
- 全庫覆核起點：`bd033e15d41a79ff9afa9fe288815eaacae7f87a`
- 上游 `reviewed_through`：`0351ece763f79c5d76f249533bce5e43562f3058`（commit 水位未推進）
- 上游 `reviewed_pr_through`：`4`（已讀 diff，略過）
- 主環境：Windows 11、PowerShell、Python 3.14、Node 26（overlay gate）
- 狀態：可繼續當 Windows 維護線。K-01 護欄、K-04、K-06 已在本 fork 落地。**不是**產品安全審計通過證明。本輪 **不回貢**。

## 結論

這個 fork 適合作為 Windows 本機、給 Agent 維護的 architecture-canvas 開發線。產品行為跟隨 `yulonghe97/draw-architecture`：`SKILL.md`、固定 viewer、scene 驗證／組裝、`npx draw-architecture` 安裝器。本線加上 overlay：頂部 fork 標示、Windows gate、產品 scene CI、`publish.yml` 官方閘門與 action pin、上游追蹤、CodeQL、Dependabot，以及已記錄的產品護欄（TITLE／KICKER escape、`</script>` 拒絕、CLI `--cursor`）。

根目錄 `README.md` 保持上游英文產品說明。npm 套件名仍是 `draw-architecture`，skill 目錄名是 `architecture-canvas`。本 fork **不發 npm**。`package.json` 的 `repository` 仍指向上游。

產生的 canvas 是單檔 HTML：scene 由本機 Agent 寫入 `<script>`，本 fork 拒絕含 `</script>` 的 scene，並 escape `TITLE`／`KICKER`。strapline 仍允許少量 HTML。讀出面板的 `about` 有 `escapeHtml`。會向 Google Fonts 要 JetBrains Mono。不要把輸出頁當成已消毒的受信任來源去嵌進第三方站。

不把 fork 當成第二個官方產品 repo。skills.sh、npm 與 live demo 仍屬上游。本線 **沒有**獨立後端。

本輪 **不回貢**。

## 本輪實證

### Git 與 remote（審查起點 `bd033e1`）

```text
git rev-parse HEAD
→ bd033e15d41a79ff9afa9fe288815eaacae7f87a

gh repo set-default --view
→ SanHsien/draw-architecture

origin   → https://github.com/SanHsien/draw-architecture.git
upstream → https://github.com/yulonghe97/draw-architecture.git

LICENSE → MIT（Copyright 2026 Yulong He）
package.json repository → git+https://github.com/yulonghe97/draw-architecture.git
engines.node → >=18；version → 0.1.0；runtime 依賴 → 無
git ls-files -s → 無 mode 120000
git ls-files .env* cookies.txt cookies.json credentials.json *.pem → 空
code-scanning alerts → 0
secret-scanning alerts → 0
```

`CLAUDE.md` 是一般檔。上游 `docs/*.png` 保留；fork 文件在 `docs/fork/`。

### GitHub Actions（overlay 落地 `62f720c`）

| Workflow | 結果 | URL |
|---|---|---|
| Validate scene | **success** | https://github.com/SanHsien/draw-architecture/actions/runs/33147004556 |
| Fork maintenance | **success** | https://github.com/SanHsien/draw-architecture/actions/runs/33147004623 |
| Upstream check | **success** | https://github.com/SanHsien/draw-architecture/actions/runs/33147004551 |
| CodeQL | **success**（0 open alerts） | https://github.com/SanHsien/draw-architecture/actions/runs/33147004550 |
| Dependency freshness | **success** | https://github.com/SanHsien/draw-architecture/actions/runs/33147004676 |

`bd033e1`（補 REVIEW CI URL）沒有重跑 fork-maintenance／validate（路徑過濾）。本輪修正會再跑一次。

### 本機 overlay gate（審查可修項落地後）

```text
pwsh -NoProfile -File tools\dev_check.ps1
→ node scripts/validate.js examples/shoply-scene.js
  5 bands · 20 boxes · 20 edges · 0 errors · 0 warnings
→ 39 passed、WINDOWS DEV CHECK GREEN
→ CLI --help 含 --cursor 與 ~\.cursor\skills
```

`examples/shoply-canvas.html` 與當下 `scripts/build.js` 重建結果位元組相同（Shoply 標題無特殊字元，escape 為恒等）。

**沒有**在瀏覽器裡重放 pinch／isolate／PNG，**沒有**對本機 `npx draw-architecture` 做真實安裝，**沒有**呼叫 artifact.cafe，**沒有**對上游開 PR。

### 產品面抽查（讀碼，不是滲透）

- `scripts/validate.js` 用 `new Function` 執行本機 `scene.js`。這是產品契約：scene 是 Agent 在本機寫的資料檔，不是遠端輸入。含 `</script>` 的 scene 在 evaluate 前就被拒絕。
- `scripts/build.js` 把 `{{SCENE}}` 注入 `assets/template.html` 的 `<script>` 區塊（同樣拒絕 `</script>`）。`{{SUB_HTML}}` 允許 strapline 裡的 `<b>`。`{{TITLE}}`／`{{KICKER}}` 做 HTML escape；`{{SLUG}}` 做 JS 單引號 escape。信任邊界仍是「誰能寫進產出目錄」。
- 讀出面板：`about` 走 `escapeHtml` 再放進 `innerHTML`。主題鈕的 `innerHTML` 是檔內寫死的 SUN／MOON SVG 常數。
- `bin/cli.js` 對無法識別為本 skill 的目錄拒絕覆寫（除非 `--force`）。非 TTY 且沒給 target 時，預設裝到 `~/.claude/skills/architecture-canvas`。本 fork 另提供 `--cursor` → `~/.cursor/skills`。Windows symlink 失敗會改 copy。
- 安裝 payload 不含 `evals/`、`LICENSE`、fork overlay。runtime 需要 `SKILL.md`、`assets/`、`scripts/`、`references/`。
- Overlay Python：`check_upstream_updates.py` 以 argv 列表呼叫 `git`；`check_dependency_freshness.py` 只對 `pypi.org` 做 `urlopen`。沒有 `os.system`、`shell=True`、`eval(`、`exec(`、`pickle`。

### 上游 open PR `#4`（已讀 diff）

[`yulonghe97/draw-architecture#4`](https://github.com/yulonghe97/draw-architecture/pull/4) `docs: improve README`，作者 `webbrain-one`，標註由本機 `qwen3.6-35b-a3b` 產生。

`gh pr diff 4` 只動 `README.md`（+3/−1）：開頭多兩行空行；把當時的 `Requirements: Node.js` 改成 `Node.js 18+`。PR 正文仍是舊結構（「A Claude skill…」），對不上目前 `main`（`7b99433` 已改成三路安裝）。本線 `engines.node` 已是 `>=18`。**略過、不 cherry-pick。** 沒有其他 open PR／獨立 open issue。

## 已修 findings

建置輪（overlay 落地）：

| ID | 嚴重度 | 項 | 處理 |
|---|---|---|---|
| R-01 | P1 | `publish.yml` 在本 fork 打 `v*` tag 會 `npm publish` | job 加官方-repo-only 閘門；checkout `persist-credentials: false` |
| R-02 | P2 | 無 Windows／文件 gate | `tools/dev_check.ps1`、`validate.yml`、`fork-maintenance.yml` |
| R-03 | P3 | Issue 會落到本 fork 當產品站 | `ISSUE_TEMPLATE/config.yml` 導向上游與本線 CONTRIBUTING |
| R-04 | P2 | `gh pr create` 預設打上游 | `.cursor/rules/no-upstream-pr.mdc` + `gh repo set-default` |

本輪審查修：

| ID | 嚴重度 | 項 | 處理 |
|---|---|---|---|
| R-05 | P3 | `.gitignore` 未點名 `*.pem` | 加上；測試鎖住 |
| R-06 | P2 | example HTML 與 template／scene 可能漂移而沒人發現 | `test_example_canvas_matches_fresh_build` 重建比對 |
| R-07 | P3 | overlay Python 沒有禁危險呼叫的測試 | 禁止 `os.system`／`shell=True`／`eval(`／`exec(`／`pickle` |
| R-08 | P3 | 連結檢查不掃 Cursor 規則 | `check_links.py` 納入 `no-upstream-pr.mdc` |
| R-09 | P3 | `fork-maintenance.yml` 不看 `.cursor/` | paths 加上 `.cursor/**` |
| R-10 | P2 | 上游 PR `#4` 建置時未讀 diff | 已讀；略過理由寫進 `docs/fork/DECISIONS.md`；`reviewed_pr_through: 4` |
| R-11 | P3 | `publish.yml` 浮動 `checkout@v6`／`setup-node@v6` 與 `npm@latest`（原 K-04） | pin SHA；`id-token` 收到 job；npm 釘 `12.0.2` |
| R-12 | P2 | TITLE／KICKER 未 escape、scene 可 `</script>` 破出（原 K-01 護欄） | build／validate 拒絕 `</script>`；TITLE／KICKER HTML escape；SLUG JS escape。不拿掉 `new Function`，不 escape strapline |
| R-13 | P3 | CLI 沒有 Cursor target（原 K-06） | `--cursor` → `~/.cursor/skills`；uninstall 預設也掃該路徑 |

## 已知、本輪不修

| ID | 嚴重度 | 項 | 理由 |
|---|---|---|---|
| K-01 | P2 | `validate.js` 仍用 `new Function` 執行 scene；`{{SUB_HTML}}` 仍允許 strapline HTML | 產品信任模型與 strapline 契約。護欄已擋 `</script>` 破出與標題注入 |
| K-02 | P3 | 產生 HTML 向 Google Fonts 發請求 | 上游 README 已聲明 |
| K-03 | P3 | 無瀏覽器 e2e（pinch／isolate／PNG） | overlay gate 不開 Playwright |
| K-05 | P3 | `package.json` 零 runtime 依賴、無 lockfile | 產品刻意為 npx 冷啟動 |
| K-07 | P3 | 安裝 payload 不含 `evals/` | evals 是 skill 開發用，不是 runtime |

## 已檢查、不列為 finding

- 產品現況：1 個 skill（`architecture-canvas`）、典範 scene Shoply 20 boxes／20 edges／5 bands，validate 0 error 0 warning。
- `publish.yml` 有 `github.repository == 'yulonghe97/draw-architecture'`；`validate.yml`／fork-maintenance／CodeQL **沒有**這道閘，本 fork 會跑。
- CodeQL workflow 綠燈且 open alerts = 0（`security-extended`，languages：actions／javascript-typescript／python）。
- Dependabot 不自動合併。
- 不對上游開 PR、不 push `upstream`。

## 使用邊界

- 給團隊的可留言連結走上游的 artifact.cafe 流程，本 fork 不代管。
- 安裝產品請用官方 `npx skills add yulonghe97/draw-architecture`，不要把本線 overlay 目錄整包丟進 skills。
