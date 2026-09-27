from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_dependency_freshness as checker  # noqa: E402


def test_comparison_uses_the_precision_the_declaration_states() -> None:
    assert not checker.is_newer_version("7.4.0", "7")
    assert checker.is_newer_version("8.0.0", "7")
    assert checker.is_newer_version("7.4.0", "7.3")
    assert not checker.is_newer_version("7.3.2", "7.3")


def test_prerelease_suffix_does_not_count_as_newer() -> None:
    assert not checker.is_newer_version("7.0.0rc1", "7.0.0")


def test_hold_marker_is_read_off_the_declaring_line() -> None:
    packages = checker.parse_requirements(
        "pytest>=8.3  # freshness-hold: keep floor\n"
        "ruff>=0.16\n",
        "requirements-dev.txt",
    )

    holds = {package["name"]: package["hold"] for package in packages}
    assert holds["ruff"] == ""
    assert holds["pytest"] == "keep floor"


def test_a_held_floor_is_reported_but_does_not_ask_for_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(checker, "fetch_pypi_version", lambda name: "9.1.0")
    packages = checker.parse_requirements(
        "pytest>=8.3.0  # freshness-hold: pytest 9 needs newer Python\n",
        "requirements-dev.txt",
    )
    rows = checker.collect_status(packages)
    assert rows[0]["outdated"] is True
    assert rows[0]["hold"]
    report = checker.render_markdown(rows)
    assert "HELD:" in report
    assert "REVIEW UPDATE" not in report


def test_requirements_dev_declares_pytest_and_ruff() -> None:
    packages = checker.load_direct_dependencies()
    names = {package["name"] for package in packages}
    assert names == {"pytest", "ruff"}
    by_name = {package["name"]: package for package in packages}
    assert by_name["pytest"]["minimum"] == "9.1"
    assert by_name["pytest"]["requirement"] == "pytest>=9.1"
