"""Tests for scripts/audit_conventions.py. Run: python3 -m unittest discover -s tests"""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "flutter-getx-architecture" / "scripts" / "audit_conventions.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def audit(name):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(FIXTURES / name)],
        capture_output=True, text=True,
    )
    return result.returncode, result.stdout


class AuditTests(unittest.TestCase):
    def test_clean_project_has_no_findings(self):
        code, out = audit("clean")
        self.assertEqual(code, 0, out)
        self.assertIn("0 error(s), 0 warning(s)", out)

    def test_broken_project_fails(self):
        code, _ = audit("broken")
        self.assertEqual(code, 1)

    def test_broken_project_reports_every_planted_violation(self):
        _, out = audit("broken")
        for rule in (
            "async-oninit", "no-print", "http-outside-network", "no-setstate",
            "api-in-ui", "route-unregistered", "route-string",
            "translation-missing", "screen-ui-missing", "commented-code",
            "hardcoded-string", "dispose",
        ):
            self.assertIn(f"[{rule}]", out, f"missing rule: {rule}")

    def test_not_a_flutter_project_exits_2(self):
        code, _ = audit("does-not-exist")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
