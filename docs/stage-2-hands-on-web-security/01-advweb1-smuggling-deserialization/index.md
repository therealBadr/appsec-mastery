---
title: "Advanced Web Exploitation I: Request Smuggling and Deserialization"
description: "Two attack classes that live in the gap between what a component believes about a message and what actually happens when a different component parses the …"
---
# Advanced Web Exploitation I: Request Smuggling and Deserialization

*Stage 2: Hands-On Web Security and Code Review · Subject 1 of 7 · Full depth subject*

> Two attack classes that live in the gap between what a component believes about a message and what actually happens when a different component parses the same bytes differently — a front-end proxy versus a back-end server, and a serializer versus whatever code runs when the object comes back.

## What you will build

- **Exercise 00 — smuggle0.** Description **Description.** A two-tier proxy/backend stack you deliberately misconfigure to disagree about request boundaries, exploited for CL.TE and TE.CL request smuggling — sending one request that the two tiers parse as a different number of requests.
- **Exercise 01 — deserialize0.** Description **Description.** A deliberately vulnerable endpoint that deserializes attacker-supplied data using an unsafe deserializer (Python `pickle`), exploited for remote code execution via a crafted malicious pickle payload you construct yourself, understanding exactly how deserialization becomes code execution.
- **Exercise 02 — smugglechain.** Description **Description.** A chained attack: use request smuggling to reach an internal-only deserialization endpoint that the front-end proxy was specifically configured to block from direct external access — proving smuggling's real value is bypassing front-end security controls, not just confusing two servers for its own sake.
- **Capstone — smuggledetect.** Description **Description.** A differential-parsing detector: given a target behind a front-end/back-end stack, systematically probes for CL.TE/TE.CL/TE.TE disagreement using timing-based detection (a technique that works even when there's no obvious response-queue-poisoning victim to observe), and separately fingerprints any reachable endpoint that appears to accept a serialized-object format fo…

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->
