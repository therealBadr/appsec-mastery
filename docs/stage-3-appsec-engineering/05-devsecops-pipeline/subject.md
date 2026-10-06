---
title: "The Subject"
description: "The integration subject: SAST, DAST, and SCA are each a tool; a DevSecOps pipeline is the engineering work of wiring all three into CI/CD so they run auto…"
---
# DevSecOps Pipeline Engineering: The Subject

*Subject 5 of 9 — Secure Development / AppSec Engineering · Version 1.0 — September 2026*

> The integration subject: SAST, DAST, and SCA are each a tool; a DevSecOps pipeline is the engineering work of wiring all three into CI/CD so they run automatically, report usefully, and — the actual hard part — don't get disabled by the first team whose velocity they visibly slow down.

## Foreword

> *DevSecOps is not "run tools in a pipeline." It's making the secure path the path of least resistance, which is a product-design problem wearing a security team's clothes.*

## Why This Subject

Every tool from the three subjects before this one produces findings; a pipeline that dumps all of them, unfiltered, into a developer's PR gets the pipeline disabled within a sprint. The actual DevSecOps skill is triage automation, severity gating, and false-positive suppression tuned well enough that developers trust what the pipeline tells them.

## What You Must Understand

### Pipeline architecture

Where each check runs and why: pre-commit hooks for the fastest, cheapest checks (secrets detection, basic lint), PR-time checks for SAST/SCA (fast enough to gate a merge), and scheduled/post-deploy checks for DAST (too slow and potentially disruptive to run on every PR).

- Pre-commit: secrets detection, formatting — must run in seconds or developers disable it
- PR/CI-time: SAST (Semgrep/Bandit/CodeQL), SCA (dependency scan) — minutes, gates merge
- Scheduled/post-deploy: DAST against a staging environment — can take longer, runs less frequently

### GitHub Actions as the orchestration layer

Workflow YAML wiring together the SAST, SCA, and DAST-baseline tools from the earlier three subjects, with results surfaced as PR annotations/comments rather than a separate dashboard nobody checks.

- Reusable workflow files so the same security gate applies consistently across many repositories
- Secrets management within the pipeline itself (the pipeline's own credentials are now part of the attack surface — a lesson the Secrets Detection subject develops fully)

### Severity gating and merge-blocking policy

The actual governance decision: which finding severities block a merge outright, which post a warning, and which are informational only — get this wrong in either direction (block everything, or block nothing) and the pipeline fails at its actual job.

- A policy that blocks on every SAST finding regardless of confidence trains developers to find workarounds, not fix issues
- A policy that never blocks anything provides no actual security guarantee at all

### Reducing false-positive fatigue

Every technique from SAST Engineering's tuning discipline, applied at pipeline scale: suppression annotations for accepted-risk findings (with required justification and expiry, not silent permanent suppression), and tracking suppression rates as a pipeline health metric.

- A suppression with no expiry/review date is a permanent hole a future engineer won't know to revisit
- Tracking false-positive rate over time tells you whether the pipeline is actually improving or just accumulating noise

## Practical Outputs

!!! success "Practical outputs"

    - A complete sample application with SAST (Semgrep/Bandit), SCA (dependency scan), and a DAST baseline scan integrated into GitHub Actions, triggered appropriately (PR-time vs. scheduled) per the pipeline-architecture topic above.
    - A documented severity-gating policy applied as actual pipeline configuration (not just a document) — demonstrated blocking a deliberately introduced high-severity finding and not blocking a deliberately introduced low-severity one.
    - A suppression mechanism with mandatory justification and expiry, demonstrated suppressing one accepted-risk finding and then correctly re-surfacing it after the expiry date passes.
    - A written retrospective: if you were rolling this pipeline out to a real, currently-pipeline-free engineering team, what would you introduce first, in what order, and why — addressing the adoption problem directly, not just the technical one.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "More gates is more secure." A pipeline developers route around (via force-push, a bypassed check, or simple attrition) provides less real security than a smaller pipeline they actually respect.
    - "This is a security team problem." A DevSecOps pipeline that the platform/DevOps team doesn't co-own gets deprioritized the moment it competes with a deadline.
    - "Once it's built, it's done." Suppression rot, tool version drift, and rule staleness all require ongoing maintenance exactly like the applications the pipeline protects.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Design a pipeline architecture (what runs where, and why) for an unfamiliar application from a short description.
    - Defend a specific severity-gating policy, including what happens when it produces a false block on a real PR.
    - Explain the suppression-with-expiry mechanism and why a permanent, unreviewed suppression is itself a security debt.
    - Show your GitHub Actions pipeline live, triggering both a passing and a blocked run.
