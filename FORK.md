# Fork 維護說明

本 repo fork 自 [`yulonghe97/draw-architecture`](https://github.com/yulonghe97/draw-architecture)，
沿用 MIT License 與完整 Git 歷史。

## 為什麼維護 fork

- 保留上游持續更新的 architecture-canvas skill：文字描述 → `scene.js` → 可拖曳、縮放、點選隔離的互動 canvas，以及 2× PNG 匯出。
- 採 Windows-first 維護：Windows 11 + PowerShell 是主要開發、除錯與完整 overlay 驗收環境。
- 繁中維護規則放 `FORK.md`；根目錄 `README.md` 必須保持上游英文產品說明。
- 建立可重現的 Windows fork gate、fork CI、產品 scene 驗證，以及逐筆審查的上游追蹤。
- 產品 skill 仍可直接安裝到 Agent Skills 目錄呼叫。

**回貢判準：修的是上游的 bug 就送回去；這裡獨創的文件／Windows 維護骨架留在這裡。**
回貢前必須在當次對話取得維護者明確同意；「fork」「建開發環境」「開 PR」都不是同意。

## 與上游的差異

| 項目 | 說明 |
|---|---|
| `README.md` | 上游英文產品說明 + 頂部 fork overlay。繁中維護在 `FORK.md`／`REVIEW.md` |
| `AGENTS.md` | 本 fork 的 AI 維護單一真相源 |
| `NOTICE.md` / `FORK.md` | 來源、授權與同步說明 |
| `SECURITY.md` / `CONTRIBUTING.md` | 本線 overlay 問題走 SanHsien；產品貢獻與產品漏洞仍指向上游 |
| `tools/dev_check.ps1` | Windows 本機一鍵 fork gate（含 example scene 驗證） |
| `.github/workflows/fork-maintenance.yml` | fork 文件與連結檢查 |
| `.github/workflows/validate.yml` | **在本 fork 跑** `node scripts/validate.js` |
| `.github/workflows/publish.yml` | 官方-repo-only 閘門；checkout／setup-node pin SHA；OIDC 權限放在 job；npm pin `12.0.2` |
| `.github/workflows/upstream-check.yml` | 每週對 `upstream/main` 做未審查 commit 檢查 |
| `scripts/build.js`／`scripts/validate.js` | 本 fork：escape `TITLE`／`KICKER`；拒絕 scene 內 `</script>`。`{{SUB_HTML}}` 仍允許 strapline HTML |
| `bin/cli.js` | 本 fork：`--cursor` 裝到 `~/.cursor/skills` |
| `docs/fork/` | Windows 開發、上游審查、決策（上游 `docs/` 是產品截圖） |

產品 `SKILL.md`、`assets/`、`references/`、`examples/`、`evals/` 以上游為準。`scripts/` 與 `bin/cli.js` 的上述護欄是已記錄的 fork 修正。

## 分支與 remote

- `origin/main`：SanHsien 維護線，也是唯一長期分支。
- 日常修改在本機跑 gate 後直接推 `origin/main`。
- `upstream/main`：yulonghe97 原始專案，只追蹤、不推送。
- Dependabot 或外部 fork 的變更走 PR，讀 diff 並通過 CI 後再合併。

不要 `git push upstream`。同步方式見 [`docs/fork/UPSTREAM.md`](docs/fork/UPSTREAM.md)。

上游更新英文 `README.md` 時，保留頂部 overlay，不要把產品說明改寫成維護索引。繁中維護差異寫在 `FORK.md`。來源 credit 留在 README 與 [`NOTICE.md`](NOTICE.md)。

## 換一台電腦怎麼開發

```powershell
git clone https://github.com/SanHsien/draw-architecture.git
cd draw-architecture
gh repo set-default SanHsien/draw-architecture
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

這是 fork 文件、連結與 example scene 的硬閘門。產品 viewer／linter 行為變更再手動打開 `examples/shoply-canvas.html` 看互動。

只想使用產品、不開發時，請走上游官方來源（見 [`README.md`](README.md)）：

```powershell
npx skills add yulonghe97/draw-architecture
```

不要把 `tools/`、`docs/fork/`、`.github/workflows/fork-maintenance.yml` 當成產品裝包。

## 審查紀錄

本輪倉庫審查見 [`REVIEW.md`](REVIEW.md)。
