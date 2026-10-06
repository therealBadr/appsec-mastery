---
title: "Networking Depth"
description: "Read, construct, and interrogate every protocol between a URL and a socket — Ethernet through TLS — until nothing on the wire is a black box, and prove it…"
---
# Networking Depth

*Stage 0: Foundations Reset · Subject 2 of 6 · Full depth subject*

> Read, construct, and interrogate every protocol between a URL and a socket — Ethernet through TLS — until nothing on the wire is a black box, and prove it by detecting real attacks against a network you built.

## What you will build

- **Exercise 00 — wireshark_deepdive.** Capture and fully annotate five real scenarios of your own traffic, at the packet level, published as a single reviewable writeup with the raw captures attached.
- **Exercise 01 — portscan0.** A port scanner built entirely on raw sockets that performs TCP SYN scanning, TCP connect scanning, and UDP scanning, with banner grabbing and TTL-based OS fingerprinting, distinguishing open/closed/filtered with the same precision a real scanner needs.
- **Exercise 02 — dnsresolve0.** A DNS resolver that performs true iterative resolution starting from a root nameserver — no upstream recursive resolver involved at any point — constructing and parsing every packet by hand.
- **Exercise 03 — tlsinspect.** Connects to any HTTPS host and produces a full trust and configuration report — chain, validity, SANs, cipher suite, TLS version, SNI/ALPN — with the chain of trust verified by your own logic, not solely by asking the library "is this valid?"
- **Exercise 04 — how_dns_actually_works.** A published, evidence-backed writeup walking every step from typing a URL to holding an IP address — deep enough to also cover the DNS attack surface (zone transfers, rebinding, and DoH) with real captures, not diagrams copied from elsewhere.
- **Capstone — netwatch.** Build `netwatch`: a passive network sentinel that sniffs a live interface, hand-parses every layer from Ethernet through DNS/TLS without any packet-crafting library, and detects a defined set of multi-layer network attacks in real time, tagging every finding by OSI layer and by subnet/NAT context.

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [Linux Administration Depth](../01-linux-admin-depth/index.md).
