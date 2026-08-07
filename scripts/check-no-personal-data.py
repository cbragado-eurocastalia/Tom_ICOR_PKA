#!/usr/bin/env python3
"""check-no-personal-data.py — release gate against author data in the scaffold.

WHY THIS EXISTS
    v1.8.2 swept the author's first name out of the scaffold and the job was
    called done. v3.0.0 shipped the Cockpit, which reintroduced ~100 literal
    mentions plus a real person's health context, and nothing noticed for 48
    days because the only check that existed looked for `{{USER_NAME}}` — a
    token that was, correctly, absent the whole time. A guard whose passing
    state is reachable without the thing being true is worse than no guard.

    So this checks the actual claim: no maintainer's personal data ships.

USAGE
    python3 scripts/check-no-personal-data.py [--root .]
    exit 0 = clean, exit 1 = findings (prints file:line for each)

ADDING A NAME
    Put it in FORBIDDEN_NAMES. If a legitimate use exists (an authorship
    credit, a historical figure, seeded sample content), add the exact
    surrounding string to ALLOWED — never widen the pattern itself.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Standalone words that must not appear: maintainers' personal names.
FORBIDDEN_NAMES = ["Tom", "Rödl", "Roedl"]

# Personal-medical and insurance markers. General clinical vocabulary is fine
# (BMI, VO2max, SpO2); what is banned is anything that describes a SPECIFIC
# person's care: a scheme they are insured under, a referral they owe, an age.
FORBIDDEN_PATTERNS = [
    (r"\bPKV\b", "private health-insurance scheme"),
    (r"\bGKV\b", "statutory health-insurance scheme"),
    (r"\bHNO\b", "ENT referral (German)"),
    (r"\bDivertikulitis\b", "named medical condition"),
    (r"\bSchlafapnoe\b", "named medical condition"),
    (r"\b\d{2}yo\b", "a specific person's age"),
    (r"appointment \(overdue\)", "a specific person's outstanding referral"),
    (r"\bdeadline \d{2}\.\d{2}\.", "a personal dated deadline"),
]

# Exact strings that are legitimate and must not trip the guard.
ALLOWED = [
    "Dr. Thomas Rödl",          # formal authorship credit (README, WAY-FORWARD)
    '"the author builds the system" → "Dr. Thomas Rödl builds the system"',
]

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "__pycache__"}
SKIP_SUFFIX = {".woff2", ".woff", ".ttf", ".png", ".jpg", ".jpeg", ".ico",
               ".pdf", ".zip", ".db", ".sqlite", ".sqlite3", ".lock"}
# This file necessarily names what it forbids.
SKIP_FILES = {"check-no-personal-data.py"}

# CASE-INSENSITIVE, deliberately. The first version of this file was case
# sensitive and reported clean on a tree that still contained `tom-roedl` in a
# slug example and `TOM'S` in a SQL comment. A name is the same name in a slug,
# a shout and a sentence.
NAME_RE = re.compile(r"\b(" + "|".join(re.escape(n) for n in FORBIDDEN_NAMES) + r")\b", re.I)
PAT_RES = [(re.compile(p, re.I), why) for p, why in FORBIDDEN_PATTERNS]


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIX or path.name in SKIP_FILES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(root)
        for lineno, line in enumerate(text.splitlines(), 1):
            probe = line
            for ok in ALLOWED:
                probe = probe.replace(ok, "")
            m = NAME_RE.search(probe)
            if m:
                findings.append(f"{rel}:{lineno}: personal name {m.group(1)!r} — {line.strip()[:96]}")
            for rx, why in PAT_RES:
                pm = rx.search(probe)
                if pm:
                    findings.append(f"{rel}:{lineno}: {why} ({pm.group(0)!r}) — {line.strip()[:96]}")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    findings = scan(root)
    if not findings:
        print("check-no-personal-data: clean — no maintainer personal data found.")
        return 0
    print(f"check-no-personal-data: {len(findings)} finding(s)\n", file=sys.stderr)
    for f in findings:
        print("  " + f, file=sys.stderr)
    print(
        "\nThe scaffold is shipped to strangers and installed with a name-substitution\n"
        "pass. Anything above renders on a member's screen as if it were theirs.\n"
        "Remove it, or add a precise exception to ALLOWED in this script.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
