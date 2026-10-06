---
title: "Modern API Authorization: BOLA, BFLA, and Rate-Limit Abuse"
description: "The API-specific vocabulary for exactly the bugs Access Control and IDOR already taught you to find, plus two failure modes that only really bite once an …"
---
# Modern API Authorization: BOLA, BFLA, and Rate-Limit Abuse

*Stage 2: Hands-On Web Security and Code Review · Subject 3 of 7 · Full depth subject*

> The API-specific vocabulary for exactly the bugs Access Control and IDOR already taught you to find, plus two failure modes that only really bite once an application becomes a JSON API instead of a server-rendered site: mass assignment, and rate limits that exist per-endpoint instead of per-user-intent.

## What you will build

- **Exercise 00 — bola_bfla0.** Description **Description.** A small deliberately vulnerable REST API (e.g.
- **Exercise 01 — massassign0.** Description **Description.** A profile-update endpoint that naively binds the entire request body onto a user object (a common ORM/serializer convenience), exploited to set fields the client-facing form never exposes — including a privilege flag.
- **Exercise 02 — ratelimit_bypass0.** Description **Description.** A naive IP-based rate limiter protecting a login/brute-force-sensitive endpoint, defeated through header-based IP spoofing and a distributed-source simulation — proving that rate limiting keyed on the wrong identity dimension is not real protection.
- **Capstone — apiauthz_suite.** Description **Description.** An OpenAPI-spec-driven authorization test suite: given a target's OpenAPI/Swagger document and credentials for at least two roles, automatically generates and runs the full BOLA/BFLA/mass-assignment/rate-limit-identity test matrix from Exercises 00-02 across every documented endpoint — the systematic coverage from Exercise 00's hand-built table, fully automated and ex…

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [Advanced Web Exploitation II: SSTI and GraphQL Security](../02-advweb2-ssti-graphql/index.md).
