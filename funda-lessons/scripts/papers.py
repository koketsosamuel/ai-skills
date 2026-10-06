#!/usr/bin/env python3
"""Find past papers, memos and exam guidelines in the owner's local library and pull them out as text.

The library (~/Documents/past papers) is indexed by papers-tracker.json. Some files live inside
zips (path "a.zip!/inner.pdf"), so --pull extracts to a working folder instead of reading in place.

  papers.py list  "Physical Sciences" 12 [--from 2022] [--lang English] [--source DBE]
  papers.py guide "Physical Sciences"                     # exam guideline documents
  papers.py pull  "Physical Sciences" 12 --from 2023 --out <scratchpad>/papers
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile

ROOT = os.environ.get('PAST_PAPERS_DIR', os.path.expanduser('~/Documents/past papers'))


def load():
    with open(os.path.join(ROOT, 'papers-tracker.json')) as f:
        data = json.load(f)
    return data['papers'], {d['id']: d for d in data['documents']}


def matches(value, wanted):
    return wanted is None or wanted.lower() in (value or '').lower()


def select(papers, a):
    rows = [
        p for p in papers
        if matches(p['subject'], a.subject)
        and p['grade'] == a.grade
        and p['year'] >= a.year_from
        and matches(p['language'], a.lang)
        and matches(p['source'], a.source)
        and p['question_paper']
    ]
    return sorted(rows, key=lambda p: (-p['year'], p['sitting'], p['paper'] or 0))


def materialise(path, out):
    """Copies a library file (or a zip member) into out and returns the local path."""
    os.makedirs(out, exist_ok=True)
    if '!/' in path:
        archive, member = path.split('!/', 1)
        target = os.path.join(out, os.path.basename(member))
        with zipfile.ZipFile(os.path.join(ROOT, archive)) as z, z.open(member) as src, open(target, 'wb') as dst:
            shutil.copyfileobj(src, dst)
        return target
    target = os.path.join(out, os.path.basename(path))
    shutil.copyfile(os.path.join(ROOT, path), target)
    return target


def to_text(pdf):
    if not pdf.lower().endswith('.pdf'):
        return None
    txt = pdf[:-4] + '.txt'
    subprocess.run(['pdftotext', '-layout', pdf, txt], check=False)
    return txt if os.path.exists(txt) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['list', 'guide', 'pull'])
    ap.add_argument('subject')
    ap.add_argument('grade', type=int, nargs='?')
    ap.add_argument('--from', dest='year_from', type=int, default=0)
    ap.add_argument('--lang', default='English')
    ap.add_argument('--source')
    ap.add_argument('--out')
    a = ap.parse_args()
    papers, docs = load()

    if a.cmd == 'guide':
        for d in docs.values():
            if matches(d['path'], 'exam guide') and matches(d['path'], a.subject) and not matches(d['path'], ' afr'):
                print(d['path'])
        return

    if a.grade is None:
        sys.exit('grade is required for list and pull')
    rows = select(papers, a)
    for p in rows:
        qp = docs[p['question_paper']]['path']
        memo = docs[p['memo']]['path'] if p.get('memo') else None
        extras = [docs[e]['path'] for e in p.get('extras', []) if e in docs]
        if a.cmd == 'list':
            print(f"{p['title']} [{p['source']}]\n  paper: {qp}\n  memo:  {memo or '(none)'}")
            for e in extras:
                print(f'  extra: {e}')
            continue
        if not a.out:
            sys.exit('pull needs --out <folder in the scratchpad>')
        folder = os.path.join(a.out, f"{p['year']}-{p['sitting'].replace('/', '-')}-P{p['paper']}-{p['source'].split()[0]}")
        for path in [qp, memo, *extras]:
            if path:
                local = materialise(path, folder)
                print(to_text(local) or local)


if __name__ == '__main__':
    main()
