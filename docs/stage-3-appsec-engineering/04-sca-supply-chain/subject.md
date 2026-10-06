---
title: "The Subject"
description: "Every vulnerability class so far assumed the vulnerability was in code your team wrote."
---
# Software Composition Analysis and Supply Chain Security: The Subject

*Subject 4 of 9 — Secure Development / AppSec Engineering · Version 1.0 — September 2026*

> Every vulnerability class so far assumed the vulnerability was in code your team wrote. Most of a modern application's code is dependencies nobody on the team wrote, reviewed, or necessarily trusts — and the supply chain that delivers those dependencies is itself an attack surface.

## Foreword

> *You didn't write 90% of your application's code. You just agreed, by running `npm install`, to trust everyone who did.*

## Why This Subject

A single vulnerable transitive dependency, three levels deep in a dependency tree nobody manually reviews, can be as exploitable as anything in Stage 1 — and a compromised package registry account can push a malicious update straight into thousands of production builds with no code review at all. This subject builds the specific skill of finding and reasoning about both.

## What You Must Understand

### Dependency vulnerability scanning

Tools (npm audit, pip-audit, OWASP Dependency-Check, Snyk, GitHub Dependabot) that match a project's declared and transitive dependencies against known-vulnerability databases (the CVE/NVD ecosystem) and report exploitability.

- Direct vs. transitive dependencies: a vulnerable package three levels down a dependency tree is often invisible until a scanner surfaces it
- Reachability matters: a vulnerable function in a dependency that your code never actually calls is lower real risk than the CVE score alone suggests — the same false-positive discipline from SAST applies here

### Software Bill of Materials (SBOM)

A complete, machine-readable inventory of every component in a build — the artifact that makes "are we affected by this new CVE" answerable in minutes instead of days during an incident like Log4Shell.

- Standard formats: SPDX and CycloneDX
- Generated at build time so it reflects what actually shipped, not what package.json/requirements.txt merely declares

### Typosquatting and dependency confusion

Supply-chain attacks that don't require compromising a legitimate package at all — publishing a malicious package under a name close to a popular one, or exploiting how some package managers resolve a name that exists in both a public and private registry.

- Typosquatting: `reqeusts` instead of `requests`, relying on a developer's typo
- Dependency confusion: an internal package name published publicly at a higher version number, tricking the resolver into preferring the attacker's public package over the intended internal one

### Malicious package/maintainer-account compromise

The most severe real-world category: a legitimate, trusted package's maintainer account is compromised (or a maintainer is socially engineered into transferring ownership) and a malicious update is pushed to everyone who updates.

- Pinning exact dependency versions and reviewing diffs on update is the direct mitigation — trading convenience for a manual trust-verification step
- Reproducible builds and package-signing (e.g. Sigstore) as an emerging structural mitigation

## Practical Outputs

!!! success "Practical outputs"

    - A dependency vulnerability scan of a real project (yours or open-source) with every finding triaged for actual reachability, not accepted at CVE-score face value.
    - A generated SBOM for that same project in SPDX or CycloneDX format, with a written note on what it would let you answer instantly during a hypothetical Log4Shell-style incident.
    - A written case study of one real historical supply-chain incident (e.g. event-stream, ua-parser-js, or a dependency-confusion incident) with the attack mechanism explained precisely, not just summarized.
    - A dependency-update policy document for a hypothetical team: pinning strategy, review requirements for major-version bumps, and how SBOM/scanning fits into the CI pipeline from the DAST/SAST subjects.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "A clean dependency scan means the app is safe." It means the *known*, *reported* vulnerabilities in your *declared* dependencies are addressed — supply-chain compromise and unreported (0-day) issues are both invisible to this class of tool.
    - "Updating dependencies immediately is always safer." An automatic, unreviewed update is exactly the mechanism a compromised-maintainer attack exploits — there's a real tradeoff between patching speed and verification.
    - "This is a solved problem once you add a scanner." SBOM generation, reachability analysis, and update review are ongoing engineering practices, not a one-time tool install.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Given a dependency tree, identify which vulnerable transitive dependencies are actually reachable from the application's own code.
    - Explain dependency confusion precisely enough to describe the exact resolver behavior it exploits.
    - Generate and interpret an SBOM for an unfamiliar project.
    - Defend a specific dependency-update policy for a hypothetical high-security team, with tradeoffs named explicitly.
