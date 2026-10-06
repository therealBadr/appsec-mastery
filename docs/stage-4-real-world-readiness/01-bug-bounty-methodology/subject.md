---
title: "The Subject"
description: "Every hands-on technique from Stage 1-2 aimed at a target you built."
---
# Bug Bounty Methodology: The Subject

*Subject 1 of 6 — Real-World Readiness and Portfolio · Version 1.0 — September 2026*

> Every hands-on technique from Stage 1-2 aimed at a target you built. This subject aims the same techniques at real, in-scope programs — with the added disciplines that separate a credible hunter from noise: scoping, systematic (not opportunistic) testing, and triage-ready reporting.

## Foreword

> *A bug bounty program's scope document is a contract. Reading it carefully is not bureaucracy — it's the difference between a valid finding and an unauthorized intrusion.*

## Why This Subject

The roadmap is explicit that bug bounty hunting before Stage 2's depth is real is demoralizing and teaches little — this subject exists specifically because, having cleared Stage 0-3, the systematic testing habits are already built; what's left is the program-specific discipline of scope, triage economics, and responsible disclosure that turns raw skill into an accepted, paid finding.

## What You Must Understand

### Scoping and rules of engagement

Every program on HackerOne/Bugcrowd defines exactly what's in scope (domains, apps, even specific vulnerability classes) and what's explicitly excluded (often DoS, social engineering, physical access) — testing outside scope is not a gray area, it's unauthorized access.

- Wildcard scope (`*.example.com`) still requires care — a subdomain that resolves to a third-party SaaS product (e.g. a status page) is technically in-scope-by-domain but often explicitly excluded or owned by someone else entirely
- Re-reading scope before every session, not just once at sign-up — programs update scope, and a stale mental model causes real mistakes

### Systematic methodology over opportunistic poking

The actual differentiator between hunters who find bugs consistently and those who don't: a repeatable process (recon → attack-surface mapping → systematic testing per vulnerability class → reporting) applied to every target, reusing the coverage-table discipline from Access Control and IDOR and the API Authorization capstone directly.

- Recon depth matters more than most people expect — an overlooked subdomain or an old API version still running is often where the bugs concentrate, precisely because it gets less attention from other hunters too
- Revisiting a program periodically (new features ship, old bugs get reintroduced) rather than testing once and moving on

### Triage economics

Understanding the process on the other side of a submitted report: a triager reviewing dozens of reports a day rewards ones that are immediately actionable and penalizes vague, low-effort, or duplicate ones — the same report-quality bar as every earlier capstone's evidence discipline, now with real money and reputation attached.

- A report a triager can reproduce in under two minutes from your steps gets prioritized over one requiring back-and-forth clarification
- Duplicate submissions are extremely common on popular programs — a fast, well-documented first report beats a technically-better but slower one

### Responsible disclosure

The ethical and legal framework underneath the entire activity: report through the program's defined channel, respect embargo/disclosure timelines, never access more data than needed to prove impact, and never disclose publicly before the program agrees.

- Accessing more data than necessary to demonstrate impact (e.g. dumping an entire user table instead of one record) can itself violate program rules even when the underlying vulnerability is real
- A program with no bounty but a documented disclosure policy still deserves the same professional, patient process as a paying one

## Practical Outputs

!!! success "Practical outputs"

    - An active profile on HackerOne and/or Bugcrowd, with a documented target-selection process (why you chose the programs you tested) rather than a random program list.
    - A systematic recon-and-testing log for at least 3 real in-scope programs, showing the methodology applied consistently, not opportunistic one-off attempts.
    - At least one submitted report, valid or not — a report written to the same triage-ready standard as your Stage 1-2 capstone reports, with steps a stranger could reproduce.
    - A written retrospective on your first submission(s): what the triager's response taught you, and what you'd do differently next time.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "More programs tested shallowly beats fewer tested deeply." Real findings concentrate where you actually understand the attack surface — the recon-and-coverage discipline from Stage 2 matters more here, not less.
    - "A rejected/duplicate report means I did something wrong." Duplicates are a normal, expected outcome on any popular program — the report-quality bar, not the outcome of any single submission, is what to judge yourself against.
    - "Bug bounty hunting is the fastest path to a job." It's a portfolio signal and a skill-sharpening practice, not a reliable income source for most hunters — treat the exit-gate finding as a credibility marker, not a career plan on its own.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Read an unfamiliar program's scope document and correctly identify what is and isn't in scope, including an ambiguous edge case.
    - Walk through your systematic testing methodology for a real program, showing the coverage log.
    - Produce a triage-ready report for a finding, live, in the time a real submission deadline would allow.
    - Explain the responsible-disclosure boundary you'd never cross, with a concrete example of a tempting-but-wrong action.

## Certification / Portfolio Checkpoint

!!! info "Checkpoint"

    This subject has no gated certification, but its output — at least one valid, acknowledged bug bounty finding — is the Stage 4 exit-gate criterion referenced later in this roadmap's portfolio strategy.
