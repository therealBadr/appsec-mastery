---
title: "The Subject"
description: "Every subject from Stage 0 onward has produced a tool solving one narrow, specific problem."
---
# Building and Publishing Original Security Tools: The Subject

*Subject 5 of 6 — Real-World Readiness and Portfolio · Version 1.0 — September 2026*

> Every subject from Stage 0 onward has produced a tool solving one narrow, specific problem. This subject is about taking one of them further than "worked for the exercise" — real usability, real documentation, real users — because an original, externally-used tool is the single strongest signal in the entire portfolio strategy this roadmap builds toward.

## Foreword

> *A tool you built for one exercise proves you understood the concept once. A tool someone else installs and depends on proves you built something that works for problems you didn't anticipate.*

## Why This Subject

This roadmap has produced dozens of working tools by this point — the difference between "a tool that passed its own exercise's defense" and "a tool worth publishing" is entirely in the parts that don't show up in an exercise's mandatory-part checklist: a real README, sane defaults, error handling for inputs you didn't plan for, and packaging that lets a stranger install and run it in under five minutes.

## What You Must Understand

### Choosing what to build (or extend)

The strongest candidate is rarely a brand-new idea — it's one of your existing roadmap tools (the OOB-confirmation scanner, the authorization-matrix fuzzer, the race-condition harness) generalized beyond the one lab target it was built and tested against.

- A tool solving a problem you personally hit repeatedly across this roadmap (the shared OOB-listener pattern reused across three separate capstones is a strong signal of a genuinely useful, generalizable idea) beats a tool built purely to have a portfolio entry
- "Not a wrapper around existing tools" — the roadmap's own portfolio-strategy standard — rules out a thin CLI wrapper around `nmap` or `sqlmap` with no independent logic

### Real documentation

A README that gets a stranger from zero to a working first run in under five minutes: what the tool does, why it exists (what gap it fills relative to existing tools), installation, a runnable example, and known limitations stated honestly.

- Stating known limitations honestly (what this tool does NOT catch, mirroring the "unclassified/inconclusive" discipline built into nearly every capstone in this roadmap) builds more credibility than an inflated feature list
- A usage example with real (or realistic sample) output, not just a command line with no context for what success looks like

### Packaging and distribution

The mechanical work of making installation trivial: a proper Python package (pyproject.toml, published to PyPI) or a single-binary release, versioned releases with changelogs, and a permissive open-source license.

- Dependency pinning and a clean virtual-environment story prevent the "works on my machine" failure that kills adoption fastest
- Semantic versioning and a changelog signal active, trustworthy maintenance to anyone evaluating whether to depend on the tool

### Community and maintenance

What happens after the first release: responding to issues, accepting a first external contribution, and the ongoing (often unglamorous) work of keeping a tool working as its dependencies and target environments change.

- A tool with open issues and no response for months signals abandonment to anyone evaluating it — even a brief "still maintained, low priority" comment matters
- Accepting one genuine external contribution (even a small doc fix) is a real, citable milestone distinct from stars/forks alone

## Practical Outputs

!!! success "Practical outputs"

    - One original security tool, generalized from an earlier roadmap capstone, published on GitHub with a proper README, installation instructions, and a runnable example with sample output.
    - A versioned release (at least v0.1.0, ideally v1.0.0) with a changelog, and — for a Python tool — a real package published to PyPI (or the equivalent for your tool's language/ecosystem).
    - A comparison section in the README: what this tool does differently from or better than existing alternatives, honestly assessed (including where an existing tool is still better for some use cases).
    - Evidence of at least minimal external engagement: a star, a fork, an issue from someone other than you, or a genuine attempt to solicit feedback (e.g. posting it to a relevant community) — the roadmap's own exit-gate criterion is "external stars/forks," and this output is the honest attempt at earning them, not a guarantee of a specific number.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "If the code is good, people will find it." Discoverability requires actually sharing it — a relevant subreddit, a security Discord/community, or a short write-up announcing it — silent publishing rarely gets organic traction.
    - "More features make a stronger portfolio piece." A tool that does one thing precisely, with honest documented limitations, is more credible and more likely to actually get used than a sprawling one that does many things unreliably.
    - "This is done once it's published." A published tool with no subsequent commits for a year reads as abandoned — even light, occasional maintenance signals real ongoing ownership.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Walk a stranger (the evaluator) through installing and running your tool from the README alone, with no additional guidance from you.
    - Defend your tool's design choices, including at least one thing you'd change if you were rebuilding it today.
    - Explain honestly what your tool does NOT catch or handle, and why those limits exist.
    - Show your actual release/versioning history and explain your maintenance plan going forward.
