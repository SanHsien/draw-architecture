[English](CHANGELOG.en.md) | 中文版

# 變更紀錄

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，新的在上面。
本檔只記錄**本 fork 的維護歷史**（2026-08-28 起）；上游
[`yulonghe97/draw-architecture`](https://github.com/yulonghe97/draw-architecture)
的產品演進見其自身歷史與 [`docs/fork/UPSTREAM.md`](docs/fork/UPSTREAM.md) 的審查清冊。
逐筆採用／略過的理由記在 [`docs/fork/DECISIONS.md`](docs/fork/DECISIONS.md)。

---

## 2026-10-25（接續開發）

### 變更

- **上游檢查補分支面向。** `check_upstream_updates.py` 以 `git ls-remote --heads` 比對 `reviewed_branch_heads`，新分支或 head 移動才列出。
- **ruff 0.17 以 `freshness-hold` 處理。** 只閘 E9／F，0.17.2 已驗證全綠；下限維持 `>=0.16`。

---

## 2026-08-28（審查可修項落地）

### 變更

- **`publish.yml` pin action SHA。** checkout／setup-node 釘完整 SHA；OIDC `id-token` 收到 job；npm 釘 `12.0.2`。官方-repo-only 閘門不變。
- **build／validate 擋 `</script>` 破出。** `TITLE`／`KICKER` 做 HTML escape；`SLUG` 做 JS 單引號 escape。strapline `{{SUB_HTML}}` 仍允許少量 HTML。不拿掉 `new Function`。
- **CLI 加 `--cursor`。** 裝到 `~/.cursor/skills`；uninstall 預設也掃該路徑。

本輪不回貢。維持不改：Google Fonts、瀏覽器 e2e、lockfile、`evals/` 不進安裝 payload。

---

## 2026-08-28（全庫審查）

### 變更

- **重寫 `REVIEW.md`。** 寫入產品抽查、上游 PR `#4` 略過證據、以及本輪 overlay 可修項。
- **gitignore 加 `*.pem`。** 與其他維護 fork 對齊。
- **連結檢查掃 Cursor 規則。** `no-upstream-pr.mdc` 的相對連結納入 `check_links.py`。
- **example canvas 重建比對。** `shoply-canvas.html` 必須等於當下 `build.js` 產出。
- **上游 PR `#4` 已讀並略過。** `reviewed_pr_through` 設為 4。

本輪不回貢。

---

## 2026-08-28（建立 Windows-first 維護型 fork）

### 新增

- **Fork overlay。** `FORK.md`、`NOTICE.md`、`REVIEW.md`、`SECURITY.md`、`docs/fork/`、Windows gate、`validate.yml`、`upstream-check`、CodeQL、Dependabot。
- **`publish.yml` 官方-repo-only 閘門。** 本 fork 打 `v*` tag 不會對 npm 發佈上游套件。

### 變更

- **`README.md` 加頂部 overlay。** 產品正文仍以上游英文為準。

本輪不回貢。
