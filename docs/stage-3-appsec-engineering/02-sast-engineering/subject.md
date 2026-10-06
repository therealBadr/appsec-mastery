---
title: "The Subject"
description: "Secure Code Review Methodology built the manual skill and confronted its scale problem head-on."
---
# SAST Engineering: The Subject

*Subject 2 of 9 — Secure Development / AppSec Engineering · Version 1.0 — September 2026*

> Secure Code Review Methodology built the manual skill and confronted its scale problem head-on. This subject builds the tool that actually scales it: real Semgrep/CodeQL rules, written and tuned by you, replacing the hand-rolled pattern-matchers from earlier capstones with the production-grade engines real AppSec teams run in CI.

## Foreword

> *A SAST rule that fires on every use of a dangerous function, with no data-flow awareness, is not a security tool. It is a way to get your tool disabled by the first team that has to triage its output.*

## Why This Subject

Your Cryptography Fundamentals and Secure Code Review capstones already built hand-rolled static scanners and were explicitly graded on zero false positives against clean code — that discipline is the entire craft of SAST engineering, and this subject hands you the industrial-strength engines (Semgrep, Bandit, CodeQL) built for exactly that problem, with real data-flow tracking your regex-based capstones could only approximate.

## What You Must Understand

### Semgrep rule authoring

A pattern-based rule language that matches source-code structure (not just text), supporting metavariables, pattern-either/pattern-not composition, and — critically — taint-mode rules that track data flow from a declared source to a declared sink across function boundaries.

- Structural patterns beat regex: `$X = input(...)` matches regardless of variable naming, spacing, or intervening comments
- Taint mode directly automates the source→sink tracing discipline from Secure Code Review's Exercise 01
- pattern-not and pattern-inside narrow a rule to avoid the false positives your earlier capstones were graded against

### Bandit for Python

A Python-specific AST-based scanner with a large built-in ruleset (hardcoded passwords, SQL string-building, insecure deserialization, weak crypto) — useful both as a ready-made baseline and as a model for how AST-based (not regex-based) scanning avoids a whole category of false positive.

- AST-based matching sees actual code structure, not text that merely looks like a pattern inside a string literal or comment
- Confidence and severity are reported separately — a real scanner's output needs both dimensions, not a single flat "found it"

### CodeQL

A full queryable database representation of a codebase (control flow, data flow, call graphs) queried with a dedicated query language — the deepest tool in this subject, capable of expressing genuinely complex, precise data-flow questions no regex or simple AST pattern could.

- Codebases are compiled into a relational database of their own structure — queries traverse it like SQL over source code
- Real-world CVE-hunting: many public CodeQL queries exist specifically to rediscover known vulnerability patterns across new codebases

### Rule quality and false-positive tuning

The actual craft: a rule with 100% recall and 40% precision gets disabled by week two; the entire discipline learned across every earlier capstone's zero-false-positive grading standard is what separates a rule that survives contact with a real codebase from one that doesn't.

- Test every rule against both a vulnerable fixture and a deliberately similar-looking-but-safe fixture, every time
- Track false-positive reports from real usage and feed them back into the rule — rules are living artifacts, not one-shot code

## Practical Outputs

!!! success "Practical outputs"

    - At least 5 custom Semgrep rules, each catching a real vulnerability pattern from this roadmap (e.g. non-parameterized SQL, shell=True with string interpolation, disabled TLS verification), each tested against a vulnerable and a clean fixture.
    - A Bandit run against a real codebase (your Secure Code Review target) with the results triaged — every finding marked true/false positive with reasoning, not accepted at face value.
    - One CodeQL query (using an existing query pack as a starting template is fine) run against a real codebase, with its results explained.
    - A written comparison of all three tools' precision/recall tradeoffs based on your own triage data, not vendor marketing claims.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "More rules is better." A noisy ruleset that developers learn to ignore is worse than a small, trusted one — this is the same zero-false-positive lesson from three earlier capstones, now applied at tool-selection scale.
    - "SAST finds everything." SAST is blind to business logic, most access-control bugs, and anything requiring runtime state — that gap is exactly what DAST (the next subject) and manual testing exist to cover.
    - "Writing the rule is the hard part." Tuning it against real-world false positives after deployment is where most of the actual engineering time goes.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Write a working Semgrep taint-mode rule from scratch, live, for a vulnerability class you're given on the spot.
    - Explain precisely why AST/structural matching catches cases regex-based scanning misses, with a concrete example.
    - Triage a batch of real Bandit findings against an unfamiliar codebase, correctly separating true from false positives with reasoning.
    - Explain what CodeQL can find that Semgrep structurally cannot, and vice versa.
