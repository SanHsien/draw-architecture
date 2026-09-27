# 貢獻指南

> **SanHsien 維護型 fork。** 本線的 overlay／Windows gate／文件問題打到 [`SanHsien/draw-architecture`](https://github.com/SanHsien/draw-architecture)。產品行為（`SKILL.md`、viewer 模板、validator、builder、安裝器、example scene）的貢獻請去上游 [`yulonghe97/draw-architecture`](https://github.com/yulonghe97/draw-architecture)。維護規則見 [`FORK.md`](FORK.md)。
>
> 本線 clone：
>
> ```powershell
> git clone https://github.com/SanHsien/draw-architecture.git
> gh repo set-default SanHsien/draw-architecture
> ```

## 開始前

1. 先讀 [`AGENTS.md`](AGENTS.md)、[`FORK.md`](FORK.md)、[`README.md`](README.md) 與 [`REVIEW.md`](REVIEW.md)。
2. 確認問題在最新 `main` 仍可重現，並查過既有 Issues。
3. 產品 skill、viewer、linter 或 scene 格式的實質變更，優先考慮回報 [`yulonghe97/draw-architecture`](https://github.com/yulonghe97/draw-architecture)。
4. 不要附上使用者 scene、產出 HTML／PNG 或任何憑證。

## 本機開發

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

產品 viewer／linter 變更時，另跑：

```powershell
node scripts/validate.js examples/shoply-scene.js
node scripts/build.js --scene examples/shoply-scene.js --out examples/shoply-canvas.html `
  --title "Shoply — platform architecture" `
  --kicker "SHOPLY — PLATFORM ARCHITECTURE" `
  --sub "<b>browse</b> → <b>price</b> → <b>order</b> → <b>fulfil</b> → <b>learn</b>" `
  --slug shoply-architecture
```

然後在瀏覽器打開 `examples/shoply-canvas.html`。不要直接手改已建好的 example HTML。

## 提交方式

本 fork 由維護者直接推 `main`，不開短期分支。改完先跑上面的 Windows gate。

- 一次提交聚焦一個問題。
- Bug 修正先附失敗測試；新行為需涵蓋成功、邊界與錯誤路徑。
- 修改使用方式時同步更新 `README.md` 頂部 overlay 與 `FORK.md`。不要把產品 README 改成繁中主檔。
- 說明是否來自 upstream、是否改動產品 `SKILL.md`／`assets/`／`scripts/`／`bin/`，以及實際跑過哪些指令。
- 提交訊息建議使用 `fix:`、`feat:`、`docs:`、`test:`、`chore:`。
- Dependabot 與外部 fork 仍可能開 Pull Request；合併前讀 diff，不要自動合併。
- 對上游開 PR 需要維護者在當次對話明確同意回貢。本線 PR 必須打到 `SanHsien/draw-architecture`。
