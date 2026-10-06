#!/usr/bin/env python3
"""Secret scan for this (public) repository. Python 3.8+, standard library only.

  python tools/scan_secrets.py --staged     scan what is about to be committed (used by .githooks/pre-commit)
  python tools/scan_secrets.py [paths...]   scan the working tree (default: whole repo); CI runs this on every push

Blocks: private-key blocks, key-looking file names, cloud/GitHub/Slack tokens, unredacted password hashes.
Warns:  credential-looking assignments, very large files.
A line containing REDACTED or kb:allow is skipped (use REDACTED in sample /etc/shadow lines you publish).
Exit status 1 when anything blocking is found.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "archive", "site", "node_modules", "__pycache__"}
BLOCK = [
    ("private key block", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("unredacted shadow-style line", re.compile(r"^[a-z_][a-z0-9_.-]*:\$(?:y|7|6|5|2[abxy]?|1)\$[./A-Za-z0-9$,=]{8,}:")),
    ("password hash", re.compile(r"\$(?:y|6|5|1)\$[./A-Za-z0-9,=$]{25,}|\$2[abxy]\$\d{2}\$[./A-Za-z0-9]{40,}")),
]
WARN = [
    ("credential-looking assignment",
     re.compile(r"(?i)\b(?:password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*[\"']?[A-Za-z0-9/+_\-]{16,}")),
]
BAD_NAMES = re.compile(r"(?i)^(?:id_(?:rsa|dsa|ecdsa|ed25519)(?:_sk)?|.*\.(?:pem|key|p12|pfx|kdbx)|\.env(?:\..*)?)$")
MAX_BYTES = 5 * 1024 * 1024


def scan_text(text, name):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if "REDACTED" in line or "kb:allow" in line:
            continue
        for label, rx in BLOCK:
            if rx.search(line):
                hits.append(f"BLOCK {name}:{i}: {label}")
        for label, rx in WARN:
            if rx.search(line):
                hits.append(f"warn  {name}:{i}: {label}")
    return hits


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def scan_blob(name, blob):
    if len(blob) > MAX_BYTES:
        return [f"warn  {name}: file is over 5 MiB; large captures do not belong in the repo"]
    if b"\0" in blob[:4096]:
        return []
    return scan_text(blob.decode("utf-8", "replace"), name)


def main(argv):
    results = []
    if "--staged" in argv:
        r = git("diff", "--cached", "--name-only", "--diff-filter=ACM", "-z")
        if r.returncode != 0:
            sys.exit("not a git repository (or git failed)")
        for n in [x for x in r.stdout.decode("utf-8", "replace").split("\0") if x]:
            if Path(n).parts and Path(n).parts[0] in SKIP_DIRS:
                continue
            base = Path(n).name
            if BAD_NAMES.match(base) and not base.endswith(".pub"):
                results.append(f"BLOCK {n}: file name looks like a key or secret file")
                continue
            results += scan_blob(n, git("show", f":{n}").stdout)
    else:
        targets = [Path(a) for a in argv if not a.startswith("-")] or [ROOT]
        for t in targets:
            files = [t] if t.is_file() else [p for p in t.rglob("*") if p.is_file()]
            for p in files:
                try:
                    rel = p.resolve().relative_to(ROOT)
                except ValueError:
                    rel = p
                if set(rel.parts) & SKIP_DIRS or p.name == "scan_secrets.py":
                    continue
                if BAD_NAMES.match(p.name) and not p.name.endswith(".pub"):
                    results.append(f"BLOCK {rel}: file name looks like a key or secret file")
                    continue
                results += scan_blob(str(rel), p.read_bytes())
    for r in results:
        print(r)
    blocks = [r for r in results if r.startswith("BLOCK")]
    if blocks:
        print(f"\n{len(blocks)} blocking finding(s). Remove the secret, replace it with REDACTED, or put 'kb:allow' "
              "on a false-positive line. If it was ever pushed, rotate it: deleting a commit does not un-leak it.",
              file=sys.stderr)
        return 1
    if not results:
        print("scan clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
