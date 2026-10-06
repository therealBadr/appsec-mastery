---
title: "Cryptography Fundamentals for AppSec"
description: "Not implementing your own crypto — using real primitives correctly, and knowing exactly where a system's security actually lives: not in the algorithm nam…"
---
# Cryptography Fundamentals for AppSec

*Stage 1: Security Fundamentals · Subject 2 of 7 · Full depth subject*

> Not implementing your own crypto — using real primitives correctly, and knowing exactly where a system's security actually lives: not in the algorithm name, but in key management, mode of operation, and the trust chain that tells you whose key you're even looking at.

## What you will build

- **Exercise 00 — aeadmatters.** Description **Description.** A file-encryption tool built correctly first (AES-GCM, random nonce per message, authenticated), then deliberately broken one safeguard at a time — nonce reuse, no authentication tag check, ECB mode — with each break demonstrated as a real, working attack, not just described.
- **Exercise 01 — hashpurpose0.** Description **Description.** A password-storage comparison tool that hashes the same wordlist under a fast general-purpose hash (SHA-256) versus a purpose-built password hash (bcrypt/Argon2), measures and demonstrates the real-world cracking-speed gap, and produces a written explanation of exactly why "hashing" is not one undifferentiated concept.
- **Exercise 02 — chaininspect.** Description **Description.** Extends the TLS chain work from Networking Depth into full manual signature verification: for a real certificate chain, verify each certificate's signature against its issuer's public key using raw cryptographic operations, and demonstrate what breaks when a chain doesn't actually terminate in a trusted root.
- **Capstone — cryptoreview.** Description **Description.** A static analysis tool that scans a codebase for the crypto-misuse patterns this subject covers — ECB mode, hardcoded keys/IVs, fast hashes used for passwords, missing authentication, weak/no salt, disabled certificate verification — and produces a reviewer-grade report with the exact line, the specific risk, and the correct fix.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [Authentication and Session Security](../01-auth-session-security/index.md).
