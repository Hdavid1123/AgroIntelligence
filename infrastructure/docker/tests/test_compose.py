import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def run_compose(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )


class ComposeConfigTest(unittest.TestCase):
    def test_compose_es_valido(self) -> None:
        result = run_compose("config")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
