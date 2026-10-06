---
title: "The Subject"
description: "Every hardcoded API key, database password, and signing secret this roadmap has spent six subjects teaching you to hunt for by hand gets a dedicated subje…"
---
# Secrets Detection and Management: The Subject

*Subject 7 of 9 — Secure Development / AppSec Engineering · Version 1.0 — September 2026*

> Every hardcoded API key, database password, and signing secret this roadmap has spent six subjects teaching you to hunt for by hand gets a dedicated subject on the other side of the table: catching it before it's ever committed, and architecting secret storage so a leaked credential is a rotation, not an incident.

## Foreword

> *A secret committed to git isn't un-committed by deleting it in the next commit. Git history is a permanent record, and a leaked credential's clock started the moment it was pushed, not the moment someone noticed.*

## Why This Subject

Cryptography Fundamentals' capstone already built a static scanner rule for hardcoded secrets; this subject goes deeper into detection (entropy analysis, git-history scanning) and — the part that actually prevents the problem rather than just catching it — real secret-management architecture, so the default way to use a credential in code never involves a literal string at all.

## What You Must Understand

### Detection techniques

How a scanner actually recognizes a secret in source without a maintained list of every possible API key format: pattern matching against known provider key formats, and Shannon-entropy analysis for anything that doesn't match a known pattern but still looks like high-randomness secret material.

- Known-format matching (AWS keys, GitHub tokens, Slack tokens all have recognizable prefixes/shapes) — high precision, but blind to anything novel
- Entropy-based detection catches arbitrary/custom secrets by flagging suspiciously high-randomness strings — higher recall, more false positives (a hash, a UUID, and a real secret can look statistically identical)

### git-secrets and truffleHog

Tools that scan not just the current working tree but the full git history — because a secret removed in a later commit is still sitting, permanently, in every clone's history unless the history itself is rewritten.

- Pre-commit hook mode (git-secrets) blocks a secret before it's ever committed — the cheapest possible point of intervention
- Full-history scanning (truffleHog) finds what already leaked, which requires a different remediation path (rotation, and potentially history rewriting) than prevention does

### Remediation: rotation, not deletion

The actual incident-response step once a secret is found in history: the credential must be treated as compromised and rotated at the source system — deleting the commit or rewriting history helps hygiene but does nothing to a secret an attacker may have already scraped.

- History rewriting (git filter-repo / BFG) without rotation is security theater — assume anything ever pushed to a remote was seen
- A rotation runbook (who rotates what, how fast, how dependent services are updated) turns this from a scramble into a practiced procedure

### Secret management architecture

The actual fix: secrets live in a dedicated store (HashiCorp Vault, AWS Secrets Manager, or your cloud provider's equivalent) and are injected into an application at runtime — never as a literal in source, never even as a plaintext environment variable checked into a deploy config.

- Short-lived, dynamically-generated credentials (Vault's dynamic secrets) bound a leaked credential's exposure window even further than rotation policy alone
- Access to the secret store itself becomes the new high-value target — the store's own access control is where the security property actually lives

## Practical Outputs

!!! success "Practical outputs"

    - A pre-commit secrets-detection hook (git-secrets or truffleHog in pre-commit mode) integrated into a real repository, demonstrated blocking a deliberately staged secret commit.
    - A full-history scan of an existing repository (yours or a permitted open-source one) with any findings triaged (true leaked secret vs. false-positive high-entropy string).
    - A written incident-response runbook for a leaked production credential: detection, rotation, and verification steps, timed and realistic.
    - A working integration of one secret-management system (Vault, AWS Secrets Manager, or equivalent) with a sample application, demonstrating a credential fetched at runtime with no plaintext secret anywhere in source or deploy config.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "I deleted the file in the next commit, so it's fine." Git history preserves it permanently unless the history itself is rewritten — and even then, assume anything pushed to a remote may already be scraped.
    - "Environment variables are a secure enough place for secrets." An env var is one accidental `env` dump, error log, or debug endpoint away from disclosure — better than hardcoding, still not a real secret-management architecture.
    - "We'll rotate it if it ever actually leaks." Rotation without a practiced runbook, under real incident pressure, takes far longer and is far more error-prone than a rehearsed one.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Explain the precision/recall tradeoff between pattern-based and entropy-based secret detection with a concrete example of each failing.
    - Given a leaked credential scenario, walk through the correct incident-response sequence from detection to verified rotation.
    - Explain why history-rewriting alone is an incomplete remediation.
    - Demonstrate an application fetching a secret from a real secret-management system at runtime, live.
