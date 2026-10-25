# 維護決策

## 2026-08-28：建立 Windows-first 維護型 fork

**決定**：fork `yulonghe97/draw-architecture`，保留 MIT 與完整歷史，預設分支維持 `main`。本線聚焦 Windows 開發 gate、fork overlay 文件、example scene 驗證，以及逐筆審查的上游追蹤。根目錄 `README.md` 保持上游英文。

**理由**：上游已經是可跑的 architecture-canvas skill（固定 viewer、scene 驗證、npm 安裝器）。缺的是 Windows 11 上可重現的 overlay 驗收骨架，以及「PR 只打本 fork、不要從 fork 發 npm」的硬邊界。直接用上游 repo 難以長期記錄 fork 取捨。上游 `docs/` 已放產品截圖，維護文件必須進 `docs/fork/`。

**限制**：

- 不把 fork 包裝成原創專案，不移除原作者與 MIT 標示。
- 不把產品 Skill、scene 或 example 翻譯成繁體；產品語言跟隨上游。
- 不改 `package.json` 的 npm 套件身分。
- 上游更新必須逐筆審查。
- 不回貢，除非維護者在當次對話明確同意。

## 2026-08-28：維護線直接推 main

**決定**：fork 維護不再開功能分支。改完在本機跑 gate，通過後直接推 `origin/main`。遠端只留 `main`；`upstream/main` 只追蹤。

**理由**：這是單人維護 fork，分支與 PR 沒有第二審查者，只增加同步成本。

**限制**：

- Dependabot 與外部 fork 仍可能開 PR，讀 diff 後再合併，不自動合併。
- 不推 `upstream`，不 force-push `main`。
- 不刪 `upstream` remote。

## 2026-08-28：publish.yml 加官方-repo-only 閘門

**決定**：在上游 `publish.yml` 的 job 加上 `if: github.repository == 'yulonghe97/draw-architecture'`，checkout 加 `persist-credentials: false`。不改 workflow 檔名、不改 npm OIDC 步驟。當時不 pin 產品 action 版本。

**後續**：同日審查可修項落地已 pin checkout／setup-node SHA、把 `id-token: write` 收到 job，並釘 `npm@12.0.2`。見下方「審查可修項在本 fork 落地」。

**理由**：workflow 檔名是 npm trusted publisher 的匹配條件。本 fork 若打 `v*` tag，未加閘門就會嘗試以 `draw-architecture` 套件名發佈。閘門是 overlay 安全邊界，不是產品行為變更。

**限制**：

- 不從本 fork 發 npm。
- 不把 `package.json` 的 `repository` 改成 SanHsien。

## 2026-08-28：fork gate 跑 Node validate，不跑瀏覽器 e2e

**決定**：`tools/dev_check.ps1` 跑 `scripts/validate.js` 與 CLI `--help`／`--version`，再跑 overlay Python。不把 Playwright 或手動截圖放進 overlay gate。

**理由**：scene linter 是上游自己的產品契約，幾秒內可在 Windows 重現。viewer 互動（pinch zoom、click-to-isolate）需要瀏覽器，Cursor stop hook 不該每次都開頁。

## 2026-08-28：現有上游 open PR 不在建置當下逐筆審查

**決定**：`reviewed_through` 設為 fork 起點 `0351ece763f79c5d76f249533bce5e43562f3058`。建置輪不寫 PR／issue watermark。

**後續**：同日全庫審查已讀 PR `#4` 並略過；baseline 改寫 `reviewed_pr_through: 4`。仍不寫 `reviewed_issue_through`（沒有獨立 open issue）。

**理由**：建置輪目標是開發環境。open PR 留到全庫審查再讀。

## 2026-08-28：略過上游 PR #4（README）

**決定**：不 cherry-pick [`yulonghe97/draw-architecture#4`](https://github.com/yulonghe97/draw-architecture/pull/4)。`reviewed_pr_through` 設為 `4`。產品英文 README 不因這份 PR 改「Node.js 18+」字樣。

**理由（證據）**：`gh pr diff 4` 只動 `README.md`（+3/−1）。開頭多兩行空行；把當時的 `Requirements: Node.js` 改成 `Node.js 18+`。PR 正文仍是舊結構（「A Claude skill…」「Try it without Claude」），對不上目前 `main`（已有 skills.sh／npm／三路安裝，見 `7b99433`）。本 fork `package.json` `engines.node` 已是 `>=18`，`docs/fork/DEVELOPMENT.md` 已寫 Node 18+。合進去會跟 overlay 頂部衝突，對產品契約無增益。作者標註由本機 `qwen3.6-35b-a3b` 產生。

**觸發條件**：若 `#4` 被 rebase 到當前 README、且只補 Node 版本下限、不改安裝來源，再重看。

## 2026-08-28：全庫審查可修 overlay 項落地

**決定**：gitignore 加 `*.pem`；`check_links.py` 掃 `.cursor/rules/no-upstream-pr.mdc`；`fork-maintenance.yml` 路徑加上 `.cursor/**`；gate 加 example canvas 重建比對與 overlay Python 禁 `shell=True`／`eval(`。當時不 pin `publish.yml` 的浮動 action、不改產品 viewer／linter。

**理由**：這幾項是本線能鎖住、且不碰產品契約的缺口。`publish.yml` 只在官方 repo 跑；當時把 action pin 留給 Dependabot／上游。

**後續**：同日改判——fork 能改的護欄就改，仍不回貢。見下方「審查可修項在本 fork 落地」。

## 2026-08-28：審查可修項在本 fork 落地（不回貢）

**決定**：本 fork 修 K-01 護欄、K-04、K-06。不拿掉 `new Function`、不改 Google Fonts、不加 Playwright、不加 lockfile、不把 `evals/` 裝進 payload。

1. `publish.yml`：checkout pin `actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803`（v6.1.0）、setup-node pin `actions/setup-node@249970729cb0ef3589644e2896645e5dc5ba9c38`（v6.5.0）；workflow 權限只留 `contents: read`；`id-token: write` 收到 job；`npm install -g npm@12.0.2` 取代 `@latest`。官方-repo-only 閘門與 `persist-credentials: false` 保留。
2. `scripts/validate.js`／`scripts/build.js` 拒絕 scene 含 `</script>`；`build.js` 對 `TITLE`／`KICKER` 做 HTML escape、對 `SLUG` 做 JS 單引號 escape。不 escape `{{SUB_HTML}}`（strapline 仍允許少量 HTML）。
3. `bin/cli.js` 加 `--cursor` → `~/.cursor/skills`；互動選單 4=Cursor、5=Custom；uninstall 預設也掃 Cursor 路徑。

**理由**：維護者指示 review 中可修的都修、先不回貢。產品信任模型核心仍是「本機 scene 由宿主 Agent 寫、用 `new Function` 執行」；護欄只擋模板破出與標題注入，不改 viewer 互動契約。

**限制**：

- 不回貢上游。merge 上游 `scripts/`、`bin/cli.js`、`publish.yml` 時必須對照本條，不要弄丟護欄。
- 不把產生的 canvas 當成已消毒的受信任來源去嵌進第三方站。

## 2026-08-29：上游檢查補上 PR 與 issue 兩個面向

**決定**：`tools/check_upstream_updates.py` 補上以 `--state all` 收集上游 PR／issue 的邏輯（比照
`SanHsien/harness-guard`），`upstream-check.yml` 補 `GH_TOKEN: ${{ github.token }}`，baseline 補
`reviewed_pr_through: 7` 與 `reviewed_issue_through: 0`。

**理由**：`UPSTREAM.md` 早就寫著「四個面向都要看」，但檢查器只讀 `reviewed_through` 一個欄位——
PR 與 issue 的水位寫在 baseline 裡，沒有任何程式讀它。那兩個面向不是「查過沒發現」，是**根本沒查**，
而每週的排程報告長得跟查過一樣綠。`gh` 在 Actions 裡沒有憑證會讓收集失敗；檢查器對此 fail closed
（exit 2），所以 token 要一起給，否則紅燈的意思會變成「檢查器壞了」而不是「上游有東西」。

**證據**：

- `gh pr list --repo yulonghe97/draw-architecture --state all` → 7 筆，最大 `#7`。
  `#1`／`#2`／`#3`／`#5`／`#6`／`#7` 都是 merged，且 merge commit 都在
  `0351ece`（`#7` 的 merge，同時是 `upstream/main` 的 tip）以內，已由 commit 水位涵蓋。
  `#4` 仍 open，2026-08-28 已讀 diff 並略過（見上方條目）。水位 4 → 7。
- `gh issue list --repo yulonghe97/draw-architecture --state all` → 0 筆。
  `reviewed_issue_through: 0` 代表「查過，是空的」，不是「沒查」。
- 落地後 `python tools/check_upstream_updates.py --strict` exit 0，三個面向都印出水位。

**測試改動**：`test_baseline_file_is_valid_and_complete` 原本把 `reviewed_date` 釘成字面
`2026-08-28`，`test_baseline_matches_decisions_record` 原本釘 `reviewed_pr_through == 4` 且要求
`reviewed_issue_through` 不存在——那是釘實作值不是釘性質，每次正當的審查都會把它變紅，壓力會落在
改測試而不是記錄審查。改成釘性質：日期符合 `YYYY-MM-DD`，三個水位都必須是整數（0 是合法值，
代表查過為空）。

**觸發條件**：上游開出 `#8` 以後的 PR 或第一個 issue 時，排程會列出來，逐筆判斷後才推進水位。

## 2026-10-25：上游檢查補上分支面向；ruff 0.17 以 freshness-hold 處理

**決定**：`tools/check_upstream_updates.py` 以 `git ls-remote --heads` 收集上游分支，和 baseline 新欄位
`reviewed_branch_heads`（分支名 → 已讀 head 的完整 SHA）比對；新分支或 head 移動才列出，`--strict` 會因此
回 1。`requirements-dev.txt` 的 `ruff>=0.16` 加行末 `# freshness-hold:`，不提高下限。

**理由**：`AGENTS.md` 與 `UPSTREAM.md` 寫「四個面向，分支記 head SHA」，但檢查器沒有分支收集，baseline 也
沒有分支欄位——和 2026-08-29 的 PR／issue 同一種「寫了沒查」。ruff 在本 repo 只閘 E9／F（`pyproject.toml`），
0.17.2 對 `tools/`、`tests/` 結果與 0.16 相同；下限是最低相容版，提高它只會逼既有環境升級，不改變閘門。

**證據**：

- `git ls-remote --heads https://github.com/yulonghe97/draw-architecture.git` → `main`（`0351ece`）以外 5 條：
  `smilewilson1999/npx-draw-architecture-cli`（`b2a2017`）、`yulonghe97/npm-token-first-publish`（`01f1ea1`）
  已是 `upstream/main` 祖先；`yulonghe97/dark-light-mode-switcher`（`cfbe227`）、`yulonghe97/fix-download-button`
  （`1d7414c`）、`yulonghe97/readme-install-guide`（`d3d32d2`）各 1 筆未進 `main` 歷史，但 `git cherry upstream/main <branch>`
  全為 `-`，即 patch 已以 squash 進 `main`（`e7ff347` #6、`2b57667` #3、`7b99433` #5）。五條都無需引進。
- 上游 commit：`0351ece..upstream/main` 0 筆；PR／issue：2026-10-24 排程 `Upstream check`
  （run `40094122768`）報告 PR 無 `#7` 以上、issue 無 `#0` 以上。
- `ruff 0.17.2`：`ruff check tools tests` → All checks passed；pytest 全綠。

**觸發條件**：上游推新分支或任一分支 head 移動時，排程列出，讀 diff 後才更新 `reviewed_branch_heads`。
ruff 若改變 E9／F 判定、或 `tools/`／`tests/` 用到只有新版才有的設定時，拿掉 hold 並提高下限。
