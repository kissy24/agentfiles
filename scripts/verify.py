#!/usr/bin/env python3
"""Check this reference distribution, not arbitrary AWF implementations.

No dependencies or network. Install examples run in temporary directories.
Behavioral compliance still requires reviewing docs/scenarios.md.
"""

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PRACTICES = ("security", "evidence", "tdd", "pre-commit", "context-management")
STATES = {"working", "verifying", "completed", "partial", "blocked",
          "approval_required", "stopped"}

# Deliberately duplicated: documentation is data, not executable authority.
# Changes to the installation procedure require reviewing this allowlist too.
APPROVED_INSTALL = '''(
  set -euC
  awf_source=$(pwd -P)
  test -d "$awf_target"
  test ! -L core
  test ! -L templates
  for awf_file in core/contract.md core/lifecycle.md templates/AGENTS.md; do
    test -f "$awf_file"
    test ! -L "$awf_file"
  done
  cd "$awf_target"
  for awf_entry in .awf AGENTS.md AGENTS.override.md; do
    if test -e "$awf_entry" || test -L "$awf_entry"; then
      echo "Existing entry; merge manually: $awf_entry" >&2
      exit 1
    fi
  done
  mkdir .awf
  mkdir .awf/core
  cat "$awf_source/core/contract.md" > .awf/core/contract.md
  cat "$awf_source/core/lifecycle.md" > .awf/core/lifecycle.md
  cat "$awf_source/templates/AGENTS.md" > AGENTS.md
)'''


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return path.read_text(encoding="utf-8")


def links(path):
    # This repo uses inline Markdown links. Ignore fenced code examples.
    body = re.sub(r"```.*?```", "", read(path), flags=re.S)
    return re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", body)


def check_links(path, base=None):
    for target in links(path):
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            continue
        resolved = (base or path.parent) / unquote(url.path)
        scope = (base or ROOT).resolve()
        require(resolved.resolve().is_relative_to(scope),
                f"Link outside allowed directory: {path.name} -> {target}")
        require(resolved.exists(), f"Broken link: {path.relative_to(ROOT)} -> {target}")


def check_distribution():
    required = [
        "README.md", "SPEC.md", "AGENTS.md", "core/contract.md",
        "core/lifecycle.md", "templates/AGENTS.md", "templates/task-status.md",
        "adapters/codex/README.md", "docs/conformance.md", "docs/scenarios.md",
        "docs/maintenance.md", "docs/task-status.md", "docs/verification.txt",
    ]
    for example in ("software-development", "research"):
        required += [f"examples/{example}/README.md", f"examples/{example}/task-status.md"]
    required += [f"practices/{name}.md" for name in PRACTICES]
    for name in required:
        path = ROOT / name
        require(path.is_file() and path.stat().st_size > 0, f"Missing/empty: {name}")

    count = 0
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts or path == ROOT / "templates/AGENTS.md":
            continue
        check_links(path)
        count += 1
    print(f"PASS distribution and local links: {count} Markdown files (template checked after install)")

    fields = ("id", "name", "version", "core_compatibility", "purpose",
              "applies_to", "preconditions", "overrides")
    for name in PRACTICES:
        body = read(ROOT / f"practices/{name}.md")
        for field in fields:
            require(re.search(rf"^- {field}: \S.+$", body, re.M), f"{name}: missing {field}")
        for heading in ("## Rules", "## Verification"):
            require(heading in body, f"{name}: missing {heading}")
    print("PASS five Practice definitions (metadata presence; semantics reviewed separately)")

    for name in ("software-development", "research"):
        path = ROOT / f"examples/{name}/README.md"
        for core in ("contract", "lifecycle"):
            target = f"../../core/{core}.md"
            require(target in links(path), f"{name}: must reference shared {core}")
            require((path.parent / target).resolve() == ROOT / f"core/{core}.md",
                    f"{name}: different Core")
    print("PASS both domains reference the identical Core files")

    status_paths = [ROOT / "docs/task-status.md"]
    for folder in ("software-development", "research"):
        status_paths += sorted((ROOT / "examples" / folder).glob("*status*.md"))
    status_paths.append(ROOT / "examples/research/handoff.md")
    for path in status_paths:
        fields = dict(re.findall(r"^- ([a-z_]+): (.+)$", read(path), re.M))
        for key in ("objective", "status", "current_focus", "decisions", "evidence",
                    "remaining", "next_action", "updated_at"):
            require(fields.get(key, "").strip(), f"{path.name}: empty {key}")
        require(fields["status"] in STATES, f"{path.name}: unknown status")
        require(not re.search(r"<[^>]+>", " ".join(fields.values())),
                f"{path.name}: unfilled placeholder")
    print(f"PASS {len(status_paths)} state records (field presence, not truth of claims)")


def install_command():
    body = read(ROOT / "adapters/codex/README.md")
    snippet = re.search(r"```sh\n(.*?)\n```", body, re.S)
    require(snippet is not None, "Missing documented install command")
    lines = snippet.group(1).splitlines()
    require(lines[0] == "awf_target='/absolute/path/to/target-project'",
            "Install command target declaration changed; review verifier")
    command = "\n".join(lines[1:])
    require(command == APPROVED_INSTALL,
            "Documented install command is not approved; review code before execution")
    return command


def run_install(command, target):
    require(command == APPROVED_INSTALL, "Refusing unapproved shell command")
    env = {"PATH": os.defpath, "LC_ALL": "C", "awf_target": str(target)}
    return subprocess.run(["sh", "-c", command], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=30)


def check_install():
    command = install_command()
    with tempfile.TemporaryDirectory(prefix="awf-install-") as temp:
        base = Path(temp)
        target = base / "project with spaces;$(touch injected)"
        target.mkdir()
        result = run_install(command, target)
        require(result.returncode == 0, f"Install failed: {result.stderr}")
        require(not (ROOT / "injected").exists(), "Target path interpreted as shell code")
        expected = ["AGENTS.md", ".awf/core/contract.md", ".awf/core/lifecycle.md"]
        actual = sorted(str(p.relative_to(target)) for p in target.rglob("*") if p.is_file())
        require(actual == sorted(expected), f"Unexpected installed files: {actual}")
        require((target / "AGENTS.md").read_bytes() == (ROOT / "templates/AGENTS.md").read_bytes(),
                "Installed entry differs")
        check_links(ROOT / "templates/AGENTS.md", base=target)
        for name in ("contract", "lifecycle"):
            installed = target / f".awf/core/{name}.md"
            require(installed.read_bytes() == (ROOT / f"core/{name}.md").read_bytes(),
                    f"Installed {name} differs")
            for link in links(installed):
                require((installed.parent / link).exists(), f"Installed broken link: {link}")
        print("PASS documented fresh install: 3 files, paths with spaces, Core unchanged, links resolve")

        original = {p: (target / p).read_bytes() for p in expected}
        require(run_install(command, target).returncode != 0, "Reinstall must stop")
        require(all((target / p).read_bytes() == data for p, data in original.items()),
                "Reinstall changed existing content")
        for name in ("AGENTS.md", "AGENTS.override.md", ".awf"):
            protected = base / ("existing-" + name)
            protected.mkdir()
            entry = protected / name
            entry.write_text("keep existing content\n", encoding="utf-8")
            result = run_install(command, protected)
            require(result.returncode != 0, f"Must stop on existing {name}")
            require(entry.read_text() == "keep existing content\n", f"Overwrote {name}")
            require(list(protected.iterdir()) == [entry], f"Partial install on existing {name}")
        dangling = base / "dangling"
        dangling.mkdir()
        (dangling / "AGENTS.md").symlink_to("missing-target")
        require(run_install(command, dangling).returncode != 0, "Must stop on dangling entry")
        require((dangling / "AGENTS.md").is_symlink(), "Changed existing symlink")
        require(not (dangling / ".awf").exists(), "Partial install on dangling entry")
        print("PASS existing AGENTS/override/.awf and dangling entry preserved; reinstall refused")


def check_example():
    example = ROOT / "examples/software-development"
    with tempfile.TemporaryDirectory(prefix="awf-tests-") as temp:
        target = Path(temp)
        for label, source in (("RED", example / "before/expiry.py"),
                              ("GREEN", example / "expiry.py")):
            case = target / label
            case.mkdir()
            shutil.copyfile(source, case / "expiry.py")
            shutil.copyfile(example / "test_expiry.py", case / "test_expiry.py")
            result = subprocess.run(
                [sys.executable, "-I", "-B", "-m", "unittest", "discover", "-s", ".", "-v"],
                cwd=case, capture_output=True, text=True, timeout=30,
                env={"PATH": os.defpath, "LC_ALL": "C"},
            )
            output = result.stdout + result.stderr
            print(f"\n{label}: identical boundary tests against {source.relative_to(ROOT)}")
            sanitized = output.rstrip()
            for directory in sorted({str(target), str(target.resolve())}, key=len, reverse=True):
                sanitized = sanitized.replace(directory, "<temporary-directory>")
            print(sanitized)
            require("Ran 3 tests" in output, f"{label}: expected three tests")
            if label == "RED":
                require(result.returncode != 0 and "FAIL: test_at_expiry" in output
                        and "FAILED (failures=1)" in output, "Bug was not reproduced as expected")
            else:
                require(result.returncode == 0, "Fixed implementation failed")
    print("\nPASS boundary regression: old code fails at equality; fixed code passes all 3")


def main():
    print("AWF reference distribution verification")
    print("Time:", datetime.now(timezone.utc).isoformat())
    print("Python:", sys.version.split()[0])
    try:
        check_distribution()
        check_install()
        check_example()
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS all executable checks. This is not a runtime enforcement or model compliance test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
