---
title: "Client-Side Injection: XSS and CSRF"
description: "The two vulnerability classes that exploit the trust a server places in a browser and the trust a browser places in a server — stored, reflected, and DOM-…"
---
# Client-Side Injection: XSS and CSRF

*Stage 1: Security Fundamentals · Subject 6 of 7 · Full depth subject*

> The two vulnerability classes that exploit the trust a server places in a browser and the trust a browser places in a server — stored, reflected, and DOM-based XSS through to a full cookie-theft payload, and CSRF from a crafted page to a defeated synchronizer token.

## What you will build

- **Exercise 00 — xsstriad0.** Description **Description.** Three separate deliberately vulnerable pages — one stored, one reflected, one DOM-based — each exploited to full impact: a working payload that exfiltrates the victim's session cookie to a listener you control, not merely a JavaScript alert.
- **Exercise 01 — csrfstrike0.** Description **Description.** A working CSRF exploit against a real state-changing action (e.g.
- **Capstone — xsscsrf_confirm.** Description **Description.** A context-aware payload tool: given a target injection point, it detects the surrounding HTML/JS/attribute context and the active CSP (if any), generates an appropriately-shaped XSS payload for that specific context, and — for any state-changing endpoint it also finds — automatically generates and tests a CSRF proof-of-concept, confirming both via real out-of-band cal…

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [Server-Side Injection: Command Injection, XXE and SSRF](../05-serverside-injection/index.md).
