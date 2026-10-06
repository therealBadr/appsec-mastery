---
title: "The Subject"
description: "SAST reads code without running it; DAST attacks the running application without reading its source — the black-box automation of everything Stage 1-2 did…"
---
# DAST and Dynamic Pipeline Integration: The Subject

*Subject 3 of 9 — Secure Development / AppSec Engineering · Version 1.0 — September 2026*

> SAST reads code without running it; DAST attacks the running application without reading its source — the black-box automation of everything Stage 1-2 did by hand, wired into a pipeline so it runs on every deploy instead of once, manually, when someone remembers.

## Foreword

> *A DAST scan that runs once before launch and never again is a photograph of a system that keeps moving.*

## Why This Subject

Every black-box technique across Stage 1 and Stage 2 — header analysis, injection probing, authorization matrix testing — has a place in an automated DAST pipeline; the engineering problem here isn't finding new vulnerability classes, it's making detection continuous, low-noise, and safe to run against a live target without becoming a denial-of-service tool.

## What You Must Understand

### OWASP ZAP as a pipeline component

A free, scriptable DAST engine that can run as a baseline passive scan (safe against production) or a full active scan (safe only against a dedicated test environment), automatable via its API/CLI for CI integration.

- ZAP Baseline scan: passive-only, safe to run against anything, catches header/cookie/config issues (reusing HTTP Internals' ground)
- ZAP Full scan: active, sends real attack payloads — test-environment only, never production
- Scripting ZAP via its API lets you seed authentication state so the scan covers logged-in functionality, not just the public surface

### Custom Burp extensions in a pipeline context

The Burp Mastery extension work, repurposed: a headless-capable check (or a Burp Enterprise/CI-integrated scan, if available) that runs the same detection logic as an interactive extension but triggered by a pipeline event instead of a person clicking scan.

- The gap between "an extension I run manually" and "a check that runs on every PR" is entirely about triggering and reporting, not detection logic

### Authenticated scanning

The single biggest practical DAST problem: an unauthenticated scan sees a fraction of the application's real attack surface, so the pipeline needs a reliable way to log the scanner in and keep it logged in across a multi-hour scan.

- Session-token injection via a pre-scan login script (reusing your Authentication and Session Security understanding of what a valid session actually requires)
- Detecting and handling session expiry mid-scan (a scan that silently continues unauthenticated after logout produces a false sense of coverage)

### Scan safety and blast-radius control

The property that separates a DAST pipeline from an unintentional attack: rate limiting, an explicit target allowlist, and exclusion rules for destructive endpoints (delete/payment actions), reusing the rate-governance discipline built in the Server-Side Injection and Race Conditions capstones.

- A DAST run against the wrong environment (production instead of staging) is a real, repeated real-world incident category — pipeline config must make that mistake hard, not just discouraged by policy

## Practical Outputs

!!! success "Practical outputs"

    - A ZAP baseline scan integrated into a GitHub Actions workflow, running automatically on every push to a test branch, with results posted as a build artifact or PR comment.
    - An authenticated ZAP scan configuration (a login script or session-handling script) that correctly logs in and maintains session state, verified by comparing authenticated vs. unauthenticated scan coverage on the same target.
    - A documented set of exclusion rules protecting destructive endpoints from the active scan, tested by confirming the scanner never triggers them.
    - A written incident-prevention checklist: the specific configuration steps that prevent a DAST pipeline from ever accidentally targeting production.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "DAST replaces manual testing." DAST finds what it's configured to find and nothing about business logic or multi-step workflow abuse (Race Conditions and Business Logic) — it's a coverage floor, not a ceiling.
    - "An unauthenticated scan is good enough." Most of an application's real attack surface sits behind a login; skipping authenticated scanning dramatically understates real risk.
    - "Active scanning is always safe to run." An active scan against a target with real payment/delete actions and no exclusion rules is a self-inflicted incident waiting to happen.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Configure and run an authenticated DAST scan against an unfamiliar target from scratch.
    - Explain exactly what separates ZAP's baseline and full scan modes and when each is safe to use.
    - Given a target application, write the exclusion-rule set that would protect it from an active scan's destructive actions.
    - Explain, concretely, how this pipeline reduces (but doesn't eliminate) the need for the manual techniques from Stage 1-2.
