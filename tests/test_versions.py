from pathlib import Path
import re
import unittest

DOCS = Path(__file__).resolve().parents[1] / 'docs'
VERSION = re.compile(r'\bv\d+\.\d+\.\d+\b')


class VersionTests(unittest.TestCase):
    def test_every_page_names_the_same_release(self):
        found = {v for page in DOCS.glob('*.md') for v in VERSION.findall(page.read_text())}
        self.assertEqual(len(found), 1, f'docs name more than one release: {sorted(found)}')


if __name__ == '__main__':
    unittest.main()
