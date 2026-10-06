---
title: "The Subject"
description: "The closing Stage 3 subject, where the whole stage's tooling meets a live fire scenario: given a web application that has already been compromised, work b…"
---
# Incident Triage for Compromised Web Applications: The Subject

*Subject 9 of 9 — Secure Development / AppSec Engineering · Version 1.0 — September 2026*

> The closing Stage 3 subject, where the whole stage's tooling meets a live fire scenario: given a web application that has already been compromised, work backward from evidence to root cause, using logging, the CrashTriage-style forensic instincts from OS Internals, and the SBOM/dependency knowledge from Software Composition Analysis to answer "what happened" fast enough to matter.

## Foreword

> *By the time you're doing incident response, every earlier stage's knowledge has already stopped being optional and started being the only thing standing between "contained in an hour" and "contained in a week.*

## Why This Subject

Every prior subject in this roadmap either builds or breaks something; this one investigates something already broken, under time pressure, with an attacker's actual actions to reconstruct instead of your own controlled exploit to demonstrate — the honest final test of whether the roadmap's knowledge actually composes under pressure.

## What You Must Understand

### Initial detection and triage

The first, highest-leverage decisions in any incident: is this real, what's the scope, and what's the fastest safe containment action — answered from log evidence (access logs, application logs, cloud audit logs) under incomplete information, not certainty.

- A false positive treated as real wastes response capacity; a real incident treated as noise is far worse — calibrated triage matters more than speed alone
- Containment (isolating the affected system) versus eradication (removing the actual foothold) are different steps, in that order, not one action

### Log analysis for compromise evidence

Reusing and extending logsentry's Bash log-analysis skill (Linux Administration Depth) and the syscall/process forensics from OS Internals' straceit and crashtriage — applied now to a genuinely unknown, adversarial timeline instead of a known lab scenario.

- Web server access logs for the initial exploitation request (often a specific vulnerability class from Stage 1/2, recognizable from its payload shape)
- Application logs for what the exploited endpoint actually did once reached
- `auth.log`/process history for any lateral movement or persistence attempt (cron-based persistence, exactly as covered in Linux Administration Depth's capstone)

### Identifying the initial vector

Working backward from a webshell, an unexpected outbound connection, or a data-exfiltration alert to the specific application vulnerability that let the attacker in — directly exercising the code-review and black-box skills from every earlier subject, now applied diagnostically instead of offensively.

- A found webshell strongly suggests a file-upload or LFI-to-RCE vector (File Handling Vulnerabilities) — the artifact itself narrows the hypothesis space
- Unexpected outbound connections from an app server suggest SSRF or a supply-chain-compromised dependency (SCA and Supply Chain) as competing hypotheses to rule in or out from evidence

### Containment, eradication, and lessons learned

The back half of the incident lifecycle: safely isolating without destroying evidence, removing every foothold (not just the obvious one — check for a second, quieter persistence mechanism), and a blameless retrospective that feeds findings back into the SAST/DAST/DevSecOps pipeline so the same class doesn't recur.

- A retrospective that stops at "patch the one CVE" without asking "why didn't our pipeline catch this" wastes the incident's only real value
- Evidence preservation (disk/memory snapshots before remediation) matters for both root-cause certainty and, in some contexts, legal/compliance requirements

## Practical Outputs

!!! success "Practical outputs"

    - A full incident-response tabletop exercise against your own deliberately-compromised lab environment (plant a realistic compromise — e.g. a webshell via a File Handling vulnerability, plus a cron-based persistence mechanism — without documenting it, then investigate cold).
    - A written incident report reconstructing the full timeline from log evidence alone: initial vector, actions taken, persistence established, and how you confirmed each step from evidence rather than assumption.
    - A containment/eradication runbook you executed against the lab compromise, including a check for a second, deliberately-planted-but-undocumented persistence mechanism you weren't told about in advance.
    - A retrospective document feeding at least two concrete findings back into a DevSecOps pipeline (SAST rule, SCA policy, or a specific monitoring alert) that would have caught this specific incident earlier.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "We found the webshell, we're done." A found artifact is evidence of the (at least one) way in — assume a competent attacker left a second, quieter path in as well until you've specifically checked and ruled it out.
    - "Incident response is a different skill from everything else in this roadmap." It's the same skills — log analysis, vulnerability-class recognition, systems forensics — applied backward, under pressure, to an unknown timeline instead of a known target.
    - "The retrospective is just paperwork after the real work is done." The retrospective is what prevents this exact incident from recurring — skipping it turns every future incident into a repeat.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Given raw, unannotated logs from a compromised lab system, reconstruct the actual attack timeline without being told what happened.
    - Correctly distinguish containment actions from eradication actions and explain why the order matters.
    - Find a second, undocumented persistence mechanism planted in your own lab compromise without being told it exists.
    - Produce a retrospective with at least two concrete, actionable pipeline changes that would have caught this incident earlier.
