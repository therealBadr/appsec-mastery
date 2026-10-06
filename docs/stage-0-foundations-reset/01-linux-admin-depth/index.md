---
title: "Linux Administration Depth"
description: "Harden, instrument, and defend a real Linux host from first principles — filesystem, permissions, processes, systemd, packet filtering, capabilities, and …"
---
# Linux Administration Depth

*Stage 0: Foundations Reset · Subject 1 of 6 · Full depth subject*

> Harden, instrument, and defend a real Linux host from first principles — filesystem, permissions, processes, systemd, packet filtering, capabilities, and logs — with nothing you cannot personally explain, line by line, while someone is watching.

## What you will build

- **Exercise 00 — bastion0.** Provision a fresh VPS and convert it into a defensible bastion host via a single idempotent script, with every control verified by a live attack you run against your own box — not asserted from memory.
- **Exercise 01 — logsentry.** A pure-Bash CLI that ingests a real auth.log/journalctl stream — including rotated, gzip-compressed history — and surfaces brute-force patterns, ranked offenders, and attack timing.
- **Exercise 02 — procwatch.** A Bash tool that enumerates every process and every listening/established socket purely by reading `/proc`, manually correlating socket inode numbers to owning PIDs via file descriptors.
- **Exercise 03 — suidwatch.** A Bash tool that walks the filesystem, finds every setUID/setGID binary and every world-writable file/directory, classifies each against a real baseline, and produces a risk-annotated report you can defend line by line.
- **Exercise 04 — linux_for_security_engineers.** A published reference document on the Linux permission model, `/proc` internals, local auth internals, and log semantics — rigorous enough that another engineer could learn the material from it alone.
- **Capstone — sentineld.** Build and operate `sentineld`: a systemd-managed daemon, running as a dedicated unprivileged system user with the minimum Linux capabilities required, that continuously detects SSH brute-force patterns, unexpected listening sockets, and setUID/permission drift, and automatically contains detected threats via nftables rules with automatic expiry — with a full structured audit trail.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->
