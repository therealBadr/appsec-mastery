---
title: "The Subject"
description: "Software Composition Analysis and Supply Chain Security built the practitioner's defensive skill: scan, triage, and manage dependency risk."
---
# Supply Chain Security Research: The Subject

*Subject 6 of 7 — Advanced Specialization · Version 1.0 — September 2026*

> Software Composition Analysis and Supply Chain Security built the practitioner's defensive skill: scan, triage, and manage dependency risk. This specialization lane studies the offense side directly — how real supply-chain attacks are actually constructed, and the emerging provenance/attestation techniques built specifically to make them harder.

## Foreword

> *The most efficient attack against a well-defended target is rarely a zero-day against the target itself. It's a normal-looking dependency update the target's own build pipeline will trust and pull in automatically.*

## Why This Subject

This lane goes past SCA's scanning-and-triage discipline into the mechanics an attacker actually uses to compromise a supply chain, and the current best practice — build provenance, artifact signing, and reproducible builds — for making that mechanism structurally harder, which is exactly the kind of "make the secure choice the default" thinking Security Architecture and Engineering formalized a stage earlier.

## What You Must Understand

### Build pipeline compromise

An attacker's highest-leverage target is rarely the shipped artifact itself but the pipeline that produces it — a compromised CI runner, an overprivileged CI credential, or a malicious pre-build/post-build script injected via a seemingly unrelated PR — because compromising the pipeline compromises every future build automatically.

- CI/CD credentials with broad, long-lived access (the DevSecOps Pipeline Engineering subject's own secrets-in-the-pipeline concern) are a direct, high-value target once an attacker has any foothold in the build environment
- A build script sourced from a third-party action/plugin (e.g. a GitHub Action from an unverified publisher) is itself a supply-chain dependency, subject to the identical trust question as any code dependency

### Dependency-confusion and typosquatting at scale

Software Composition Analysis and Supply Chain Security introduced these; this subject studies them as an attacker actually would — systematically identifying internal package names likely to exist (via leaked build configs, job postings, or public references) as realistic targets for a dependency-confusion attempt in a research/authorized context.

- Internal package naming conventions are frequently discoverable via the exact OSINT techniques from Advanced Reconnaissance and OSINT — leaked internal references, public build logs, or job postings
- A researcher publishing a benign, telemetry-only "proof of confusion" package (with responsible, pre-arranged authorization) is the standard, real-world way this class of finding gets reported and fixed

### Build provenance and artifact signing (SLSA, Sigstore)

The emerging structural defense: cryptographically verifiable claims about exactly how and where an artifact was built (SLSA provenance) plus keyless, transparency-logged artifact signing (Sigstore/cosign) so a consumer can verify an artifact actually came from the expected pipeline, not just that it has the expected name and version.

- SLSA defines graduated levels of build-pipeline trustworthiness (from basic provenance metadata up to fully verified, tamper-resistant build processes) — a maturity model a real organization can adopt incrementally
- Sigstore's keyless signing model reuses PKI/trust-chain concepts directly from Cryptography Fundamentals, substituting a transparency log and short-lived certificates for long-lived private keys developers would otherwise have to protect indefinitely

### Reproducible builds

The strongest structural guarantee available: if a build process is fully deterministic, any third party can independently rebuild from the same source and cryptographically verify the published artifact matches — meaning a compromised build pipeline that silently injects malicious code becomes detectable by comparison, not just by trust.

- Reproducibility is a genuinely hard engineering property (compiler timestamps, build-path embedding, and non-deterministic dependency resolution all break it by default) — real projects that achieve it treat it as an ongoing discipline, not a one-time setting
- Reproducible builds and SLSA/Sigstore are complementary, not competing: provenance says who built it and how; reproducibility lets anyone independently check that claim

## Practical Outputs

!!! success "Practical outputs"

    - A simulated build-pipeline compromise in your own lab (a CI configuration you deliberately weaken, e.g. an overprivileged runner credential or an unpinned third-party action) exploited to demonstrate a malicious artifact being produced and shipped through an otherwise-normal-looking pipeline run.
    - A responsible, pre-authorized dependency-confusion research exercise: identify a plausible internal package name via OSINT techniques (against your own organization or a permitted target) and document the finding through the correct responsible-disclosure channel — never squatting a real target's name without authorization.
    - A working SLSA-provenance-and-Sigstore-signing integration for one of your own published tools (from Tool Building and Publishing), with a consumer-side verification step demonstrated actually rejecting a tampered/unsigned artifact.
    - A written case study of a real historical supply-chain attack, analyzed specifically through the build-pipeline-compromise lens from this subject's first topic, distinct from the incident-summary level of Software Composition Analysis's earlier case-study output.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "Supply chain security is just dependency scanning." Scanning addresses known-vulnerable code already in a dependency; it does nothing against a compromised pipeline injecting new malicious code into an otherwise-legitimate artifact.
    - "Signing an artifact proves it's safe." Signing proves provenance (who/what produced it) — it says nothing about whether the build pipeline itself was compromised at the moment of signing, which is exactly why provenance and reproducibility are complementary, not substitutes for each other.
    - "This is only relevant to huge, high-profile open-source projects." Any organization's internal build pipeline is exactly as viable a target, and often far less scrutinized than a popular public package's.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Walk through your simulated build-pipeline compromise end to end, identifying the specific weakness that enabled it.
    - Explain the precise difference between what SLSA provenance and what reproducible builds each independently guarantee.
    - Demonstrate a consumer correctly rejecting a tampered artifact via your Sigstore verification setup, live.
    - Present your historical supply-chain case study through the build-pipeline-compromise lens specifically, not just as a narrative summary.
