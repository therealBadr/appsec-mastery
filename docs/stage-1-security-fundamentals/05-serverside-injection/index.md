---
title: "Server-Side Injection: Command Injection, XXE and SSRF"
description: "Three vulnerability classes united by one shape: user input crosses a trust boundary into something that interprets it as instructions rather than data — …"
---
# Server-Side Injection: Command Injection, XXE and SSRF

*Stage 1: Security Fundamentals · Subject 5 of 7 · Full depth subject*

> Three vulnerability classes united by one shape: user input crosses a trust boundary into something that interprets it as instructions rather than data — a shell, an XML parser, or the server's own outbound network stack.

## What you will build

- **Exercise 00 — cmdinject0.** Description **Description.** A deliberately vulnerable feature that shells out to a system command with unsanitized user input (e.g.
- **Exercise 01 — xxeharvest0.** Description **Description.** A deliberately vulnerable XML-accepting endpoint (e.g.
- **Exercise 02 — ssrfmeta0.** Description **Description.** A deliberately vulnerable "fetch this URL and show me a preview" feature (a common real-world SSRF source: image proxies, webhook validators, PDF-from-URL generators) exploited to reach internal-only resources, culminating in reading a simulated cloud instance-metadata endpoint for credentials.
- **Capstone — injecttriage.** Description **Description.** A single scanner that, given a target application's endpoints, probes for command injection, XXE, and SSRF using safe, non-destructive out-of-band canary techniques for all three — confirming exploitability through a listener you control rather than causing real damage, the way a responsible engagement actually operates.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [Access Control Models and IDOR](../04-access-control-idor/index.md).
