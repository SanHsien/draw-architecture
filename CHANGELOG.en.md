English | [中文版](CHANGELOG.md)

# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); newest first.
This file records **this fork's maintenance history** only (from 2026-08-28). The product
history of upstream
[`yulonghe97/draw-architecture`](https://github.com/yulonghe97/draw-architecture) lives in its
own history and in the review ledger at [`docs/fork/UPSTREAM.md`](docs/fork/UPSTREAM.md).
Per-commit adopt/skip reasoning is recorded in [`docs/fork/DECISIONS.md`](docs/fork/DECISIONS.md).

---

## 2026-10-25 (continued development, `46ae0c0`, `0ef829e`)

### Changed

- **Upstream check covers branches.** `check_upstream_updates.py` compares `git ls-remote --heads` against `reviewed_branch_heads` and lists only new branches or moved heads.
- **ruff 0.17 handled with `freshness-hold`.** Only E9/F are gated and 0.17.2 passes; the floor stays `>=0.16`.

---

## 2026-08-28 (review remediations)

### Changed

- **Pinned `publish.yml` action SHAs.** checkout and setup-node now use full SHAs; OIDC `id-token` is job-scoped; npm is pinned to `12.0.2`. The official-repo-only guard is unchanged.
- **build/validate reject `</script>` breakout.** `TITLE`/`KICKER` are HTML-escaped; `SLUG` is JS-single-quote-escaped. Strapline `{{SUB_HTML}}` still allows a little HTML. `new Function` stays.
- **CLI `--cursor`.** Installs to `~/.cursor/skills`; uninstall also scans that path by default.

This pass does not contribute back upstream. Still unchanged: Google Fonts, browser e2e, lockfile, and keeping `evals/` out of the install payload.

---

## 2026-08-28 (full-repo review)

### Changed

- **Rewrote `REVIEW.md`.** Records the product sampling, the skip evidence for upstream PR `#4`, and the overlay remediations from this pass.
- **`.gitignore` now lists `*.pem`.** Matches the other maintenance forks.
- **Link checker covers the Cursor rule.** Relative links in `no-upstream-pr.mdc` go through `check_links.py`.
- **Example canvas rebuild check.** `shoply-canvas.html` must equal a fresh `build.js` output.
- **Upstream PR `#4` was read and skipped.** `reviewed_pr_through` is now 4.

This pass does not contribute back upstream.

---

## 2026-08-28 (create a Windows-first maintenance fork)

### Added

- **Fork overlay.** `FORK.md`, `NOTICE.md`, `REVIEW.md`, `SECURITY.md`, `docs/fork/`, the Windows gate, `validate.yml`, `upstream-check`, CodeQL, and Dependabot.
- **Official-repo-only guard on `publish.yml`.** Tagging `v*` on this fork will not publish the upstream npm package.

### Changed

- **Overlay banner on `README.md`.** Product prose still follows upstream English.

This pass does not contribute back upstream.
