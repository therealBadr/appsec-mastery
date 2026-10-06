---
title: "HTTP Internals"
description: "Build the protocol by hand, then attack the security semantics layered on top of it — headers, cookies, CORS, CSP, and the auth flows that live or die by …"
---
# HTTP Internals

*Stage 0: Foundations Reset · Subject 3 of 6 · Full depth subject*

> Build the protocol by hand, then attack the security semantics layered on top of it — headers, cookies, CORS, CSP, and the auth flows that live or die by them — until every response your browser trusts is a response you can explain byte by byte.

## What you will build

- **Exercise 00 — httpanatomy0.** Description **Description.** A minimal HTTP/1.1 client and server pair built directly on TCP sockets, handling request/response anatomy, methods, status lines, headers, and both content-length and chunked transfer encoding by hand.
- **Exercise 01 — headersec0.** Description **Description.** A CLI that fetches a URL, follows redirects, and produces a structured, color-coded report of every security-relevant header and cookie flag present, missing, or misconfigured, plus the TLS version/cipher in use.
- **Exercise 02 — cookielab.** Description **Description.** A minimal Flask app with intentionally broken session/cookie security, exploited by hand via Burp/devtools, then fixed field by field with a before/after comparison.
- **Capstone — httpsentinel.** Description **Description.** A single audit tool that combines header/cookie security analysis with CORS misconfiguration testing, CSP bypass reasoning, open-redirect detection, and Host-header-injection probing against a target you own or run locally — producing one structured report an engineering team could act on.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [Networking Depth](../02-networking-depth/index.md).
