from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_links  # noqa: E402
import check_upstream_updates as checker  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_REPO = "yulonghe97/draw-architecture"
FORK_REPO = "SanHsien/draw-architecture"
UNGATED_WORKFLOWS = (
    "fork-maintenance.yml",
    "upstream-check.yml",
    "validate.yml",
    "codeql.yml",
    "dependency-freshness.yml",
)
GATED_WORKFLOWS = ("publish.yml",)


def test_baseline_file_is_valid_and_complete() -> None:
    baseline = checker.load_baseline()

    assert baseline["repo"].endswith("draw-architecture.git")
    assert baseline["branch"] == "main"
    assert len(baseline["reviewed_through"]) == 40
    # The date is pinned as a shape, not as a literal: a hardcoded date turns
    # every legitimate review into a test failure, and the pressure is then to
    # edit the test rather than to record the review.
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", baseline["reviewed_date"])


def test_workflow_is_scheduled_and_fails_on_unreviewed_commits() -> None:
    workflow = (
        ROOT / ".github" / "workflows" / "upstream-check.yml"
    ).read_text(encoding="utf-8")

    assert "schedule:" in workflow
    assert "cron:" in workflow
    assert "workflow_dispatch:" in workflow
    assert "tools/check_upstream_updates.py" in workflow
    assert "fetch-depth: 0" in workflow
    assert "exit 1" in workflow


def test_render_markdown_reports_no_new_commits() -> None:
    baseline = {
        "repo": "https://example.invalid/upstream.git",
        "branch": "main",
        "reviewed_through": "a" * 40,
        "reviewed_date": "2026-08-28",
    }

    report = checker.render_markdown(baseline, [])

    assert "No new upstream commits" in report


def test_render_markdown_surfaces_check_failure() -> None:
    baseline = {
        "repo": "https://example.invalid/upstream.git",
        "branch": "main",
        "reviewed_through": "a" * 40,
        "reviewed_date": "2026-08-28",
    }

    report = checker.render_markdown(baseline, [], error="git fetch failed")

    assert "Check failed" in report
    assert "git fetch failed" in report


def test_load_baseline_rejects_missing_file(tmp_path: Path) -> None:
    try:
        checker.load_baseline(tmp_path / "nope.json")
    except checker.UpstreamCheckError:
        return
    raise AssertionError("expected UpstreamCheckError")


def test_baseline_matches_decisions_record() -> None:
    decisions = (ROOT / "docs" / "fork" / "DECISIONS.md").read_text(encoding="utf-8")
    upstream = (ROOT / "docs" / "fork" / "UPSTREAM.md").read_text(encoding="utf-8")
    baseline = json.loads(
        (ROOT / "tools" / "upstream_baseline.json").read_text(encoding="utf-8")
    )

    assert baseline["reviewed_date"] in decisions
    assert baseline["reviewed_through"][:7] in upstream
    # All four upstream axes carry a watermark. Leaving one out is not "checked
    # and found nothing" -- it is not checked at all, and the report still reads
    # green. Zero is a legitimate value: it means the axis was queried and was
    # empty, which is why the number has to be present rather than merely
    # truthy.
    assert isinstance(baseline["reviewed_pr_through"], int)
    assert isinstance(baseline["reviewed_issue_through"], int)


def test_overlay_markdown_links_resolve() -> None:
    failures = 0
    for path in check_links.iter_documents():
        problems = check_links.check_document(path)
        failures += len(problems)
        for problem in problems:
            print(f"{path}: {problem}")
    assert failures == 0


def test_readme_keeps_upstream_english_product_contract() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert not (ROOT / "README.en.md").exists()
    assert "SanHsien 維護型 fork" in readme
    assert FORK_REPO in readme
    assert OFFICIAL_REPO in readme
    assert "FORK.md" in readme
    assert "REVIEW.md" in readme
    assert "architecture-canvas" in readme
    assert "MIT" in readme
    assert "npx skills add yulonghe97/draw-architecture" in readme


def test_link_checker_skips_product_readme_and_scans_review() -> None:
    rels = {path.relative_to(ROOT).as_posix() for path in check_links.iter_documents()}

    assert "README.md" not in rels
    assert "REVIEW.md" in rels
    assert "FORK.md" in rels
    assert ".cursor/rules/no-upstream-pr.mdc" in rels
    assert "NOTICE.md" in rels
    assert "SECURITY.md" in rels
    assert "CONTRIBUTING.md" in rels
    assert "docs/fork/DECISIONS.md" in rels


def test_missing_relative_rejects_path_escape() -> None:
    problem = check_links._missing_relative(ROOT / "FORK.md", "../outside-the-repo")

    assert problem is not None
    assert "逃出 repo 根目錄" in problem
    assert check_links._missing_relative(ROOT / "FORK.md", "NOTICE.md") is None


def test_agents_overlay_points_at_fork_rules() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "SanHsien/draw-architecture" in agents
    assert "FORK.md" in agents
    assert "不推送到 `upstream`" in agents
    assert "architecture-canvas" in agents
    assert "REVIEW.md" in agents
    assert "--cursor" in agents
    assert "</script>" in agents


def test_fork_records_product_hardening() -> None:
    fork = (ROOT / "FORK.md").read_text(encoding="utf-8")
    decisions = (ROOT / "docs" / "fork" / "DECISIONS.md").read_text(encoding="utf-8")
    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")

    assert "--cursor" in fork
    assert "</script>" in fork
    assert "npm@12.0.2" in decisions
    assert "d23441a48e516b6c34aea4fa41551a30e30af803" in decisions
    assert "</script>" in security
    assert "--cursor" in security


def test_skill_frontmatter_names_architecture_canvas() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert skill.lstrip().startswith("---")
    assert "name: architecture-canvas" in skill


def test_example_scene_validates() -> None:
    result = subprocess.run(
        [
            "node",
            str(ROOT / "scripts" / "validate.js"),
            str(ROOT / "examples" / "shoply-scene.js"),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_cli_reports_version_and_help() -> None:
    version = subprocess.run(
        ["node", str(ROOT / "bin" / "cli.js"), "--version"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    help_text = subprocess.run(
        ["node", str(ROOT / "bin" / "cli.js"), "--help"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    assert version.stdout.strip() == package["version"]
    assert "architecture-canvas" in help_text.stdout
    assert "--global" in help_text.stdout
    assert "--cursor" in help_text.stdout
    assert ".cursor" in help_text.stdout.replace("\\", "/")


def test_package_json_keeps_upstream_npm_identity() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    assert package["name"] == "draw-architecture"
    assert package["license"] == "MIT"
    assert OFFICIAL_REPO in package["repository"]["url"]
    assert package.get("dependencies") in (None, {})
    assert package["bin"]["draw-architecture"] == "bin/cli.js"


def test_product_validate_workflow_runs_on_this_fork() -> None:
    ci = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
    assert "node scripts/validate.js examples/shoply-scene.js" in ci
    assert "persist-credentials: false" in ci
    assert f"github.repository == '{OFFICIAL_REPO}'" not in ci


def test_every_workflow_is_classified() -> None:
    names = {path.name for path in (ROOT / ".github" / "workflows").glob("*.yml")}
    assert names == set(UNGATED_WORKFLOWS) | set(GATED_WORKFLOWS)


def test_ungated_workflows_are_not_official_repo_only() -> None:
    official_guard = f"github.repository == '{OFFICIAL_REPO}'"
    workflows = ROOT / ".github" / "workflows"
    for name in UNGATED_WORKFLOWS:
        text = (workflows / name).read_text(encoding="utf-8")
        assert official_guard not in text, name


def test_publish_workflow_is_official_repo_only() -> None:
    text = (ROOT / ".github" / "workflows" / "publish.yml").read_text(
        encoding="utf-8"
    )
    assert f"github.repository == '{OFFICIAL_REPO}'" in text
    assert "npm publish" in text
    assert "persist-credentials: false" in text
    assert "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803" in text
    assert "actions/setup-node@249970729cb0ef3589644e2896645e5dc5ba9c38" in text
    assert "uses: actions/checkout@v6" not in text
    assert "uses: actions/setup-node@v6" not in text
    assert "npm@latest" not in text
    assert "npm@12.0.2" in text
    workflow_perms, _, rest = text.partition("jobs:")
    assert "id-token: write" not in workflow_perms
    assert "id-token: write" in rest


def test_security_and_contributing_name_the_fork() -> None:
    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert FORK_REPO in security
    assert FORK_REPO in contributing
    assert "FORK.md" in security
    assert "FORK.md" in contributing
    assert "tools\\dev_check.ps1" in contributing
    assert f"{OFFICIAL_REPO}/security/advisories/new" in security


def test_gitignore_covers_overlay_and_secrets() -> None:
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env*" in text
    assert ".venv/" in text
    assert "node_modules/" in text
    assert "cookies.txt" in text
    assert "cookies.json" in text
    assert "credentials.json" in text
    assert "*.pem" in text
    assert ".artifactcafe/" in text


def test_agents_md_is_a_regular_file() -> None:
    agents = ROOT / "AGENTS.md"
    assert agents.is_file()
    assert not agents.is_symlink()


def test_fork_workflows_use_python_314() -> None:
    for name in ("fork-maintenance.yml", "upstream-check.yml"):
        text = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
        assert 'python-version: "3.14"' in text, name


def test_issue_templates_point_to_upstream_product() -> None:
    config = (ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text(
        encoding="utf-8"
    )
    assert OFFICIAL_REPO in config
    assert "blank_issues_enabled: false" in config
    assert f"{FORK_REPO}/blob/main/CONTRIBUTING.md" in config


def test_docs_screenshots_stay_in_upstream_docs() -> None:
    docs = ROOT / "docs"
    assert (docs / "shoply.png").is_file()
    assert (docs / "meridian.png").is_file()
    assert (docs / "focus-mode.png").is_file()
    assert (docs / "fork" / "DEVELOPMENT.md").is_file()


def test_example_canvas_matches_fresh_build(tmp_path: Path) -> None:
    out = tmp_path / "index.html"
    subprocess.run(
        [
            "node",
            str(ROOT / "scripts" / "build.js"),
            "--scene",
            str(ROOT / "examples" / "shoply-scene.js"),
            "--out",
            str(out),
            "--title",
            "Shoply — platform architecture",
            "--kicker",
            "SHOPLY — PLATFORM ARCHITECTURE",
            "--sub",
            "<b>browse</b> → <b>price</b> → <b>order</b> → <b>fulfil</b> → <b>learn</b>",
            "--slug",
            "shoply-architecture",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    tracked = (ROOT / "examples" / "shoply-canvas.html").read_bytes()
    assert out.read_bytes() == tracked


def test_overlay_python_does_not_shell_out_unsafely() -> None:
    forbidden = ("os.system", "shell=True", "eval(", "exec(", "pickle")
    for path in sorted((ROOT / "tools").glob("*.py")):
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in text, f"{path.name} contains {token}"


def test_fork_maintenance_watches_cursor_rules() -> None:
    text = (ROOT / ".github" / "workflows" / "fork-maintenance.yml").read_text(
        encoding="utf-8"
    )
    assert ".cursor/**" in text


def test_no_tracked_git_symlinks() -> None:
    result = subprocess.run(
        ["git", "ls-files", "-s"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    for line in result.stdout.splitlines():
        mode = line.split(None, 1)[0]
        assert mode != "120000", line
