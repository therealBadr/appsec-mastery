---
title: "Race Conditions and Business Logic Abuse"
description: "The closing Stage 2 subject, and the one hardest to find with any scanner: bugs that exist only in the gap between two requests arriving close together, o…"
---
# Race Conditions and Business Logic Abuse

*Stage 2: Hands-On Web Security and Code Review · Subject 7 of 7 · Full depth subject*

> The closing Stage 2 subject, and the one hardest to find with any scanner: bugs that exist only in the gap between two requests arriving close together, or in a workflow an attacker can reorder, skip a step of, or repeat — nothing here is a malformed payload, every request is individually well-formed.

## What you will build

- **Exercise 00 — couponrace0.** Description **Description.** A deliberately vulnerable single-use discount-code redemption endpoint, exploited via a classic TOCTOU (time-of-check-to-time-of-use) race: fire many redemption requests for the same code at once and redeem it far more than once.
- **Exercise 01 — workflowbypass0.** Description **Description.** A multi-step business workflow (e.g.
- **Capstone — racefuzz.** Description **Description.** A concurrency-fuzzing harness: given a set of candidate endpoints (especially ones involving limited resources — codes, tokens, inventory counts, single-use actions), automatically fires calibrated concurrent bursts at each and statistically detects race-condition windows by comparing observed outcomes (e.g.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [Burp Suite Mastery and the PortSwigger Gauntlet](../06-burp-mastery-portswigger/index.md).
