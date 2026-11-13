"""Tests for bin/jig. Standard library only."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_loader = importlib.machinery.SourceFileLoader("jig", str(ROOT / "bin" / "jig"))
_spec = importlib.util.spec_from_loader("jig", _loader)
jig = importlib.util.module_from_spec(_spec)
sys.modules["jig"] = jig
_loader.exec_module(jig)

def _can_symlink() -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        try:
            os.symlink(tmp, os.path.join(tmp, "probe"))
        except (OSError, NotImplementedError):
            return False
    return True


SYMLINKS = _can_symlink()


def run(*argv: str) -> tuple[int, str]:
    out = io.StringIO()
    code = 0
    with redirect_stdout(out), redirect_stderr(io.StringIO()):
        try:
            jig.main(list(argv))
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 1
    return code, out.getvalue()


class Frontmatter(unittest.TestCase):
    def test_parses_nested_metadata(self):
        meta, body = jig.parse_frontmatter(
            '---\nname: x\nmetadata:\n  version: "1.0.0"\n---\n# Body\n'
        )
        self.assertEqual(meta["name"], "x")
        self.assertEqual(meta["metadata"]["version"], "1.0.0")
        self.assertTrue(body.startswith("# Body"))

    def test_rejects_missing_frontmatter(self):
        with self.assertRaises(ValueError):
            jig.parse_frontmatter("# no frontmatter")

    def test_rejects_unterminated(self):
        with self.assertRaises(ValueError):
            jig.parse_frontmatter("---\nname: x\n")


class Catalog(unittest.TestCase):
    def test_repo_is_valid(self):
        code, out = run("check")
        self.assertEqual(code, 0, out)

    def test_every_distributed_skill_has_eval(self):
        for skill in jig.require_skills():
            if skill.distributed:
                self.assertTrue((ROOT / "evals" / f"{skill.name}.yaml").is_file(), skill.name)

    def test_validate_flags_bad_description(self):
        skill = next(s for s in jig.require_skills() if s.name == "new-project")
        bad = jig.Skill(
            name=skill.name,
            description="Scaffold things",
            directory=skill.directory,
            skill_md=skill.skill_md,
            meta=skill.meta,
            body=skill.body,
        )
        errors = jig.validate_skill(bad)
        self.assertTrue(any("third-person" in e for e in errors))
        self.assertTrue(any("Use when" in e for e in errors))

    def test_list_json(self):
        code, out = run("list", "--json")
        self.assertEqual(code, 0)
        self.assertIn('"name": "new-project"', out)


@unittest.skipUnless(SYMLINKS, "symlinks unavailable")
class Linking(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name) / "app"
        self.project.mkdir()

    def distributed(self) -> list[str]:
        return [s.name for s in jig.require_skills() if s.distributed]

    def test_link_is_idempotent_and_healthy(self):
        self.assertEqual(run("link", str(self.project))[0], 0)
        _, second = run("link", str(self.project))
        self.assertFalse([l for l in second.splitlines() if l.startswith("linked")])
        self.assertEqual(run("doctor", str(self.project))[0], 0)
        for name in self.distributed():
            self.assertTrue((self.project / ".claude" / "skills" / name / "SKILL.md").is_file())

    def test_dry_run_writes_nothing(self):
        run("link", str(self.project), "--dry-run")
        self.assertFalse((self.project / ".agents").exists())

    def test_doctor_flags_removed_link_and_link_heals(self):
        run("link", str(self.project))
        name = self.distributed()[0]
        (self.project / ".agents" / "skills" / name).unlink()
        code, out = run("doctor", str(self.project))
        self.assertEqual(code, 1)
        self.assertIn(name, out)
        run("link", str(self.project))
        self.assertEqual(run("doctor", str(self.project))[0], 0)

    def test_unlink_removes_only_jig_links(self):
        run("link", str(self.project))
        mine = self.project / ".agents" / "skills" / "mine"
        mine.mkdir()
        (mine / "SKILL.md").write_text("x", encoding="utf-8")
        run("unlink", str(self.project))
        self.assertTrue(mine.is_dir())
        for name in self.distributed():
            self.assertFalse((self.project / ".agents" / "skills" / name).exists())


class Scaffold(unittest.TestCase):
    def test_new_creates_skill_and_eval_and_refuses_duplicates(self):
        skill_dir = ROOT / ".agents" / "skills" / "zz-demo"
        eval_file = ROOT / "evals" / "zz-demo.yaml"
        self.addCleanup(lambda: eval_file.unlink(missing_ok=True))
        self.addCleanup(
            lambda: __import__("shutil").rmtree(skill_dir, ignore_errors=True)
        )
        code, _ = run("new", "zz-demo", "--category", "dev")
        self.assertEqual(code, 0)
        self.assertTrue((skill_dir / "SKILL.md").is_file())
        self.assertIn("zz-demo", eval_file.read_text(encoding="utf-8"))
        self.assertEqual(run("new", "zz-demo", "--category", "dev")[0], 1)


if __name__ == "__main__":
    unittest.main()
