---
title: "SQL and Database Internals"
description: "Go under the ORM and the ?"
---
# SQL and Database Internals

*Stage 0: Foundations Reset · Subject 5 of 6 · Full depth subject*

> Go under the ORM and the ? placeholder to where a query actually becomes a parse tree — because SQL injection is not a list of payloads to memorize, it is what happens when user input crosses from data into syntax at parse time.

## What you will build

- **Exercise 00 — manualsqli0.** Description **Description.** A minimal login endpoint built with raw string-concatenated SQL, exploited entirely by hand to bypass authentication, with the exact parse-tree-level explanation of why each payload works.
- **Exercise 01 — unionharvest.** Description **Description.** A UNION-based injection against a vulnerable search/listing endpoint, manually extracting the database version, full schema (table and column names via `information_schema`), and table contents — entirely by hand.
- **Exercise 02 — paramfix.** Description **Description.** Every vulnerable query from Exercise 00 and 01 rewritten as a parameterized query, with your own Exercise 00/01 exploits re-run against the fixed version and proven to fail — plus a from-first-principles explanation of why parameterization actually closes the hole.
- **Capstone — blindextract.** Description **Description.** A tool that extracts data from a SQL injection point that returns no visible output and no verbose errors — using boolean-based blind and time-based blind techniques, both implemented as a generic binary-search character extractor against any injectable parameter you point it at.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [OS Internals](../04-os-internals/index.md).
