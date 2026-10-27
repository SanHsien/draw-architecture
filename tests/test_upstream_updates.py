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


def test_shipped_baseline_records_every_branch_head_it_claims_to_have_read():
    baseline = checker.load_baseline()
    heads = baseline.get("reviewed_branch_heads")
    assert heads, "branch axis has no watermark; it is not being watched"
    assert all(len(sha) == 40 for sha in heads.values())


def test_missing_gh_binary_reports_unchecked_rather_than_crashing(monkeypatch):
    """No `gh` on PATH raises FileNotFoundError, not a non-zero exit code."""

    def runner(args, **kwargs):
        raise FileNotFoundError(2, "No such file or directory", "gh")

    monkeypatch.setattr(checker.subprocess, "run", runner)
    assert checker.collect_new_tickets(BASELINE, "pr") is None
