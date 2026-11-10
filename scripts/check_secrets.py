#!/usr/bin/env python3
"""Limited, offline publication check; not a comprehensive secret detector.

Scan tracked and non-ignored untracked files. Report locations, never values.
Review the publication manifest too: ignored files are intentionally excluded.
"""

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
RULES = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"),
    "aws-access-key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "github-token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b"),
    "openai-style-key": re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}\b"),
    "slack-token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "credential-url": re.compile(r"https?://[^\s/:]+:[^\s/@]+@"),
    "literal-credential": re.compile(
        r'''(?i)\b(?:api_key|secret_key|access_token|password)\s*[:=]\s*["'][A-Za-z0-9_+/=-]{16,}["']'''),
}


def findings(text):
    for name, rule in RULES.items():
        for match in rule.finditer(text):
            yield name, text.count("\n", 0, match.start()) + 1


def main():
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT, capture_output=True, check=True,
    )
    paths = sorted(set(result.stdout.decode().split("\0")) - {""})
    errors = []
    for name in paths:
        path = ROOT / name
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
            errors.append(f"{name}: symlink/outside repository; inspect before publication")
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            errors.append(f"{name}: unreadable/non-text file; manual review required")
            continue
        errors.extend(f"{name}:{line}: {rule}" for rule, line in findings(body))
    if errors:
        print("FAIL publication scan (matched values are not printed):")
        print("\n".join(errors))
        return 1
    print(f"PASS limited secret-pattern scan: {len(paths)} files, {len(RULES)} rules, no matches")
    print("Scope: current tracked and non-ignored untracked files; excludes Git history and ignored files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
