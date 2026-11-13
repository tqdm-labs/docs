from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'site'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])


class SiteTests(unittest.TestCase):
    def test_internal_links_and_anchors(self):
        self.assertTrue((ROOT / 'index.html').exists(), 'build the site first')
        pages = {path.resolve(): Page(path) for path in ROOT.rglob('*.html')}
        for source, page in pages.items():
            for link in page.links:
                url = urlsplit(link)
                if url.scheme or url.netloc:
                    continue
                target = ((ROOT / unquote(url.path).lstrip('/')) if url.path.startswith('/')
                          else source.parent / unquote(url.path)) if url.path else source
                if target.is_dir():
                    target /= 'index.html'
                target = target.resolve()
                with self.subTest(source=source.relative_to(ROOT), link=link):
                    self.assertTrue(target.exists(), f'missing target {target}')
                    if url.fragment and target in pages:
                        self.assertIn(unquote(url.fragment), pages[target].ids)


if __name__ == '__main__':
    unittest.main()
