from pathlib import Path
import re
import unittest

DOCS = Path(__file__).resolve().parents[1] / 'docs'
VERSIONED = re.compile(r'releases/v\d|tqctl_v\d')


class VersionTests(unittest.TestCase):
    def test_no_link_or_file_name_carries_a_version(self):
        for page in DOCS.glob('*.md'):
            self.assertIsNone(VERSIONED.search(page.read_text()), f'{page.name} names a release')


if __name__ == '__main__':
    unittest.main()
