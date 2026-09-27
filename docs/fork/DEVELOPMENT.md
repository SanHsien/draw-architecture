# 開發環境

維護者與 AI 接手用的開發文件。產品用法看 [`README.md`](../../README.md)；上游同步在 [`UPSTREAM.md`](UPSTREAM.md)；決策在 [`DECISIONS.md`](DECISIONS.md)。

## 架構

```text
Agent 讀 SKILL.md
        │
        ▼
   寫 scene.js（純資料：PLANES / BANDS / BOXES / EDGES / …）
        │
        ├─ node scripts/validate.js   佈局 linter
        └─ node scripts/build.js      拼進 assets/template.html
                │
                ▼
        單一 index.html（pan / zoom / isolate / PNG）
```

- `SKILL.md`：skill 規格與流水線。
- `assets/template.html`：固定 viewer。
- `scripts/validate.js`、`scripts/build.js`：驗證與組裝。
- `bin/cli.js`：`npx draw-architecture` 安裝器。
- `examples/`：Shoply 典範 scene 與已建 canvas。
- `FORK.md`、`tools/`、`docs/fork/` 是本 fork 的開發與治理骨架。

不要把 fork pytest 寫進產品 `examples/`。fork 測試放 `tests/`。

## 本機開發（Windows）

需要 Python 3.11+（fork gate）與 Node 18+（產品 validate／build）。本機已驗證 Node 26 + Python 3.14。

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
$env:PYTHONUTF8 = "1"
pwsh -NoProfile -File tools\dev_check.ps1
```

## Canonical fork gate

`tools\dev_check.ps1` 會依序：

1. `node scripts/validate.js examples/shoply-scene.js`
2. `node bin/cli.js --version` 與 `--help`
3. `python -m compileall`（`tools`、`tests`）
4. `ruff check`（E9 + F，僅 overlay Python）
5. `pytest tests -q`
6. `python tools/check_links.py`

這是 fork 文件與 example scene 的硬閘門，不是瀏覽器裡的互動回歸。viewer 行為變更時，在瀏覽器打開 `examples/shoply-canvas.html`。

上游沒有產品 unit CI；本 fork 的 `validate.yml` 在 Ubuntu 與 Windows 上跑同一條 Node 驗證。`publish.yml` 只在官方 `yulonghe97/draw-architecture` 發 npm。

## 不要做的事

- 不要把產品 `README.md` 改成繁中主檔。
- 不要覆寫 `SKILL.md`、`assets/template.html` 來「統一風格」。`scripts/` 與 `bin/cli.js` 以上游為準，只保留 `FORK.md` 已記錄的護欄（TITLE／KICKER escape、`</script>` 拒絕、`--cursor`）。
- 不要提交 `.env*`、API key、npm token 或使用者生成的 HTML／PNG／scene。
- 不要從本 fork 發 npm、不要改 `package.json` 的 `repository` 欄位。
- 不要對上游開 PR，除非維護者在當次對話明確同意回貢。
