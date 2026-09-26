from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_git_metadata_privacy.py"
SAFE_EMAIL = "12345+sample-user@users.noreply.github.com"
GITHUB_WEB_EMAIL = "noreply@github.com"
PRIVATE_EMAIL = "private.person@example.net"


class GitMetadataPrivacyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.git("config", "user.name", "Sample User")
        self.git("config", "user.email", SAFE_EMAIL)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def git(self, *args: str, env: dict[str, str] | None = None) -> None:
        subprocess.run(["git", *args], cwd=self.repo, env=env, check=True, capture_output=True)

    def make_commit(self, author_email: str = SAFE_EMAIL, committer_email: str = SAFE_EMAIL) -> None:
        (self.repo / "sample.txt").write_text("sample\n", encoding="utf-8")
        self.git("add", "sample.txt")
        env = os.environ.copy()
        env.update(
            {
                "GIT_AUTHOR_NAME": "Sample User",
                "GIT_AUTHOR_EMAIL": author_email,
                "GIT_COMMITTER_NAME": "Sample User",
                "GIT_COMMITTER_EMAIL": committer_email,
            }
        )
        self.git("commit", "-m", "Add sample", env=env)

    def run_check(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT)], cwd=self.repo, text=True, capture_output=True, check=False
        )

    def test_accepts_github_noreply_commit_and_annotated_tag(self) -> None:
        self.make_commit()
        env = os.environ.copy()
        env.update({"GIT_COMMITTER_NAME": "Sample User", "GIT_COMMITTER_EMAIL": SAFE_EMAIL})
        self.git("tag", "-a", "v0.1.0", "-m", "Sample tag", env=env)

        result = self.run_check()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS:", result.stdout)

    def test_accepts_github_web_merge_committer_identity(self) -> None:
        self.make_commit(committer_email=GITHUB_WEB_EMAIL)

        result = self.run_check()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS:", result.stdout)

    def test_rejects_other_github_com_identity(self) -> None:
        self.make_commit(committer_email="other@github.com")

        result = self.run_check()

        self.assertEqual(result.returncode, 1)
        self.assertIn("committer email is not allowlisted", result.stdout)

    def test_rejects_author_and_committer_email_without_printing_address(self) -> None:
        self.make_commit(PRIVATE_EMAIL, PRIVATE_EMAIL)

        result = self.run_check()

        self.assertEqual(result.returncode, 1)
        self.assertIn("author email is not allowlisted", result.stdout)
        self.assertIn("committer email is not allowlisted", result.stdout)
        self.assertNotIn(PRIVATE_EMAIL, result.stdout + result.stderr)

    def test_rejects_annotated_tag_tagger_email_without_printing_address(self) -> None:
        self.make_commit()
        env = os.environ.copy()
        env.update({"GIT_COMMITTER_NAME": "Sample User", "GIT_COMMITTER_EMAIL": PRIVATE_EMAIL})
        self.git("tag", "-a", "bad-tag", "-m", "Sample tag", env=env)

        result = self.run_check()

        self.assertEqual(result.returncode, 1)
        self.assertIn("tag refs/tags/bad-tag: tagger email is not allowlisted", result.stdout)
        self.assertNotIn(PRIVATE_EMAIL, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
