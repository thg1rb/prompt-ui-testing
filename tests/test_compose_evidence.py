import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "skills/prompt-ui-testing/scripts/compose_evidence.py"
sys.path.insert(0, str(HELPER.parent))
from compose_evidence import redact_url  # noqa: E402


class RedactionTests(unittest.TestCase):
    def test_removes_credentials_query_values_and_fragment(self):
        actual = redact_url("https://user:password@example.com/callback?token=secret&state=abc#private")
        self.assertEqual(actual, "https://example.com/callback?token=[REDACTED]&state=[REDACTED]#[REDACTED]")

    def test_keeps_localhost_and_hides_opaque_path_segments(self):
        actual = redact_url("http://127.0.0.1:5173/reset/0123456789abcdef0123456789abcdef")
        self.assertEqual(actual, "http://127.0.0.1:5173/reset/[REDACTED]")

    def test_rejects_non_web_url(self):
        with self.assertRaises(ValueError):
            redact_url("about:blank")

    def test_rejects_control_characters(self):
        with self.assertRaises(ValueError):
            redact_url("https://example.com/path\nFORGED")

    def test_redacts_opaque_query_key(self):
        actual = redact_url("https://example.com/result?0123456789abcdef=private")
        self.assertEqual(actual, "https://example.com/result?[REDACTED]=[REDACTED]")


class CompositionTests(unittest.TestCase):
    def test_cli_preserves_raw_pixels_and_adds_readable_strip(self):
        with tempfile.TemporaryDirectory() as directory:
            raw_path = Path(directory) / "raw.png"
            output_path = Path(directory) / "final.png"
            Image.new("RGB", (80, 60), "#123456").save(raw_path)
            result = subprocess.run(
                [sys.executable, str(HELPER), "--input", str(raw_path), "--output", str(output_path)],
                input=json.dumps({"url": "http://localhost:3000/result?token=secret"}),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            metadata = json.loads(result.stdout)
            self.assertEqual(metadata["displayed_url"], "http://localhost:3000/result?token=[REDACTED]")
            self.assertNotIn("secret", result.stdout)
            self.assertTrue(output_path.exists())
            with Image.open(raw_path) as original, Image.open(output_path) as final:
                strip_height = final.height - original.height
                self.assertGreater(strip_height, 0)
                self.assertEqual(final.crop((0, strip_height, 80, final.height)).tobytes(), original.convert("RGB").tobytes())

    def test_refuses_to_overwrite_raw_screenshot(self):
        with tempfile.TemporaryDirectory() as directory:
            raw_path = Path(directory) / "raw.png"
            Image.new("RGB", (80, 60), "white").save(raw_path)
            before = raw_path.read_bytes()
            result = subprocess.run(
                [sys.executable, str(HELPER), "--input", str(raw_path), "--output", str(raw_path)],
                input=json.dumps({"url": "https://example.com"}),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(raw_path.read_bytes(), before)

    def test_preserves_rgba_pixels(self):
        with tempfile.TemporaryDirectory() as directory:
            raw_path = Path(directory) / "raw.png"
            output_path = Path(directory) / "final.png"
            Image.new("RGBA", (20, 10), (18, 52, 86, 128)).save(raw_path)
            result = subprocess.run(
                [sys.executable, str(HELPER), "--input", str(raw_path), "--output", str(output_path)],
                input=json.dumps({"url": "https://example.com"}),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(raw_path) as original, Image.open(output_path) as final:
                strip_height = final.height - original.height
                self.assertEqual(final.crop((0, strip_height, 20, final.height)).tobytes(), original.tobytes())


if __name__ == "__main__":
    unittest.main()
