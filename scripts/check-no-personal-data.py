#!/usr/bin/env python3
"""check-no-personal-data.py — release gate against maintainer data in the scaffold.

WHY THIS EXISTS
    v1.8.2 swept the author's first name out of the scaffold and the job was
    called done. v3.0.0 shipped the Cockpit, which reintroduced ~100 literal
    mentions plus a real person's health context, and nothing noticed for 48
    days because the only check that existed looked for `{{USER_NAME}}` — a
    token that was, correctly, absent the whole time. A guard whose passing
    state is reachable without the thing being true is worse than no guard.

    So this checks the actual claim: no maintainer's personal data ships.

WHY THE NAMES ARE NOT IN THIS FILE
    This script ships inside the scaffold. Hardcoding a maintainer's name here
    would put that name in every member's folder, which is precisely what the
    guard exists to prevent. Names live in a config file that is NOT shipped
    (`.privacy-guard.json`, marked export-ignore in .gitattributes).

CONFIG  (.privacy-guard.json at the repo root, optional)
    {
      "forbidden_names": ["Ada", "Lovelace"],
      "allowed": ["Dr. Ada Lovelace"]
    }
    `allowed` holds EXACT strings that are legitimate (a formal authorship
    credit, a historical figure quoted in sample content). Add an exact string
    rather than widening a pattern.

USAGE
    python3 scripts/check-no-personal-data.py [--root .] [--require-config]
    exit 0 = clean, exit 1 = findings (prints file:line for each)

    --require-config makes a missing or name-less config a FAILURE. CI uses it,
    so this gate can never quietly degrade to patterns-only and report green.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CONFIG_NAME = ".privacy-guard.json"

# Personal-medical and insurance markers. General clinical vocabulary is fine
# (BMI, VO2max, SpO2); what is banned is anything describing a SPECIFIC
# person's care: a scheme they are insured under, a referral they owe, an age.
# These are generic and apply to any maintainer, so they live in the script.
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

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "__pycache__"}
SKIP_SUFFIX = {".woff2", ".woff", ".ttf", ".png", ".jpg", ".jpeg", ".ico",
               ".pdf", ".zip", ".db", ".sqlite", ".sqlite3", ".lock"}
SKIP_FILES = {"check-no-personal-data.py", CONFIG_NAME}


def load_config(root: Path) -> tuple[list[str], list[str], bool]:
    p = root / CONFIG_NAME
    if not p.is_file():
        return [], [], False
    try:
        cfg = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"{CONFIG_NAME} is unreadable: {exc}", file=sys.stderr)
        return [], [], False
    names = [str(n) for n in cfg.get("forbidden_names", []) if str(n).strip()]
    allowed = [str(a) for a in cfg.get("allowed", []) if str(a).strip()]
    return names, allowed, True


def scan(root: Path, names: list[str], allowed: list[str]) -> list[str]:
    # CASE-INSENSITIVE, deliberately. The first version of this file was case
    # sensitive and reported clean on a tree that still held a lowercase name
    # inside a slug example and an upper-case one in a SQL comment. A name is
    # the same name in a slug, a shout and a sentence.
    name_re = (re.compile(r"\b(" + "|".join(re.escape(n) for n in names) + r")\b", re.I)
               if names else None)
    pat_res = [(re.compile(p, re.I), why) for p, why in FORBIDDEN_PATTERNS]

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
            for ok in allowed:
                probe = probe.replace(ok, "")
            if name_re:
                m = name_re.search(probe)
                if m:
                    findings.append(f"{rel}:{lineno}: personal name {m.group(1)!r} — {line.strip()[:96]}")
            for rx, why in pat_res:
                pm = rx.search(probe)
                if pm:
                    findings.append(f"{rel}:{lineno}: {why} ({pm.group(0)!r}) — {line.strip()[:96]}")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--require-config", action="store_true",
                    help="fail if no config with at least one name is present")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    names, allowed, had_config = load_config(root)

    if args.require_config and not names:
        print(
            f"check-no-personal-data: REFUSING TO PASS.\n"
            f"  --require-config was given but {CONFIG_NAME} is "
            f"{'missing' if not had_config else 'present with no forbidden_names'}.\n"
            f"  Without a name list this gate only checks generic health patterns, and\n"
            f"  reporting green would claim more than it verified.",
            file=sys.stderr)
        return 1

    findings = scan(root, names, allowed)

    if not names:
        print("check-no-personal-data: NO NAME LIST CONFIGURED — generic health "
              f"patterns only. Add {CONFIG_NAME} to check maintainer names too.",
              file=sys.stderr)

    if not findings:
        scope = f"{len(names)} name(s) + {len(FORBIDDEN_PATTERNS)} patterns" if names \
            else f"{len(FORBIDDEN_PATTERNS)} patterns"
        print(f"check-no-personal-data: clean — nothing found ({scope} checked).")
        return 0

    print(f"check-no-personal-data: {len(findings)} finding(s)\n", file=sys.stderr)
    for f in findings:
        print("  " + f, file=sys.stderr)
    print(
        "\nThe scaffold is shipped to strangers and installed with a name-substitution\n"
        "pass. Anything above renders on a member's screen as if it were theirs.\n"
        f"Remove it, or add an exact exception to \"allowed\" in {CONFIG_NAME}.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
