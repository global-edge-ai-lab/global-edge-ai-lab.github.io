"""Validate the static Pages artifact using only the Python standard library."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / 'website'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.tags = [], [], []
        self.source = path.read_text()
        self.feed(self.source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for name in ('href', 'src', 'poster'):
            if attrs.get(name):
                self.links.append(attrs[name])


pages = {path: Page(path) for path in ROOT.glob('*.html')}
errors = []
assert ROOT.joinpath('index.html').is_file(), 'Missing website/index.html'
for path, page in pages.items():
    label = path.name
    for identifier, count in Counter(page.ids).items():
        if count > 1:
            errors.append(f'{label}: duplicate id {identifier}')
    for required in ('title',):
        if not any(tag == required for tag, _ in page.tags):
            errors.append(f'{label}: missing {required}')
    for name in ('description', 'viewport'):
        if not any(tag == 'meta' and attrs.get('name') == name and attrs.get('content')
                   for tag, attrs in page.tags):
            errors.append(f'{label}: missing {name} metadata')
    links = page.links + re.findall(r'url\([\s\'\"]*([^\)\'\"\s]+)', page.source)
    for link in links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            if url.scheme == 'http':
                errors.append(f'{label}: insecure HTTP resource {link}')
            continue
        target = (ROOT / unquote(url.path).lstrip('/') if url.path.startswith('/')
                  else path.parent / unquote(url.path)) if url.path else path
        target = target.resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.exists():
            errors.append(f'{label}: missing or unsafe local resource {link}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{label}: missing anchor {link}')
for error in errors:
    print(error, file=sys.stderr)
if errors:
    sys.exit(1)
print(f'PASS: {len(pages)} pages; local links, anchors, CSS assets, IDs and metadata verified.')
