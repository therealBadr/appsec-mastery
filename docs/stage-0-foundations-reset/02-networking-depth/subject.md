---
title: "The Subject"
description: "Read, construct, and interrogate every protocol between a URL and a socket — Ethernet through TLS — until nothing on the wire is a black box, and prove it…"
---
# Networking Depth: The Subject

*Subject 2 of Stage 0 — Foundations Reset · Version 1.0 — August 2026*

> Read, construct, and interrogate every protocol between a URL and a socket — Ethernet through TLS — until nothing on the wire is a black box, and prove it by detecting real attacks against a network you built.

## Chapter 00 — Foreword

> *The wire doesn't lie about where a packet has been. It only lies about where it's going.*

Every protocol below was designed by someone solving a real problem under real constraints. You will not understand why TLS looks the way it does, or why DNS trusts almost nothing, until you have built a smaller, worse version of each yourself and watched it break.

## Chapter I — Introduction

This subject moves from "I can read a Wireshark capture" to "I can write the thing that produced the capture, and separately, the thing that would have caught the attack hiding inside it." You will build protocol implementations from raw sockets — no `scapy`, no `nmap`, no `dnspython` — and end by building a passive sentinel that has to understand every layer at once, live, on a network you constructed yourself.

## Chapter II — General Instructions

**II.1** **Evaluation environment.** Exercises 00–04 may be evaluated against hosts you own or explicitly-authorized public infrastructure (e.g. your own domain's authoritative nameservers, your own bastion VPS). The Chapter IV capstone requires an **isolated lab network** you control end to end — a local hypervisor (VirtualBox/KVM/libvirt) with 2–3 VMs on a host-only or internal-only virtual network, or an equivalent private cloud VPC segment. Active Layer 2/3 attacks (ARP poisoning, rogue DHCP) must never touch a network you do not own or administer.

**II.2** **Scope and legality.** Every active technique in this subject (scanning, spoofing, poisoning, rogue services) is authorized only against infrastructure you personally own or a lab you built for this purpose. None of it is authorized against a third party, an employer's network, a coffee-shop Wi-Fi, or "just to see what happens." This is a hard boundary, not a suggestion.

**II.3** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input, an unreachable host, or unexpected protocol responses. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.4** **Norm (code-quality baseline), applies to every exercise.** Functions do one thing and are named for what they do. No magic numbers — ports, timeouts, protocol constants (flag bits, record types, opcode values) are named constants, never bare literals. No block of code you cannot explain, unprompted, line by line, during defense. Every non-obvious line carries a comment explaining why, not what.

**II.5** **Global forbidden list.** Unless an exercise explicitly says otherwise: no `scapy`, `dpkt`, `pyshark`, `nmap`, `hping3`, `masscan`, `dnspython`, or any library that performs the exercise's core protocol parsing or construction for you. Reading their source for ideas is allowed. Depending on them at runtime for the graded logic is not. The standard library's `socket`, `struct`, and `ssl` modules are always allowed unless an exercise restricts them further.

**II.6** **Evidence, not assertions.** Every claim of the form "this detects X" or "this parses Y correctly" must be backed by a reproducible capture, transcript, or log — captured in your turn-in. Assertions without evidence are treated as unmet requirements during defense.

**II.7** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct. A single mandatory-part flaw — even a minor one — zeroes the bonus evaluation for that exercise, no exceptions.

## Chapter III — Mandatory Part

### Exercise 00 — wireshark_deepdive

- **Turn-in dir:** networking_depth/ex00/
- **Files:** captures/\*.pcapng, ANALYSIS.md
- **Allowed:** Wireshark/tshark, your own traffic only
- **Forbidden:** third-party capture files, unannotated screenshots

**Description.** Capture and fully annotate five real scenarios of your own traffic, at the packet level, published as a single reviewable writeup with the raw captures attached.

!!! success "Mandatory"

    - Five captures, each isolated to the scenario: (1) a DNS lookup, (2) a plaintext HTTP request, (3) a full HTTPS/TLS handshake, (4) an SSH connection setup, (5) a **deliberately caused failed TCP connection** (e.g. connecting to a closed port you control) — the failure must be one you engineered, not one you stumbled into.
    - Every packet in every capture annotated with: OSI layer(s) involved, relevant header fields and their actual values (not paraphrased), and what would be visible to an on-path observer versus what is encrypted.
    - The TCP handshake and failed-connection captures must have every flag (SYN/ACK/RST/FIN) and every sequence/acknowledgment number annotated, with an explanation of why the ack number is always "their seq + 1" and what would happen if an attacker could predict or inject a sequence number at that point in the handshake.
    - The TLS handshake capture must identify, from the raw bytes, the ClientHello's SNI extension and the ServerHello's negotiated cipher suite and TLS version — read from the packet, not asserted from memory.

!!! failure "Forbidden"

    - Screenshots without the underlying `.pcapng` file attached for independent verification.
    - Captures of third-party traffic that is not yours to publish.
    - Annotations copied from a tutorial's example capture instead of your own.

!!! note "Norm"

    See §II.4, plus: one markdown section per scenario, consistent structure (capture → annotated field table → narrative explanation).

!!! tip "Bonus"

    A sixth capture of a NAT'd connection (client behind NAT to a public server) with an explanation of exactly what the server sees versus what the client's LAN sees.

### Exercise 01 — portscan0

- **Turn-in dir:** networking_depth/ex01/
- **Files:** portscan0.py, README.md
- **Allowed:** raw sockets, socket, struct, standard library only
- **Forbidden:** scapy, nmap, masscan, hping3, python-nmap

**Description.** A port scanner built entirely on raw sockets that performs TCP SYN scanning, TCP connect scanning, and UDP scanning, with banner grabbing and TTL-based OS fingerprinting, distinguishing open/closed/filtered with the same precision a real scanner needs.

!!! success "Mandatory"

    - TCP SYN scan: hand-construct the IP and TCP headers (including checksum computation), send a raw SYN, and classify the target port by the exact response — SYN/ACK means open, RST means closed, no response after a defined timeout means filtered. No connection is ever completed (no ACK sent back on open ports) — a true half-open scan.
    - TCP connect scan: full three-way handshake via the standard `connect()` syscall, as a slower/louder comparison mode.
    - UDP scan: send an empty or protocol-appropriate probe, classify as open (response received), closed (ICMP port-unreachable received — you must parse the ICMP message to determine this), or open|filtered (no response after timeout — and your writeup must explain why UDP scanning can never fully disambiguate this case without a protocol-aware probe).
    - Banner grabbing on discovered open TCP ports (read the first response bytes after connecting).
    - TTL-based OS fingerprinting: read the IP TTL of response packets, compare against a signature table you built (e.g. default TTLs for Linux/Windows/network gear) accounting for hop-count decrement, and report a best-guess OS family with your confidence reasoning.
    - A written section explaining the source-IP-spoofing concept: why a SYN scan cannot practically be run with a spoofed source address if you need to see the response, and what that implies about blind spoofing attacks against TCP's handshake in general.

!!! failure "Forbidden"

    - scapy, nmap, masscan, hping3, or any wrapper around them.
    - Hardcoding checksum values instead of computing them from the actual header bytes.
    - Treating "no response" identically for TCP filtered and UDP open|filtered without acknowledging, in code and in writing, that they are different levels of uncertainty.

!!! note "Norm"

    See §II.4, plus: header construction, checksum computation, response classification, and fingerprinting each in their own function; no protocol constant as a bare literal.

!!! tip "Bonus"

    Parallel scanning with correct raw-socket response demultiplexing (matching responses back to the probe that caused them under concurrent sends); IPv6 support.

### Exercise 02 — dnsresolve0

- **Turn-in dir:** networking_depth/ex02/
- **Files:** dnsresolve0.py, README.md
- **Allowed:** socket (UDP/TCP), struct, standard library only
- **Forbidden:** dnspython, any DNS parsing/query library

**Description.** A DNS resolver that performs true iterative resolution starting from a root nameserver — no upstream recursive resolver involved at any point — constructing and parsing every packet by hand.

!!! success "Mandatory"

    - Starts from a hardcoded root nameserver IP, sends a manually-constructed binary DNS query (correct header, question section, ID, flags), and performs **iterative resolution**: follow each referral (root → TLD → authoritative) yourself by parsing the Authority/Additional sections, never asking a resolver to do the walk for you.
    - Supports at minimum record types A, AAAA, MX, TXT, NS, and CNAME — correctly following a CNAME chain to its final answer.
    - Handles the TC (truncated) flag by re-issuing the same query over TCP with the correct length-prefix framing.
    - Handles NXDOMAIN and SERVFAIL responses distinctly and reports them clearly rather than crashing or returning an empty result indistinguishable from "no such record type."
    - A written explanation, in your own words, of the difference between recursive and iterative resolution and which role your tool is playing at each step (it iterates on the caller's behalf, which is what makes it "a recursive resolver" from the outside while performing iteration internally — you must be able to explain why both terms are correct from different vantage points).

!!! failure "Forbidden"

    - Sending the query to `8.8.8.8`, your OS resolver, or any recursive resolver at any point — that defeats the entire exercise.
    - dnspython or any library that parses/constructs DNS packets for you.
    - Silently returning an empty result on NXDOMAIN instead of reporting it as NXDOMAIN specifically.

!!! note "Norm"

    See §II.4, plus: packet construction, packet parsing, referral-following, and TCP-fallback each isolated in their own function; DNS header flag bits accessed via named bitmasks, never magic hex.

!!! tip "Bonus"

    EDNS0 support (OPT record) with a larger UDP payload size advertised; basic negative-caching of NXDOMAIN responses per TTL.

### Exercise 03 — tlsinspect

- **Turn-in dir:** networking_depth/ex03/
- **Files:** tlsinspect.py, README.md
- **Allowed:** ssl, socket standard library modules
- **Forbidden:** sslyze, testssl.sh, or any wrapper around them

**Description.** Connects to any HTTPS host and produces a full trust and configuration report — chain, validity, SANs, cipher suite, TLS version, SNI/ALPN — with the chain of trust verified by your own logic, not solely by asking the library "is this valid?"

!!! success "Mandatory"

    - Connects using the SNI extension explicitly set to the target hostname, and reports the negotiated ALPN protocol.
    - Retrieves and displays the full certificate chain: subject, issuer, validity window, SANs, signature algorithm, key type/size, for every certificate in the chain, not just the leaf.
    - Verifies the chain **yourself**: each certificate's signature checked against its issuer's public key, terminating at a certificate present in your local trust store — not solely by calling a single "verify" method and trusting its boolean output without being able to explain each link.
    - Performs SAN/CN hostname matching yourself, including correct wildcard matching rules (`*.example.com` matches `foo.example.com`, not `foo.bar.example.com`).
    - Flags, explicitly, each of: self-signed leaf, expired certificate, SHA-1 (or weaker) signature algorithm anywhere in the chain, and TLS version below 1.2 offered or negotiated.
    - Reports the negotiated cipher suite and TLS protocol version as read from the actual handshake, with a plain-language note on what "negotiated" means (client offers a list, server picks one — not the other way around).

!!! failure "Forbidden"

    - Reporting `ssl.get_server_certificate()`'s success as your only chain validation without independently walking and verifying the chain.
    - sslyze, testssl.sh, or any existing TLS-audit tool wrapped and relabeled.
    - Ignoring intermediate certificates and only reporting on the leaf.

!!! note "Norm"

    See §II.4, plus: connection setup, chain retrieval, chain verification, hostname matching, and misconfiguration flagging each in their own function.

!!! tip "Bonus"

    OCSP stapling detection and interpretation; a batch mode scanning a list of hosts and producing a comparison table.

### Exercise 04 — how_dns_actually_works

- **Turn-in dir:** networking_depth/ex04/
- **Files:** README.md (published externally), captures/
- **Allowed:** your own domain/zone, your own captures
- **Forbidden:** AXFR attempts against domains you don't control

**Description.** A published, evidence-backed writeup walking every step from typing a URL to holding an IP address — deep enough to also cover the DNS attack surface (zone transfers, rebinding, and DoH) with real captures, not diagrams copied from elsewhere.

!!! success "Mandatory"

    - Full walkthrough, with real Wireshark screenshots and referenced `.pcapng` captures, from URL entry to resolved IP: browser/OS cache check, stub resolver, recursive resolver, root → TLD → authoritative referral chain, final answer, and TTL-driven caching.
    - A zone-transfer (AXFR) attempt against an authoritative nameserver **you control** for a domain/zone you own, showing a properly configured server refusing the transfer, with the exact response captured and explained.
    - A constructed DNS-rebinding walkthrough in your own lab: a record with a short TTL that first resolves to a public IP and then, on re-query after TTL expiry, resolves to a private/loopback address — captured and explained as the mechanism, with a note on what mitigations (DNS pinning, host header validation) defeat it.
    - A captured comparison of the same query performed as plaintext DNS (UDP/53) versus DNS-over-HTTPS, with an explanation of exactly what an on-path observer can and cannot see in each case.
    - Published externally (GitHub or personal site).

!!! failure "Forbidden"

    - AXFR attempts against any domain you do not own or administer.
    - Diagrams or explanations lifted from other blogs/tutorials without independent verification via your own captures.
    - Treating DoH as "encryption for the query" without addressing what it does *not* hide (e.g. SNI in the subsequent TLS connection, unless ECH is also used — which you should mention as the next layer of the problem).

!!! note "Norm"

    See §II.4, plus: consistent structure (concept → capture → narrative → implication) per section.

!!! tip "Bonus"

    A comparable capture of DNS-over-TLS (port 853) alongside DoH; a short section on Encrypted Client Hello (ECH) and what it additionally hides.

## Chapter IV — Capstone

!!! warning "Read this first"

    **Lab-only.** Every attack scenario demonstrated in this capstone must be run inside the isolated lab described in §II.1/§II.2. Never against a network you don't own or administer.

!!! info "How this capstone forces everything together"

    **This exercise forces together** the OSI model as a working analysis framework, full TCP mechanics (handshake, sequence/ack tracking, flags, state), IP-layer behavior (fragmentation, TTL, spoofing reasoning), UDP and amplification patterns, ARP and ARP poisoning, the full DHCP DORA lifecycle plus starvation and rogue-server detection, DNS depth (including zone-transfer and rebinding detection live on the wire), ICMP types/codes and tunneling detection, subnetting/CIDR-aware segmentation reasoning, NAT and attribution caveats, TLS handshake-level parsing, and the practical reason HTTPS/HSTS defeats on-path MITM. No exercise above touches more than two or three of these; `netwatch` requires understanding essentially the entire theory list simultaneously to correctly interpret one live capture. Someone who only knows DNS cannot parse the ARP and DHCP traffic on the same wire. Someone who only knows TCP/IP headers has no way to recognize a DNS-rebinding response or a TLS downgrade. The tool doesn't work — doesn't even start correctly classifying traffic — on partial knowledge.

### Capstone — netwatch

- **Turn-in dir:** networking_depth/capstone/
- **Files:** src/, topology.md, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** Build `netwatch`: a passive network sentinel that sniffs a live interface, hand-parses every layer from Ethernet through DNS/TLS without any packet-crafting library, and detects a defined set of multi-layer network attacks in real time, tagging every finding by OSI layer and by subnet/NAT context. Demonstrate it against real attack traffic you generate in your own isolated lab.

!!! success "Mandatory"

    - Raw packet capture (`AF_PACKET`/raw socket on Linux) with all parsing — Ethernet, ARP, IP (including fragment reassembly), TCP, UDP, ICMP, DNS, and TLS ClientHello/ServerHello — implemented by hand from the raw bytes. No `scapy`/`dpkt`/`pyshark` anywhere in the parsing path.
    - **TCP flow tracker**: maintains per-flow state (SYN_SENT → SYN_RECEIVED/ESTABLISHED → FIN/RST variants) from observed packets; uses sequence/ack tracking to flag anomalies such as unexpected RST injection or out-of-window sequence numbers.
    - **IP layer module**: reassembles fragmented packets (including out-of-order fragment arrival), tracks per-source-IP TTL and flags inconsistent TTL from the same source address as a possible spoofing indicator, and is configured with an expected CIDR baseline — any traffic violating your defined subnet boundaries (e.g. an unexpected source on the internal segment, or an RFC1918 address leaking onto the external-facing interface) is flagged as a segmentation violation.
    - **UDP amplification module**: tracks request/response size ratio for known amplification-capable services (DNS, NTP, memcached, etc.) and flags any ratio above a configurable threshold.
    - **ARP module**: tracks IP-to-MAC bindings observed on the wire; flags conflicting bindings for the same IP (the ARP-poisoning signature) and unsolicited ARP replies.
    - **DHCP module**: parses the full DORA sequence (Discover/Offer/Request/Ack); flags more than one distinct server address issuing OFFERs (rogue DHCP) and abnormal DISCOVER volume from many distinct MACs in a short window (starvation).
    - **DNS module**: classifies observed record types; flags AXFR requests/responses; flags rebinding indicators (short-TTL A record whose answer is a private/loopback address).
    - **ICMP module**: parses type/code; flags anomalous payload size/pattern relative to standard echo traffic as a tunneling indicator.
    - **TLS module**: parses ClientHello/ServerHello without decrypting; extracts SNI, ALPN, offered/negotiated version and cipher suite; flags a version/cipher **downgrade** relative to a known-good baseline capture you provide.
    - Every finding in the output is tagged with the OSI layer(s) involved and an explicit NAT/attribution caveat where the true origin cannot be determined from this vantage point alone.
    - Demonstrated end to end in your own isolated lab (documented topology required) with real evidence for **every** module: an ARP-poisoning attempt, a rogue DHCP server, a DHCP starvation burst, a UDP amplification pattern, a DNS zone-transfer attempt, a DNS-rebinding pattern, an ICMP tunneling pattern, a fragmented-packet evasion attempt, and a TLS downgrade attempt — each with a capture and the corresponding detection log entry.
    - A final live demonstration: from an ARP-poisoned on-path position in your lab, attempt to intercept traffic to (a) a plain HTTP site — succeeds, captured — and (b) an HSTS-preloaded HTTPS site — fails, captured — with a written explanation of exactly why HSTS defeats the downgrade your on-path position would otherwise allow.

!!! failure "Forbidden"

    - `scapy`, `dpkt`, `pyshark`, or any packet-crafting/parsing library anywhere in the capture or parsing path.
    - Existing IDS/IPS engines (Zeek, Suricata, Snort) doing the detection logic for you — reading their detection-rule documentation for ideas is fine, depending on their engine is not.
    - Running the attacks themselves with your own hand-rolled attacker tooling is **not required** — you may use an existing tool (e.g. `arpspoof`, a rogue DHCP daemon) purely to generate attacker-side traffic for testing, since building attacker tooling is out of scope for a defensive project. The detection logic must still be entirely yours.
    - Silently dropping a packet type your parser doesn't recognize instead of logging it as unclassified.
    - Claiming a detection "works" without the paired capture + log-entry evidence for that specific module.

!!! note "Norm"

    See §II.4, plus: one module per protocol/attack class, each independently testable against a static capture file; no protocol magic numbers (flag bits, DHCP message types, DNS opcodes, TLS content types) without named constants; a single top-level dispatcher that routes parsed packets to the relevant modules, not one function doing everything.

!!! tip "Bonus (§II.7)"

    Run `netwatch` itself as an unprivileged process holding only `CAP_NET_RAW` instead of root, tying back to the Linux Administration Depth capstone's capability-minimization principle; a live terminal dashboard; DNS-over-HTTPS traffic classification (distinguishing it from regular HTTPS by heuristic, since it's not distinguishable by port alone).

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
networking_depth/
├── ex00/
├── ex01/
├── ex02/
├── ex03/
├── ex04/
└── capstone/
```

Each exercise is defended live. For Exercises 01–03 the evaluator supplies or selects the target (their own test host/domain) live and expects your tool to behave exactly as specified — no pre-baked output. For the capstone, the evaluator may generate additional attack traffic in your lab beyond the scenarios you demonstrated and expects a correctly-tagged finding or an honest "not covered by this module" — silence on a real attack is a failure, a wrong classification is a failure, a crash is an automatic fail regardless of anything else working.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — wireshark_deepdive

**Defense questions**

1. Pick the TCP handshake capture — walk me through the exact seq/ack values across all three packets and explain what "their seq + 1" means at each step.
2. In the failed-connection capture, what flag(s) came back, and what does that specifically tell you versus a timeout with no response at all?
3. Show me the SNI value in the TLS capture, byte-level, in the actual hex dump — not just what your annotation claims.
4. What is visible to an on-path observer in the HTTPS capture versus the HTTP capture — be exact about what's still visible even though it's "encrypted" (e.g. SNI pre-ECH, packet sizes/timing).
5. Why does the DNS lookup capture use UDP, and under what condition would you expect to see it retried over TCP in a live capture?

### A.1 — portscan0

**Defense questions**

1. Show me the raw IP+TCP header your SYN scan constructs, byte by byte — where's the checksum computed, and prove it's actually computed, not hardcoded.
2. Run a SYN scan against a filtered port live — how do you distinguish "filtered" from "closed" from "the packet got lost on the wire," and what's your actual timeout logic?
3. Your UDP scan gets no response on a port — is it open or filtered? Be honest about what you cannot know, and explain why a protocol-aware probe would resolve it.
4. Why can't you practically run this SYN scan with a spoofed source address and still see results? What does that imply about blind TCP session hijacking?
5. Show your TTL fingerprinting table — where did these baseline values come from, and how many hops does your test target sit behind, and how did you account for that in your guess?

### A.2 — dnsresolve0

**Defense questions**

1. Show me, live, your query going to the actual root server IP — not `8.8.8.8`, not your OS resolver.
2. Walk me through a referral response — where in the packet is the next nameserver's address, Authority or Additional section, and why does that distinction matter for your parser?
3. Resolve a name with a CNAME chain — show each hop your resolver follows and where that's happening in your code.
4. Force a truncated response — show the TC flag being read and the TCP retry actually happening.
5. Is your resolver "recursive" or "iterative"? Defend both answers from different vantage points.

### A.3 — tlsinspect

**Defense questions**

1. Walk me through your chain verification — pick the intermediate certificate and show me exactly how you checked its signature against the root's public key.
2. Show a wildcard SAN and prove your matching logic handles it correctly including a case where it should NOT match.
3. Point it at a self-signed host — what specifically triggers your flag, and what would a naive implementation relying only on `ssl.verify_mode` have missed?
4. What's the actual difference between what the client offers and what gets negotiated — show me both in your output for a real connection.
5. Point it at a TLS 1.0-only host if you can find or stand one up — what happens, and how does your tool represent "the server offered something weak" versus "the connection failed entirely"?

### A.4 — how_dns_actually_works

**Defense questions**

1. Show the AXFR refusal capture — what's in the response that indicates refusal specifically, at the protocol level?
2. Walk through your rebinding lab step by step — what TTL did you use and why did that value matter for the timing of your demonstration?
3. In your DoH-vs-plaintext comparison, what exactly can an on-path observer still learn even with DoH in place?
4. Why is attempting AXFR against a domain you don't control off-limits here, technically and legally?

### A.5 — Capstone: netwatch

**Defense questions**

1. Walk me through OSI-layer tagging for one finding, live — show the actual layers your tool attributes to a flagged DNS-rebinding event and justify each one.
2. Trigger ARP poisoning against your lab right now — show me the conflicting-binding detection fire, and explain what your tool does if the "poisoning" is actually a legitimate DHCP lease migrating a host to a new MAC (e.g. a VM restart) — how do you avoid a false positive there?
3. Show me your IP fragment reassembly with out-of-order fragments — what happens if a fragment never arrives?
4. Your UDP amplification threshold — what is it, why that number, and show me a legitimate large DNS response that does NOT trigger a false positive.
5. Rogue DHCP detection — what's your window for "multiple servers observed," and could two legitimate redundant DHCP servers (a real, intentional HA setup) trigger a false positive? How would you tell them apart, or do you not currently?
6. Show the TLS downgrade detection live — what's your "known-good baseline" and what happens if you never captured one for a given host?
7. Walk through the HSTS-defeats-MITM demonstration — what specifically causes the browser (or your test client) to refuse the downgrade, and what would have happened on the victim's very first-ever connection to that site, before HSTS was cached (or absent HSTS preloading)?
8. A packet arrives that your parser doesn't recognize at all — what happens, and how do I verify it's logged rather than silently dropped?
9. Explain a finding where NAT makes attribution ambiguous — show me the exact caveat your report attaches to it, and why you can't resolve it from this capture point alone.
10. Why raw sockets and hand-rolled parsing instead of just using `scapy` to save weeks of work — what did you actually gain from doing it by hand that matters for a defensive tool like this?

**Test / edge cases**

- [ ] Fragmented IP packet with fragments arriving out of order: reassembled correctly.
- [ ] Fragmented IP packet missing a fragment entirely: does not hang forever, times out and logs an incomplete-reassembly event.
- [ ] Same source IP observed with two different TTLs within a short window: flagged as a possible spoofing indicator.
- [ ] Legitimate large DNS response (e.g. a DNSSEC-signed zone answer) that is large but not attack traffic: does not falsely trigger the amplification module.
- [ ] Two ARP replies for the same IP with different MACs within your detection window: flagged.
- [ ] A host's MAC legitimately changing (e.g. VM restart with a new virtual NIC) is either correctly distinguished from poisoning or the limitation is explicitly documented.
- [ ] Two distinct DHCP servers responding to the same DISCOVER: flagged as rogue DHCP.
- [ ] A burst of DISCOVER messages from many distinct MACs in a short window: flagged as starvation.
- [ ] A DNS response with a short TTL resolving to `127.0.0.1` or a private RFC1918 address: flagged as a rebinding indicator.
- [ ] An AXFR request observed on the wire: flagged regardless of whether the server granted or refused it.
- [ ] An ICMP echo request with an oversized or non-standard payload: flagged as a possible tunneling indicator; a normal `ping` with default payload size: not flagged.
- [ ] A TLS handshake offering only TLS 1.0/1.1 where a prior baseline showed 1.3 available: flagged as a downgrade.
- [ ] A packet type outside all implemented parsers: logged as unclassified, never silently dropped, never crashes the sentinel.
- [ ] Traffic sourced from an RFC1918 address observed on the interface designated "external": flagged as a segmentation/NAT-boundary violation.
