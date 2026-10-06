---
title: "The Subject"
description: "The shift from breaking to building defensively starts here: a disciplined method for finding an application's vulnerabilities before a single line of exp…"
---
# Threat Modeling: The Subject

*Subject 1 of 9 — Secure Development / AppSec Engineering · Version 1.0 — September 2026*

> The shift from breaking to building defensively starts here: a disciplined method for finding an application's vulnerabilities before a single line of exploit code exists, by decomposing what it does, what could go wrong, and what you're actually going to do about it.

## Foreword

> *A threat model is not a document you write once and file away. It's the question "what did we just assume?" asked systematically instead of never.*

## Why This Subject

Every earlier stage found vulnerabilities by attacking or reading real, already-built systems. Threat modeling finds them on a whiteboard, before the system exists, which is both cheaper (a design-time fix costs nothing; a production fix costs an incident) and harder (there's no running target to poke — only assumptions to interrogate systematically).

## What You Must Understand

### STRIDE

A per-element threat taxonomy applied to a data-flow diagram: for every process, data store, and data flow, ask whether Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, or Elevation of privilege applies.

- Spoofing → maps to authentication controls (Authentication and Session Security)
- Tampering → maps to integrity controls (parameterized queries, signed tokens, TLS)
- Repudiation → maps to audit logging and non-repudiation (who did what, provably)
- Information disclosure → maps to access control and encryption (Access Control and IDOR)
- Denial of service → maps to rate limiting and resource-consumption bounds (Race Conditions' concurrency limits, GraphQL complexity limiting)
- Elevation of privilege → maps to authorization boundaries (BOLA/BFLA, least privilege)

### PASTA

A seven-stage, risk-centric methodology (Process for Attack Simulation and Threat Analysis) that starts from business objectives and works down to attack simulation, favored where a threat model needs to justify itself to non-technical stakeholders in business-impact terms rather than pure technical taxonomy.

- Stage progression: business objectives → technical scope → application decomposition → threat analysis → vulnerability/weakness analysis → attack modeling → risk/impact analysis
- Distinguishing feature versus STRIDE: explicitly risk- and business-impact-driven throughout, not just a technical checklist

### Attack trees

A goal-oriented decomposition: put the attacker's objective at the root, and break it down into the concrete ways it could be achieved, each further decomposable — useful specifically for reasoning about a single high-value target (e.g. "compromise the admin account") across multiple attack classes at once.

- Root node = attacker goal; child nodes = ways to achieve it (each optionally AND/OR combined)
- Directly reusable output: each leaf node is a concrete finding candidate to test for, tying threat modeling straight back to Stage 1/2's hands-on techniques

### Data-flow diagramming

The prerequisite artifact for STRIDE: processes, data stores, external entities, and trust-boundary lines between them — drawn accurately enough that "what crosses this boundary unchecked" becomes a visually obvious question.

- Trust boundaries are the single most important element — everything this roadmap has taught about "data crossing into syntax/execution unchecked" is a trust-boundary violation
- A DFD drawn from the actual architecture (not the idealized one) surfaces the assumptions worth threat-modeling

## Practical Outputs

!!! success "Practical outputs"

    - A full STRIDE threat model for a real application (your own Stage 1/2 target, or an open-source app) — DFD, per-element threat enumeration, and a mitigation mapped to each identified threat.
    - An attack tree for one high-value goal against that same application (e.g. "achieve admin account takeover"), with at least 10 leaf nodes, each cross-referenced to a specific technique from an earlier roadmap subject.
    - A PASTA-style business-impact writeup for the single highest-risk finding from your STRIDE model, translating the technical risk into a stakeholder-facing impact statement.
    - A "threat model diff": re-run the STRIDE model after a hypothetical architecture change (e.g. adding a new microservice or third-party integration) and document exactly which new threats the change introduces.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "Threat modeling is a one-time document." It has to be revisited every time the architecture changes — an out-of-date threat model gives false confidence, which is worse than none.
    - "STRIDE finds vulnerabilities." STRIDE finds *threat categories* to investigate — the actual vulnerability-finding still happens through the hands-on techniques from Stages 1-2, applied to what STRIDE flagged as worth checking.
    - "This is a compliance exercise." A threat model that exists only to satisfy an audit checkbox, with no engineering team actually reading or acting on it, produced nothing of value.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Given an unfamiliar application's architecture diagram, produce a STRIDE threat enumeration for at least three components without notes.
    - Explain the practical difference between STRIDE, PASTA, and attack trees, and when you'd reach for each.
    - Draw a data-flow diagram with correctly placed trust boundaries for a system you haven't modeled before, live.
    - Defend your published STRIDE threat model's mitigations, mapping each back to a concrete control from an earlier Stage 0-2 subject.
