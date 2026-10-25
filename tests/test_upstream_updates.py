"""What the upstream checker must not be allowed to do.

Every test here names a way the check could go quiet without anybody deciding
to stop watching upstream.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_upstream_updates as checker  # noqa: E402, I001


BASELINE = {
    "repo": "https://github.com/example/product.git",
    "branch": "main",
    "reviewed_through": "a" * 40,
    "reviewed_date": "2026-08-29",
}


def fake_gh(payload: object, returncode: int = 0):
    """Stand in for `gh`, so no test reaches the network."""

    def runner(args, **kwargs):
        assert args[0] == "gh"
        assert "--state" in args and args[args.index("--state") + 1] == "all"
        return subprocess.CompletedProcess(
            args, returncode, stdout=json.dumps(payload), stderr=""
        )

    return runner


def test_tickets_are_queried_with_state_all(monkeypatch):
    """An item opened and closed between two runs was still never triaged."""
    monkeypatch.setattr(
        checker.subprocess,
        "run",
        fake_gh([{"number": 9, "title": "closed without merging"}]),
    )
    tickets = checker.collect_new_tickets(BASELINE, "pr")
    assert tickets == [{"number": 9, "title": "closed without merging"}]


def test_items_at_or_below_the_watermark_are_not_re_reported(monkeypatch):
    monkeypatch.setattr(
        checker.subprocess,
        "run",
        fake_gh([{"number": 4, "title": "old"}, {"number": 5, "title": "new"}]),
    )
    baseline = {**BASELINE, "reviewed_pr_through": 4}
    assert [t["number"] for t in checker.collect_new_tickets(baseline, "pr")] == [5]


def test_ticket_titles_survive_undecodable_bytes(monkeypatch):
    """Titles are written by strangers and the console is not always UTF-8.

    Without an explicit `errors`, one undecodable byte kills the whole upstream
    check instead of costing one garbled character.
    """
    captured = {}

    def runner(args, **kwargs):
        captured.update(kwargs)
        return subprocess.CompletedProcess(args, 0, stdout="[]", stderr="")

    monkeypatch.setattr(checker.subprocess, "run", runner)
    checker.collect_new_tickets(BASELINE, "pr")

    assert captured["errors"] == "replace"


def test_gh_failure_reports_unchecked_rather_than_empty(monkeypatch):
    """`None`, not `[]`: "not checked" must never render as "nothing to review"."""
    monkeypatch.setattr(checker.subprocess, "run", fake_gh([], returncode=1))
    assert checker.collect_new_tickets(BASELINE, "issue") is None


def test_report_says_so_when_tickets_could_not_be_enumerated():
    report = checker.render_markdown(BASELINE, [], prs=None, issues=None)
    assert "Not checked" in report


def test_report_covers_all_three_axes_even_when_commits_are_clean():
    report = checker.render_markdown(BASELINE, [], prs=[], issues=[])
    assert "## Commits" in report
    assert "## Upstream pull requests" in report
    assert "## Upstream issues" in report


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://github.com/example/product.git", "example/product"),
        ("https://github.com/example/product", "example/product"),
        ("git@github.com:example/product.git", "example/product"),
        ("https://gitlab.com/example/product.git", None),
    ],
)
def test_upstream_slug(url, expected):
    assert checker.upstream_slug(url) == expected


def test_shipped_baseline_matches_the_documented_upstream():
    baseline = checker.load_baseline()
    assert checker.upstream_slug(baseline["repo"]) is not None


def fake_ls_remote(heads: dict[str, str]):
    """Stand in for `git ls-remote --heads`, so no test reaches the network."""

    def runner(args, **kwargs):
        assert args[:3] == ["git", "ls-remote", "--heads"]
        stdout = "".join(f"{sha}\trefs/heads/{name}\n" for name, sha in heads.items())
        return subprocess.CompletedProcess(args, 0, stdout=stdout, stderr="")

    return runner


def test_unrecorded_upstream_branch_is_reported(monkeypatch):
    """A fix can sit on a branch with no PR; the commit axis never sees it."""
    monkeypatch.setattr(
        checker.subprocess,
        "run",
        fake_ls_remote({"main": "a" * 40, "fix-crash": "b" * 40}),
    )
    branches = checker.collect_branch_changes(BASELINE, REPO_ROOT)
    assert [(b["name"], b["sha"], b["previous"]) for b in branches] == [
        ("fix-crash", "b" * 40, None)
    ]


def test_branch_is_re_reported_only_when_its_head_moves(monkeypatch):
    monkeypatch.setattr(
        checker.subprocess,
        "run",
        fake_ls_remote({"main": "a" * 40, "same": "b" * 40, "moved": "d" * 40}),
    )
    baseline = {
        **BASELINE,
        "reviewed_branch_heads": {"same": "b" * 40, "moved": "c" * 40},
    }
    branches = checker.collect_branch_changes(baseline, REPO_ROOT)
    assert [(b["name"], b["previous"]) for b in branches] == [("moved", "c" * 40)]


def test_report_covers_the_branch_axis():
    report = checker.render_markdown(BASELINE, [], prs=[], issues=[], branches=[])
    assert "## Upstream branches" in report


def test_shipped_baseline_records_every_branch_head_it_claims_to_have_read():
    baseline = checker.load_baseline()
    heads = baseline.get("reviewed_branch_heads")
    assert heads, "branch axis has no watermark; it is not being watched"
    assert all(len(sha) == 40 for sha in heads.values())


def test_report_lists_new_and_moved_branch_heads():
    branches = [
        {"name": "fix", "sha": "b" * 40, "short": "b" * 7, "previous": None},
        {"name": "moved", "sha": "d" * 40, "short": "d" * 7, "previous": "c" * 40},
    ]
    report = checker.render_markdown(BASELINE, [], prs=[], issues=[], branches=branches)
    assert "| `fix` | `bbbbbbb` | (new) |" in report
    assert "| `moved` | `ddddddd` | `ccccccc` |" in report


def test_strict_fails_when_only_a_branch_head_moved(monkeypatch, tmp_path):
    """A moved branch is review work even when every other axis is clean."""
    monkeypatch.setattr(checker, "load_baseline", lambda: dict(BASELINE))
    monkeypatch.setattr(checker, "fetch_upstream", lambda baseline, repo_dir: "ref")
    monkeypatch.setattr(checker, "collect_new_commits", lambda *args: [])
    monkeypatch.setattr(checker, "collect_new_tickets", lambda baseline, kind: [])
    monkeypatch.setattr(
        checker,
        "collect_branch_changes",
        lambda baseline, repo_dir: [
            {"name": "fix", "sha": "b" * 40, "short": "b" * 7, "previous": None}
        ],
    )
    monkeypatch.setattr(
        sys, "argv", ["check", "--strict", "--output", str(tmp_path / "r.md")]
    )
    assert checker.main() == 1
