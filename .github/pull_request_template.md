## 變更

簡述問題、修正與使用者可觀察到的結果。

## 類型

- [ ] Bug 修復
- [ ] 新功能
- [ ] 文件／開發環境
- [ ] 上游同步
- [ ] 測試／CI

## 驗證

- [ ] `pwsh -NoProfile -File tools\dev_check.ps1`
- [ ] 產品 viewer／linter 有動：`node scripts/validate.js examples/shoply-scene.js`，並打開 example canvas
- [ ] 沒有提交 `.env*`、憑證或使用者生成的 HTML／PNG／scene

## 上游與相容性

說明是否來自 upstream、是否改動 `SKILL.md`／`assets/`／`scripts/`／`bin/`，以及需要保留的 fork 差異。
本線 PR 必須打到 `SanHsien/draw-architecture`。對上游開 PR 需要維護者在當次對話明確同意回貢。
