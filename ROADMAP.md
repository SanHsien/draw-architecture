# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `00ee0ead9774` 查的快照，開工前先重查 GitHub。

## 現況
本 repo 為 yulonghe97/draw-architecture 的維護 fork，將系統架構轉換為可互動探索的 Canvas 架構圖技能。目前健康狀況良好，CI、CodeQL、Upstream check、Fork maintenance 與 Validate scene 全綠，所有工作流程運作正常；Issues 維持停用，無待處理 open PR 與安全告警。

## 近期：可以直接動手
| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 補強 tools/check_links.py 大小寫敏感度比對 | Windows 不分大小寫導致連結拼錯在本機過、GitHub 上斷連 | 改以磁碟真實項目比對大小寫，新增回歸測試並確保 `pytest` 與 `tools/dev_check.ps1` 綠燈 | Claude Sonnet | 深掃報告（2026-10-26）；`tools/check_links.py` |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 解除 ruff freshness-hold，提高下限 | ruff 改變 E9／F 判定，或 `tools/`／`tests/` 用到只有新版才有的設定（`docs/fork/DECISIONS.md:138`） | `requirements-dev.txt` 移除 `freshness-hold` 註解並提高下限；`ruff check .` 與 `pytest tests -q` 綠；Dependency freshness 綠 | Claude Haiku | `requirements-dev.txt:2`；`docs/fork/DECISIONS.md:116-138` |
| 同步上游新提交與畫布模板更新 | `Upstream check` workflow 轉為 failure 或上游 main 有新 commit | 執行 `python tools/check_upstream_updates.py`，完成審查並更新 `tools/upstream_baseline.json`，`tools/dev_check.ps1` 綠燈 | Codex | `tools/upstream_baseline.json`；`tools/check_upstream_updates.py` |
| 修復 bin/cli.js 參數解析邊界（--dir 後接選項被當路徑） | 上游合併該修復，或維護者決定在 fork 加入本機 CLI 防護 overlay | `tests/` 新增 pytest 案例：`node bin/cli.js --dir --force` 會報錯或拒絕，cwd 不會出現 `--force` 目錄；`pytest tests -q` 綠 | Codex | 深掃報告（2026-10-26）；`bin/cli.js`；既有 CLI 測試 `tests/test_fork_overlay.py:200-231` |

## 刻意不做
| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 主動重構或覆寫上游 template.html 畫布核心 | 本 fork 專注於建置安全（build.js 注入防護）與 CLI 體驗，避免偏離上游渲染核心 | 上游畫布存在嚴重未修復的安全性漏洞或重大記憶體洩漏 |
| 引進上游 PR #4（README 空行與 Node 18+ 宣稱） | 已讀 diff 並略過（`docs/fork/DECISIONS.md:56-62`） | #4 被 rebase 到當前 README、且只補 Node 版本下限、不改安裝來源 |

## 維護方式
- 每週由 `Upstream check` 自動排程追蹤上游更新，有新提交或突破水位時才進行人工審查移植。
- 本地開發遵循 `tools/dev_check.ps1` 全套門禁（包含 pytest、ruff、scene 驗證與連結檢查）。