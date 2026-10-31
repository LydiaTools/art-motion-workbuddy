#!/usr/bin/env python3
"""Prepare the pinned public Art Motion package in a new directory."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import sys
import tempfile
import unicodedata
import urllib.request
import zipfile

URL = "https://github.com/LydiaTools/art-motion-workbuddy/releases/download/v0.1.1/art-motion-workbuddy-v0.1.1.zip"
SHA256 = "cd688513101d3150d9c45281fc06c7fbc4199c64f27adb21f0cf27980ed462d4"
MAX_ARCHIVE = 32 * 1024 * 1024
MAX_EXPANDED = 128 * 1024 * 1024
MAX_MEMBERS = 1500
PREFIX = "art-motion-workbuddy"


def verify(archive):
    digest = hashlib.sha256()
    total = 0
    with archive.open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            total += len(block)
            if total > MAX_ARCHIVE:
                raise ValueError('Archive exceeds size limit.')
            digest.update(block)
    if digest.hexdigest() != SHA256:
        raise ValueError('Archive SHA-256 does not match the pinned release.')


def prepare(archive, target):
    verify(archive)
    target = target.expanduser().absolute()
    if not target.parent.is_dir():
        raise ValueError('Target parent directory must already exist.')
    with zipfile.ZipFile(archive) as package:
        members = package.infolist()
        if len(members) > MAX_MEMBERS or sum(i.file_size for i in members) > MAX_EXPANDED:
            raise ValueError('Archive expands beyond the allowed limit.')
        entries = []
        names = set()
        for item in members:
            name = item.filename
            if any(char in name for char in '\\:*?"<>|\x00'):
                raise ValueError('Unsupported archive path.')
            part = PurePosixPath(name)
            if part.is_absolute() or '..' in part.parts or len(part.parts) < 2 or part.parts[0] != PREFIX:
                raise ValueError('Archive entry escapes the package root.')
            mode = item.external_attr >> 16
            if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)):
                raise ValueError('Archive contains a symbolic link or special file.')
            relative = Path(*part.parts[1:])
            key = unicodedata.normalize('NFC', '/'.join(part.parts[1:])).casefold()
            if key in names:
                raise ValueError('Archive contains duplicate or case-colliding paths.')
            names.add(key)
            entries.append((item, relative))
        if 'skill.md' not in names or 'scripts/local_engine.py' not in names:
            raise ValueError('Archive is missing the skill entry or adapter.')
        # mkdir is exclusive: do not replace any user directory or follow a target link.
        target.mkdir()
        try:
            for item, relative in entries:
                output = target / relative
                if item.is_dir():
                    output.mkdir(parents=True, exist_ok=True)
                else:
                    output.parent.mkdir(parents=True, exist_ok=True)
                    with package.open(item) as source, output.open('xb') as dest:
                        shutil.copyfileobj(source, dest, 65536)
        except Exception:
            # Keep a partial target visible instead of deleting possible user data.
            raise RuntimeError(f'Extraction failed; inspect the incomplete directory: {target}')
    return {'target': str(target), 'sha256': SHA256, 'files': len(entries)}


def download(target):
    request = urllib.request.Request(URL, headers={'User-Agent': 'art-motion-workbuddy-prepare/0.1.1'})
    with urllib.request.urlopen(request, timeout=30) as response, target.open('wb') as out:
        total = 0
        while True:
            chunk = response.read(65536)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_ARCHIVE:
                raise ValueError('Download exceeds size limit.')
            out.write(chunk)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, type=Path, help='New output directory; its parent must exist.')
    parser.add_argument('--archive', type=Path, help='Use a previously downloaded matching release ZIP instead of downloading.')
    args = parser.parse_args()
    try:
        target = args.target.expanduser().absolute()
        if target.exists() or target.is_symlink():
            raise ValueError('Target already exists; choose a new directory.')
        if args.archive:
            result = prepare(args.archive.expanduser(), target)
        else:
            with tempfile.TemporaryDirectory(prefix='art-motion-zip-') as tmp:
                archive = Path(tmp) / 'package.zip'
                download(archive)
                result = prepare(archive, target)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
