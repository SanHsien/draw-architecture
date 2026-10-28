# AGENTS.md

給 Codex、Claude Code、Cursor 與其他自動化代理在本專案工作時的指引。產品與使用方式先讀 [`README.md`](README.md)；開發與驗收細節見 [`docs/fork/DEVELOPMENT.md`](docs/fork/DEVELOPMENT.md)。

## 專案定位

這是 [`yulonghe97/draw-architecture`](https://github.com/yulonghe97/draw-architecture) 的 MIT fork。
核心價值是把系統架構（程式庫、架構文件或口頭描述）編成可互動的 architecture canvas，而不是再做一份靜態 Mermaid／SVG。

`origin` 是 `SanHsien/draw-architecture`，`upstream` 是原作者 repo，預設分支皆為 `main`。
保留上游作者、MIT 授權與產品 `SKILL.md`。本 fork 的維護差異記在 [`FORK.md`](FORK.md) 與 [`docs/fork/DECISIONS.md`](docs/fork/DECISIONS.md)。

主要開發與完整 overlay 驗收環境是 **Windows 11 + PowerShell**；Ubuntu CI 補跨平台相容性。
產品 scene 驗證（`node scripts/validate.js`）在 Windows 本機 gate 與 `validate.yml` 都跑。

## 硬性邊界

- **不要覆寫產品 `SKILL.md`。** 根目錄 `SKILL.md` 是給 Claude Code / Cursor / Codex 安裝的 skill 規格，不是本 fork 的維護索引。`assets/`、`bin/`、`scripts/`、`references/`、`examples/`、`evals/` 同樣以上游為準，除非有已記錄的 fork 修正（見 `FORK.md` 與 `docs/fork/DECISIONS.md`）。目前已記錄的產品修正：`scripts/build.js`／`scripts/validate.js` 的 HTML／`</script>` 護欄，以及 `bin/cli.js` 的 `--cursor`。維護規則以本檔為準。
- 不要把產品 Skill、scene 格式或 example 翻譯成繁體來「統一文件語言」。上游產品語言是英文；本 fork 的公開入口 overlay 與維護文件只使用繁體中文與英文。
- 根目錄 `README.md` 必須保持上游英文產品說明。繁中維護寫在 `FORK.md`。
- 上游 `docs/` 是產品截圖。fork 文件放 `docs/fork/`，不要把維護文件寫進 `docs/` 根層。
- 不提交使用者的 scene、產出 HTML／PNG、API key、npm token、cookie 或帳號資料；`.env*` 同樣不可提交。
- 不推送到 `upstream`。上游同步先跑 `python tools/check_upstream_updates.py`，逐筆審查後再 merge / cherry-pick；不盲目覆蓋 fork 文件與 Windows gate。
- 不新增 hosted backend、不把本 fork 包裝成原創專案、不從本 fork 發 npm（`publish.yml` 已加官方-repo-only 閘門）。
- 不把 `package.json` 的 `repository`／`bugs` 改成 SanHsien——那是 npm 套件身分，以上游為準。

## 技術與資料流

- 產品本體是 Markdown skill + 固定 viewer：`SKILL.md` → 寫 `scene.js` → `scripts/validate.js` → `scripts/build.js` 把 scene 拼進 `assets/template.html` → 單一 `index.html`。
- `bin/cli.js`：`npx draw-architecture` 安裝器，零依賴。安裝目錄名是 `architecture-canvas`。
- `tools/`：fork 維護工具（上游檢查、相對連結檢查、Windows gate、依賴新鮮度）。
- `tests/`：pytest 測 overlay 與已記錄的產品護欄。產品 layout 驗證走 Node `scripts/validate.js`。
- `pyproject.toml`：**只放工具設定**，沒有 `[project]` 與 `[build-system]`——本 repo 交付的是 Agent Skill 與 HTML canvas，不是 Python 套件。
- `.gitattributes`：index 全 LF。沒有它，全域 `core.autocrlf=true` 會讓檔案假性顯示為 modified。

## 開發原則

- 一般變更直接推 `origin/main`，不開功能分支、不開維護 PR。只有在需要他人審查、或改動風險高到值得先讓 CI 在 PR 上跑一輪時，才退回 **branch → PR → CI → merge**。與 `CONTRIBUTING.md` 一致。
- 修 bug 先補可重現失敗測試，再做最小修正。
- 上游公開安裝方式、`SKILL.md` 步驟、scene 九個常數與 viewer 互動視為相容性契約。
- 不為了套格式而大改上游檔案；Ruff 只閘 E9（語法）與 F（pyflakes），且只掃 `tools/`、`tests/`。
- 使用繁體中文回覆；維護文件以繁中為主。不要把根目錄 `README.md` 改成繁中主檔。
- 提交訊息用 Conventional Commit。Dependabot 或外部 fork 的變更也走 PR，讀 diff 並通過 CI 後再合併。
- 不 force-push `main`，不刪 `upstream` remote。

## 上游處理

1. `git fetch upstream main`
2. `python tools/check_upstream_updates.py --strict`
3. 逐筆判斷是否與繁中 overlay、Windows gate、`publish.yml` 閘門或測試衝突。
4. 可同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
5. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`
6. 採用／略過寫進 `docs/fork/DECISIONS.md`，驗證後才推進 `tools/upstream_baseline.json`

Baseline 代表「已審查」，不代表「全部已合併」。

**四個面向都要看，不是只看 commit**：commit、open PR、open issue、上游分支。每個面向各記一個
水位（`reviewed_through`／`reviewed_pr_through`／`reviewed_issue_through`，分支記 head SHA），
下次只看更大的編號或變動過的 head。

**判準是證據，不是分類。** 「產品方向」「等上游合併」「大概率同理」都不是理由。結論要寫得可查證：diff 動了哪些檔案、本 fork 對應的檔案實際長什麼樣，以及觸發條件。

上游尚未合併的 PR 一樣要看：它可能是本 fork 也中的缺陷修正。只有在「本 fork 沒有對應層」或「缺陷本 fork 不成立」這種可查證的事實下才不引用。

## 驗證

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

沒有實際跑過 Windows gate，不要宣稱本機開發環境已可用。修改維護工具或測試前，先跑對應 pytest 確認現況；直接交付可驗證結果，不要用「應該可以」代替。

## 文件責任

- `README.md`：公開產品入口。保持上游英文；來源與授權 credit 必留。
- `FORK.md`：與上游的關係、差異、同步方式。
- `NOTICE.md`：授權與 attribution。
- `docs/fork/UPSTREAM.md`：upstream remote 與審查清冊。
- `docs/fork/DEVELOPMENT.md`：本機開發與驗收指令。
- `docs/fork/DECISIONS.md`：長期取捨。
- `REVIEW.md`：全庫風險快照，不是每個一般 bug 的流水帳。
- `CONTRIBUTING.md` / `SECURITY.md` / `CODE_OF_CONDUCT.md`：本 fork 的貢獻、安全回報與行為準則。
- `CHANGELOG.md` / `CHANGELOG.en.md`：**只記本 fork 的維護歷史**，不複製上游產品演進。

## 對外邊界：PR 只打本 fork

- **PR、push、release 一律指向 `SanHsien/draw-architecture`。** 對上游 `yulonghe97/draw-architecture` 開 PR、push 或發 release
  需要維護者在當次對話明確同意回貢；「fork 一份」「建開發環境」「比照其他 repo」都不是同意。
- 根因是機制不是粗心：`gh` 在 fork clone 的**預設 repo 就是上游**（`gh repo set-default --view` 會回
  `yulonghe97/draw-architecture`），裸跑 `gh pr create` 必然打上去。每個 clone 先跑一次
  `gh repo set-default SanHsien/draw-architecture`。
- 開 PR 仍明寫 `gh pr create --repo SanHsien/draw-architecture --base <分支> --head <分支>`，並**讀輸出的 URL**，
  owner 必須是 `SanHsien`。不是就立刻 `gh pr close` 留言道歉說明，再對 origin 重開。
- 2026-08-22 一天內兩個工作階段各誤開一個上游 PR（`lidge-jun/opencodex#2373`、
  `hamanpaul/paulsha-cortex#787`）。批次跑多個 repo 時最容易略過確認，而那正是兩次出事的場合。

## 路線圖

- `ROADMAP.md` 是本 repo 後續工作的單一真相源。完成或新增工作時，在同一個 commit 更新它：做完的列刪掉、新工作加進去。不要在其他文件另列待辦。
