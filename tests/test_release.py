from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReleaseTests(unittest.TestCase):
    def test_invalid_version_is_rejected_before_creating_output(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'output'
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/build-release.py'),
                                     '--source', temp, '--version', '../bad', '--output', str(output)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('version must look', result.stderr)
            self.assertFalse(output.exists())

    def test_output_inside_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/build-release.py'),
                                     '--source', temp, '--version', 'v0.4.8',
                                     '--output', str(Path(temp) / 'dist')],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('outside the private source', result.stderr)


if __name__ == '__main__':
    unittest.main()
