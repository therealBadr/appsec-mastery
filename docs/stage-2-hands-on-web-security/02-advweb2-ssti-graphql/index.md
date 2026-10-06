---
title: "Advanced Web Exploitation II: SSTI and GraphQL Security"
description: "A template engine given attacker-controlled template syntax is a code-execution primitive wearing the costume of a rendering bug."
---
# Advanced Web Exploitation II: SSTI and GraphQL Security

*Stage 2: Hands-On Web Security and Code Review · Subject 2 of 7 · Full depth subject*

> A template engine given attacker-controlled template syntax is a code-execution primitive wearing the costume of a rendering bug. A GraphQL API with introspection on and no query-cost limiting is a full schema map handed to an attacker for free, plus a denial-of-service lever built into the query language itself.

## What you will build

- **Exercise 00 — sstichain0.** Description **Description.** A deliberately vulnerable Flask app that renders user input directly as a Jinja2 template string (instead of passing it as data into a template), exploited from initial fingerprinting through full remote code execution via Python's object-introspection chain.
- **Exercise 01 — graphqlrecon0.** Description **Description.** A GraphQL API with introspection enabled and no query-complexity limiting, attacked to fully map its schema without documentation, then abused for a resource-exhaustion denial-of-service via deeply nested/circular queries.
- **Capstone — ssti_graphql_auditor.** Description **Description.** One tool combining SSTI fingerprinting/OOB-confirmed exploitation with a GraphQL security auditor that performs introspection recovery, flags overly permissive/sensitive fields, and estimates query-complexity DoS risk — producing a report spanning both attack surfaces for a target that exposes either or both.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [Advanced Web Exploitation I: Request Smuggling and Deserialization](../01-advweb1-smuggling-deserialization/index.md).
