---
title: "OS Internals"
description: "Cross the line from \"I wrote C that ran\" to \"I know exactly what the kernel and the loader did with the bytes I wrote\" — memory layout, syscalls, the dyna…"
---
# OS Internals

*Stage 0: Foundations Reset · Subject 4 of 6 · Full depth subject*

> Cross the line from "I wrote C that ran" to "I know exactly what the kernel and the loader did with the bytes I wrote" — memory layout, syscalls, the dynamic linker, and the exact mechanics that turn a bounds-checking mistake into a hijacked return address.

## What you will build

- **Exercise 00 — memmap0.** Description **Description.** A C program that prints the runtime address of a stack variable, a heap allocation, a global variable, a function pointer, and an environment variable, then reads and annotates its own `/proc/self/maps` — with and without ASLR — to show the layout matches reality, not just the textbook diagram.
- **Exercise 01 — straceit.** Description **Description.** Trace five different programs with `strace`, and produce a report that reads each trace like a security engineer doing triage — not a transcript with no interpretation.
- **Exercise 02 — stackoverflow0.** Description **Description.** A deliberately vulnerable C program with a stack buffer overflow, compiled with protections off, exploited far enough in GDB to overwrite the saved return address and prove it — plus a written explanation of exactly why each disabled protection was necessary to get there.
- **Capstone — crashtriage.** Description **Description.** A triage tool that takes a crashing binary plus a crashing input, runs it under GDB in batch mode, and automatically classifies the crash — stack overflow vs.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [HTTP Internals](../03-http-internals/index.md).
