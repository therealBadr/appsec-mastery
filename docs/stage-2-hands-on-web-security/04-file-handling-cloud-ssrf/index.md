---
title: "File Handling Vulnerabilities and Cloud SSRF"
description: "Every feature that touches a filesystem path or a filename supplied by the user is a potential escape hatch out of the directory the developer imagined."
---
# File Handling Vulnerabilities and Cloud SSRF

*Stage 2: Hands-On Web Security and Code Review · Subject 4 of 7 · Full depth subject*

> Every feature that touches a filesystem path or a filename supplied by the user is a potential escape hatch out of the directory the developer imagined. Every feature that fetches a URL on a server running inside a cloud provider is a potential escape hatch into the provider's own control plane.

## What you will build

- **Exercise 00 — uploadbypass0.** Description **Description.** A file-upload feature defended by three progressively stronger but still-bypassable restrictions — client-side-only validation, then extension blocklisting, then content-type checking — each defeated in turn, ending in an uploaded web shell that actually executes.
- **Exercise 01 — lfi_logpoison0.** Description **Description.** A deliberately vulnerable "include this page fragment by name" feature, exploited for path traversal to read arbitrary local files, then escalated to remote code execution via log poisoning — planting attacker-controlled PHP code inside a log file the vulnerable include can be tricked into including.
- **Exercise 02 — imdsv2_bypass0.** Description **Description.** An SSRF against a target hardened with IMDSv2 (token-required metadata access, specifically designed to defeat simple SSRF) — demonstrating why IMDSv2 stops a naive SSRF but not one with the right request-shape control, and why network-layer restriction remains the real fix.
- **Capstone — filessrf_auditor.** Description **Description.** A single auditor covering file-upload restriction strength, LFI/path-traversal probing, and SSRF-to-cloud-metadata risk assessment (including IMDSv1-vs-v2-aware testing) against a target application — the three exercises' techniques combined into one coherent pre-engagement recon tool.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [Modern API Authorization: BOLA, BFLA, and Rate-Limit Abuse](../03-api-authorization/index.md).
