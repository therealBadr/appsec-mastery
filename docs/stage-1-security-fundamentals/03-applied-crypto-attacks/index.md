---
title: "Applied Cryptographic Attacks"
description: "Four attacks that show up repeatedly in real CVEs and bug bounty reports, executed for real against your own vulnerable targets: the padding oracle, hash-…"
---
# Applied Cryptographic Attacks

*Stage 1: Security Fundamentals · Subject 3 of 7 · Full depth subject*

> Four attacks that show up repeatedly in real CVEs and bug bounty reports, executed for real against your own vulnerable targets: the padding oracle, hash-length-extension, a timing side-channel, and weak-RNG token prediction.

## What you will build

- **Exercise 00 — paddingoracle0.** Description **Description.** A full padding-oracle attack against a deliberately vulnerable CBC-mode endpoint that leaks padding-validity through distinguishable error responses — decrypting an entire ciphertext block by block without ever knowing the key.
- **Exercise 01 — lengthextend0.** Description **Description.** A hash-length-extension attack against a naive `MAC = SHA256(secret || message)` authentication scheme: forge a valid MAC over an attacker-extended message without ever learning the secret, by exploiting the Merlin-Damgård construction directly.
- **Exercise 02 — timingleak0.** Description **Description.** A statistical timing side-channel attack that extracts a secret token character by character purely from measured response-time differences of a non-constant-time string comparison — proving the attack with real measurements and real statistics, not a theoretical description.
- **Capstone — timingbypass.** Description **Description.** A full authentication-bypass chain: use the timing side-channel technique from Exercise 02 to extract a valid API key or session-signing secret from a target application byte by byte, then use that recovered secret to forge a valid authenticated request — proving a timing leak is not an academic curiosity but a direct path to full compromise.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [Cryptography Fundamentals for AppSec](../02-crypto-fundamentals/index.md).
