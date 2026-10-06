---
title: "Access Control Models and IDOR"
description: "Authentication answers \"who are you.\" Access control answers the much more frequently broken question: \"what are you allowed to touch.\" Build a real RBAC …"
---
# Access Control Models and IDOR

*Stage 1: Security Fundamentals · Subject 4 of 7 · Full depth subject*

> Authentication answers "who are you." Access control answers the much more frequently broken question: "what are you allowed to touch." Build a real RBAC engine, then break a deliberately careless one by walking straight through it — no exploit needed, just a changed ID.

## What you will build

- **Exercise 00 — rbacengine0.** Description **Description.** A small app implementing DAC (owner-only object access) and RBAC (role-gated actions) as a real, centrally-enforced authorization layer — not scattered `if user.role == "admin"` checks copy-pasted into every route.
- **Exercise 01 — idorhunt0.** Description **Description.** A deliberately careless multi-tenant app (you build it, modeled on a real SaaS pattern — e.g.
- **Exercise 02 — functionlevel0.** Description **Description.** Broken Function Level Authorization: discover admin-only or hidden functionality through client-side artifacts (JS source, hidden form fields, API responses that reveal endpoint names) and successfully call it as an unprivileged user — the exact class of bug behind most "hidden admin panel" real-world reports.
- **Capstone — authzfuzz.** Description **Description.** An authorization fuzzer: given a captured set of authenticated requests (a HAR file or Burp export) from multiple roles, systematically replays every request under every other role's session and flags any response that shouldn't have succeeded — turning the manual hunting from Exercises 01-02 into a repeatable matrix test.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [Applied Cryptographic Attacks](../03-applied-crypto-attacks/index.md).
