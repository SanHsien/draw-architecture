# 上游維護

## Remote

- Fork：`origin` → `https://github.com/SanHsien/draw-architecture.git`
- 原作者：`upstream` → `https://github.com/yulonghe97/draw-architecture.git`
- 追蹤分支：`main`

## 檢查新提交

```powershell
git fetch upstream main
python tools\check_upstream_updates.py --strict
```

工具以 `tools/upstream_baseline.json` 的 `reviewed_through` 為起點，列出所有未審查提交。
有新提交或檢查失敗時，`--strict` 回傳非零；排程 workflow 也會因此明確失敗。

## 審查清冊

每次只做一次批次審查：

1. 讀 commit 主旨與變更檔案（open PR 必須讀 diff，禁止只憑標題／「等上游定案」結案）。
2. 判斷是否與 fork overlay、Windows gate、`publish.yml` 閘門或測試衝突。
3. 可直接同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
4. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`。產品 viewer／linter 有動再打開 example canvas。
5. 在 `docs/fork/DECISIONS.md` 記錄採用／略過理由（須引用具體檔案與衝突點）。
6. 驗證完成後才把 baseline 推進到已審查的完整 40 字元 SHA。

Baseline 代表「已審查」，不代表「全部已合併」。

**四個面向都要看，不是只看 commit**：commit、open PR、open issue、上游分支。

README 衝突的解法：保留頂部 overlay，把上游新產品說明留在英文 `README.md`。不要把公開入口改成繁中主檔。來源與授權 credit 留在 README 與 `NOTICE.md`。

`publish.yml` 的官方-repo-only 閘門、`persist-credentials: false`、action SHA pin、job-scoped `id-token` 與釘死的 `npm@12.0.2` 是 fork overlay。`scripts/build.js`／`scripts/validate.js` 的 HTML／`</script>` 護欄與 `bin/cli.js` 的 `--cursor` 也是。merge 上游時若這些檔一起改，要對照，不要弄丟。

## 2026-08-28：fork 起點

本 fork 自上游 `main` `0351ece763f79c5d76f249533bce5e43562f3058` 建立。此 SHA 設為第一個 `reviewed_through`。
之後的上游 commit 才需要進入審查清冊。

建置當下 GitHub 上已有 open PR `#4`（`docs: improve README`）。2026-08-28 全庫審查已讀該 diff 並略過；baseline 寫 `reviewed_pr_through: 4`。沒有獨立的 open issue。

## 2026-08-29：PR 與 issue 面向真的接上排程

在此之前，`UPSTREAM.md` 寫著「四個面向都要看」，但 `tools/check_upstream_updates.py` 只讀
`reviewed_through`；PR／issue 的水位放在 baseline 裡沒有程式讀，所以那兩個面向根本沒被排程檢查，
報告卻是綠的。檢查器已補上 `--state all` 的 PR／issue 收集，`gh` 無法列舉時回 `None` 而不是 `[]`
並 fail closed（exit 2）——「沒查到」和「沒有」在綠色報告裡長得一樣，只有一個是真的。

水位現況：`reviewed_pr_through: 7`（`#1`–`#7` 全數處理完，理由見 `DECISIONS.md` 2026-08-29 條目）、
`reviewed_issue_through: 0`（上游 issue 數為 0，查過為空）。`upstream-check.yml` 需要
`GH_TOKEN: ${{ github.token }}`，少了它檢查器會 fail closed。

## 2026-10-25：分支面向接上排程

檢查器原本沒有分支收集。現在以 `git ls-remote --heads` 比對 baseline 的 `reviewed_branch_heads`，
新分支或 head 移動才列出。上游 5 條非 `main` 分支的 patch 都已在 `0351ece` 內（證據見 `DECISIONS.md`
2026-10-25 條目），水位記各自 head SHA。
