---
title: "Bash and Python for Security"
description: "The tooling layer underneath everything else in this roadmap — concurrent sockets, binary packing, subprocess handling that doesn't open a second vulnerab…"
---
# Bash and Python for Security

*Stage 0: Foundations Reset · Subject 6 of 6 · Full depth subject*

> The tooling layer underneath everything else in this roadmap — concurrent sockets, binary packing, subprocess handling that doesn't open a second vulnerability while closing the first, and the Burp-adjacent HTTP fuzzing primitives you will otherwise depend on a GUI for forever.

## What you will build

- **Exercise 00 — subenum0.** Description **Description.** A concurrent subdomain enumerator: given a domain and a wordlist, resolves each candidate subdomain and reports which exist, with real concurrency and real rate control — not a naive serial loop with a library doing the DNS work for you.
- **Exercise 01 — bannergrab0.** Description **Description.** A tool that scans a CIDR range for a set of common ports, grabs service banners (including a TLS-wrapped banner where relevant), and identifies services from the banner text into a structured report — the connect-and-read pattern underneath every recon tool's "service detection" feature.
- **Exercise 02 — httpfuzz0.** Description **Description.** A stripped-down HTTP fuzzer: takes a request template with a marked injection point and a payload wordlist, sends every payload, and flags responses that differ meaningfully from a measured baseline — by status, length, and timing — the exact mechanism behind Burp Intruder's "Grep/Extract" and response-diffing.
- **Capstone — reconpipe.** Description **Description.** A single pipeline that takes one domain and, unattended, runs subdomain enumeration, then banner-grabs every discovered live host, then fuzzes any discovered HTTP endpoints with a small default payload set for anomalies — producing one structured, prioritized attack-surface report with zero manual steps between stages.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [SQL and Database Internals](../05-sql-db-internals/index.md).
