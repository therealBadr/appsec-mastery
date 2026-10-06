---
title: "Authentication and Session Security"
description: "Every auth scheme is a promise about who a request is from."
---
# Authentication and Session Security

*Stage 1: Security Fundamentals · Subject 1 of 7 · Full depth subject*

> Every auth scheme is a promise about who a request is from. Session cookies, JWTs, OAuth 2.0, and SAML each make that promise differently — and each breaks differently. Build a session store, break a JWT implementation six distinct ways, and walk through a full OAuth 2.0 authorization-code flow by hand.

## What you will build

- **Exercise 00 — sessionstore0.** Description **Description.** A hand-built server-side session store (session ID generation, storage, expiry, and rotation-on-privilege-change) used to back a minimal login flow — so the mechanics a framework usually hides are ones you've implemented and can break.
- **Exercise 01 — jwtbreak0.** Description **Description.** A small JWT-authenticated app with at least three real implementation flaws, exploited entirely by manually constructing forged tokens — base64-decoding, editing, and re-encoding JSON by hand, not through a GUI tool.
- **Exercise 02 — oauthflow0.** Description **Description.** A full OAuth 2.0 authorization-code flow captured and annotated request-by-request through Burp, followed by manual demonstrations of the two most common real-world OAuth bugs: `redirect_uri` manipulation and CSRF via a missing/unvalidated `state` parameter.
- **Capstone — authfingerprint.** Description **Description.** A tool that, given a target login flow, identifies which authentication scheme (server-side session, JWT, or OAuth/SSO redirect) it uses, then runs the appropriate probe set from Exercises 00-02 automatically — session-fixation and rotation checks for session-based auth, algorithm/claim probes for JWTs, and redirect_uri/state checks for OAuth.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->
