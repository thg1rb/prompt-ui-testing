#!/usr/bin/env python3
"""Reject reachable Git identities outside the public GitHub noreply domain."""

from __future__ import annotations

import re
import subprocess
import sys


ALLOWED_EMAIL_DOMAIN = "users.noreply.github.com"
IDENTITY_RE = re.compile(rb"^(author|committer|tagger) .* <([^>]+)>")


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], stderr=subprocess.PIPE)


def permitted(email: bytes) -> bool:
    try:
        value = email.decode("ascii").lower()
    except UnicodeDecodeError:
        return False
    return value.count("@") == 1 and bool(value.partition("@")[0]) and value.endswith(
        "@" + ALLOWED_EMAIL_DOMAIN
    )


def reachable_commits() -> list[str]:
    output = git("rev-list", "--all")
    return sorted(set(output.decode("ascii").splitlines()))


def referenced_tags() -> list[tuple[str, str]]:
    output = git("for-each-ref", "--format=%(refname)%09%(objectname)")
    return [tuple(line.split("\t", 1)) for line in output.decode("ascii").splitlines()]


def identity_violations() -> tuple[int, int, list[str]]:
    commits = reachable_commits()
    violations: list[str] = []

    for commit in commits:
        raw = git("cat-file", "commit", commit)
        headers = raw.split(b"\n\n", 1)[0].splitlines()
        for header in headers:
            match = IDENTITY_RE.match(header)
            if match and match.group(1) in (b"author", b"committer"):
                if not permitted(match.group(2)):
                    violations.append(f"commit {commit[:12]}: {match.group(1).decode()} email is not allowlisted")

    seen_tags: set[str] = set()
    for ref, start_oid in referenced_tags():
        try:
            object_type = git("cat-file", "-t", start_oid).strip()
        except subprocess.CalledProcessError:
            continue
        oid = start_oid
        while object_type == b"tag" and oid not in seen_tags:
            seen_tags.add(oid)
            raw = git("cat-file", "tag", oid)
            headers = raw.split(b"\n\n", 1)[0].splitlines()
            target = None
            for header in headers:
                if header.startswith(b"object "):
                    target = header[7:].decode("ascii")
                match = IDENTITY_RE.match(header)
                if match and match.group(1) == b"tagger" and not permitted(match.group(2)):
                    violations.append(f"tag {ref}: tagger email is not allowlisted")
            if target is None:
                break
            oid = target
            try:
                object_type = git("cat-file", "-t", oid).strip()
            except subprocess.CalledProcessError:
                break

    return len(commits), len(seen_tags), violations


def main() -> int:
    try:
        commit_count, tag_count, violations = identity_violations()
    except (subprocess.CalledProcessError, UnicodeDecodeError) as error:
        print(f"ERROR: could not inspect reachable Git metadata ({error.__class__.__name__}).", file=sys.stderr)
        return 2

    if violations:
        print(f"FAIL: found {len(violations)} non-allowlisted Git identity field(s) across reachable history.")
        for violation in violations:
            print(f"- {violation}; address redacted")
        return 1

    print(f"PASS: checked {commit_count} reachable commit(s) and {tag_count} annotated tag object(s); identity emails are allowlisted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
