#!/usr/bin/env python3
"""Minimal YAML sanity checker: tabs, duplicate top-level keys, trailing spaces."""
import sys, re

def check(path):
    problems = []
    seen = set()
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if "\t" in line:
                problems.append((n, "tab character (YAML forbids tabs)"))
            if line.rstrip("\n").endswith(" ") and line.strip():
                problems.append((n, "trailing whitespace"))
            m = re.match(r"^([A-Za-z0-9_-]+):", line)
            if m:
                if m.group(1) in seen:
                    problems.append((n, "duplicate top-level key: " + m.group(1)))
                seen.add(m.group(1))
    return problems

def main(args):
    rc = 0
    for p in args:
        for n, msg in check(p):
            print("%s:%d: %s" % (p, n, msg))
            rc = 1
    return rc

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
