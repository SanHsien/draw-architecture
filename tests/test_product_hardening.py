from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "examples" / "shoply-scene.js"


def _run_node(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["node", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def test_build_escapes_title_and_kicker(tmp_path: Path) -> None:
    out = tmp_path / "index.html"
    result = _run_node(
        [
            str(ROOT / "scripts" / "build.js"),
            "--scene",
            str(SCENE),
            "--out",
            str(out),
            "--title",
            '<script>x</script>',
            "--kicker",
            'A&B',
            "--sub",
            "<b>ok</b>",
            "--slug",
            "safe-slug",
        ]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    html = out.read_text(encoding="utf-8")
    assert "<title>&lt;script&gt;x&lt;/script&gt;</title>" in html
    assert "A&amp;B" in html
    assert "<b>ok</b>" in html
    assert "<title><script>x</script></title>" not in html


def test_build_escapes_slug_for_js_string(tmp_path: Path) -> None:
    out = tmp_path / "index.html"
    result = _run_node(
        [
            str(ROOT / "scripts" / "build.js"),
            "--scene",
            str(SCENE),
            "--out",
            str(out),
            "--title",
            "Safe",
            "--slug",
            "o'reilly-arch",
        ]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    html = out.read_text(encoding="utf-8")
    assert "a.download = 'o\\'reilly-arch@2x.png';" in html
    assert "o'reilly-arch@2x.png" not in html


def test_build_and_validate_reject_script_breakout(tmp_path: Path) -> None:
    poisoned = tmp_path / "scene.js"
    poisoned.write_text(
        SCENE.read_text(encoding="utf-8") + '\nconst x = "</script><script>alert(1)</script>";\n',
        encoding="utf-8",
    )
    validated = _run_node(
        [str(ROOT / "scripts" / "validate.js"), str(poisoned)]
    )
    assert validated.returncode == 1
    assert "</script>" in validated.stderr

    built = _run_node(
        [
            str(ROOT / "scripts" / "build.js"),
            "--scene",
            str(poisoned),
            "--out",
            str(tmp_path / "out.html"),
            "--title",
            "Poison",
        ]
    )
    assert built.returncode == 1
    assert "</script>" in built.stderr
    assert not (tmp_path / "out.html").exists()


def test_shoply_scene_still_validates_after_breakout_guard() -> None:
    result = _run_node(
        [str(ROOT / "scripts" / "validate.js"), str(SCENE)]
    )
    assert result.returncode == 0, result.stdout + result.stderr
