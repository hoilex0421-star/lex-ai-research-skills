#!/usr/bin/env python3
"""Fetch the pinned public template; never silently accept a changed upstream file."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

MANIFEST = Path(__file__).resolve().parents[1] / 'assets/official-template.json'


def verify(path):
    expected = json.loads(MANIFEST.read_text())['sha256']
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f'Template SHA256 mismatch: expected {expected}, got {actual}')
    return actual


def fetch(destination):
    destination = Path(destination)
    if destination.exists():
        verify(destination)
        return destination
    spec = json.loads(MANIFEST.read_text())
    with urlopen(Request(spec['download_url'], headers={'User-Agent': 'Mozilla/5.0'}), timeout=60) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != spec['sha256']:
        raise ValueError('Upstream template changed; inspect it and review the manifest before use.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    print(fetch(args.destination))
