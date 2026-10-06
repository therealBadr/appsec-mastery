---
title: "The Subject"
description: "Two attack classes that live in the gap between what a component believes about a message and what actually happens when a different component parses the …"
---
# Advanced Web Exploitation I: Request Smuggling and Deserialization: The Subject

*Subject 1 of 7 — Hands-On Web Security + Code Review · Version 1.0 — September 2026*

> Two attack classes that live in the gap between what a component believes about a message and what actually happens when a different component parses the same bytes differently — a front-end proxy versus a back-end server, and a serializer versus whatever code runs when the object comes back.

## Chapter 00 — Foreword

> *Request smuggling isn't a bug in either server. It's a disagreement between two servers that both parsed the same bytes correctly, by their own rules.*

HTTP Internals gave you the anatomy of one request between one client and one server. Real infrastructure chains multiple HTTP parsers together — a CDN, a load balancer, an app server — and every parser is free to interpret an ambiguous message its own way. Deserialization has the identical shape one layer up the stack: an object graph reconstructed from bytes, where the reconstruction process itself can be hijacked into doing something the original object never did.

## Chapter I — Introduction

You will build a deliberately mismatched proxy/backend pair and smuggle a request past the front end, exploit insecure deserialization in a Python/Java-style vulnerable endpoint to achieve remote code execution, and chain the two: a smuggled request that reaches an internal deserialization endpoint the front end was supposed to protect. The capstone builds a differential-parsing detector that finds smuggling-prone configurations automatically.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of exploitability or of a fix working must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation targets DVWA, Juice Shop, WebGoat, PortSwigger Academy labs, HackTheBox/lab machines, or an application you wrote — never a third party without written authorization.

## Chapter III — Mandatory Part

### Exercise 00 — smuggle0

- **Turn-in dir:** advweb1_smuggling_deserialization/ex00/
- **Files:** proxy_stack/, EXPLOIT.md, evidence/
- **Allowed:** nginx or a Python proxy you configure/build, raw sockets for crafted requests, Burp
- **Forbidden:** Smuggler or any automated request-smuggling scanner

**Description.** A two-tier proxy/backend stack you deliberately misconfigure to disagree about request boundaries, exploited for CL.TE and TE.CL request smuggling — sending one request that the two tiers parse as a different number of requests.

!!! success "Mandatory"

    - A front-end proxy and a back-end server, each parsing `Content-Length` and `Transfer-Encoding` headers with different precedence (e.g. front end honors `Content-Length` when both are present, back end honors `Transfer-Encoding`) — the deliberate misconfiguration, documented explicitly.
    - CL.TE smuggling: craft a single raw request (built with your own socket code, reusing HTTP Internals' `httpanatomy0`) that the front end forwards as one request but the back end interprets as two, with the smuggled second "request" demonstrated landing in a subsequent, unrelated victim's response (a classic response-queue-poisoning proof) or at minimum reaching an endpoint the front end should have blocked.
    - TE.CL smuggling: the reverse misconfiguration, with an equivalent working exploit.
    - A packet/byte-level walkthrough (reusing your Wireshark annotation skill from Networking Depth) showing exactly where the two tiers' interpretations diverge — the literal byte offset at which "this is the end of request one" differs between them.
    - The fix applied and verified: reconfigure both tiers to agree (e.g. reject ambiguous requests with both headers present, per RFC 7230's guidance) and show your smuggling payloads failing afterward.

!!! failure "Forbidden"

    - Smuggler, or any existing request-smuggling detection/exploitation tool.
    - A "smuggled" request you can't explain byte-by-byte in terms of the two tiers' differing parse.
    - Leaving the deliberately vulnerable proxy stack running anywhere reachable beyond your own lab.

!!! note "Norm"

    See §II.2, plus: raw request construction, and the CL.TE and TE.CL payload builders, each isolated.

!!! tip "Bonus"

    A third smuggling variant: TE.TE, where both tiers honor `Transfer-Encoding` but can be tricked into disagreeing about whether a given `Transfer-Encoding` header is even valid (e.g. via an obfuscated value like `Transfer-Encoding: chunked, identity` or embedded whitespace/casing tricks).

### Exercise 01 — deserialize0

- **Turn-in dir:** advweb1_smuggling_deserialization/ex01/
- **Files:** vuln_app.py, EXPLOIT.md, evidence/
- **Allowed:** Python pickle (deliberately, for the vulnerable target), a safe alternative (JSON) for the fix
- **Forbidden:** ysoserial as a black box — reading it for technique ideas is fine, your Python gadget/payload must be your own

**Description.** A deliberately vulnerable endpoint that deserializes attacker-supplied data using an unsafe deserializer (Python `pickle`), exploited for remote code execution via a crafted malicious pickle payload you construct yourself, understanding exactly how deserialization becomes code execution.

!!! success "Mandatory"

    - A vulnerable endpoint that accepts a base64-encoded blob (e.g. a "saved preferences" or "session state" feature) and deserializes it with `pickle.loads()` with no integrity check.
    - A hand-crafted malicious payload exploiting `__reduce__` (or an equivalent object-reconstruction hook) to execute an arbitrary command when the object is deserialized — not merely a data-tampering payload, actual code execution, demonstrated with output (e.g. a planted file created, or an OOB callback reusing your Server-Side Injection listener) proving the command ran on the server.
    - A written, precise explanation of the mechanism: *why* deserialization is fundamentally different from parsing (e.g. JSON) — the deserializer is executing instructions embedded in the serialized stream to reconstruct arbitrary object graphs, and a class's own reconstruction hooks are attacker-reachable code paths the moment attacker-controlled bytes reach the deserializer.
    - A demonstration that a naive mitigation — a blocklist on dangerous-looking bytes in the blob — is bypassable (encode/obfuscate the payload to avoid the specific bytes blocked), reinforcing the same blocklist-fails-structurally lesson from every earlier injection subject.
    - The correct fix applied and verified: replace `pickle` with a data-only format (JSON) for this feature entirely, with your exploit payload shown failing (as invalid JSON, or as inert data with no execution hooks) against the fixed endpoint.

!!! failure "Forbidden"

    - ysoserial or any prebuilt payload-generation tool used as a black box without understanding the generated gadget chain.
    - A payload that only proves data tampering (e.g. changing a stored value) rather than actual code execution.
    - A "fix" that keeps `pickle` but adds a blocklist/signature check as the sole defense — the mandatory fix is architectural (stop deserializing untrusted data with an executable-format deserializer).

!!! note "Norm"

    See §II.2, plus: payload construction and the vulnerable/fixed endpoints each clearly separated.

!!! tip "Bonus"

    Demonstrate the equivalent vulnerability class conceptually in a different ecosystem you research (e.g. Java's `ObjectInputStream` or PHP's `unserialize` with a magic `__wakeup`/`__destruct` method) — a written gadget-chain walkthrough is acceptable here even without a full working exploit, since ysoserial's Java gadget chains are legitimately out of reach without a JVM lab.

### Exercise 02 — smugglechain

- **Turn-in dir:** advweb1_smuggling_deserialization/ex02/
- **Files:** EXPLOIT.md, evidence/
- **Allowed:** your own proxy stack and deserialization endpoint from Ex. 00/01, combined
- **Forbidden:** automated tools for either half of the chain

**Description.** A chained attack: use request smuggling to reach an internal-only deserialization endpoint that the front-end proxy was specifically configured to block from direct external access — proving smuggling's real value is bypassing front-end security controls, not just confusing two servers for its own sake.

!!! success "Mandatory"

    - Configure your Exercise 00 front-end proxy to explicitly block direct external requests to your Exercise 01 deserialization endpoint's path (a realistic control — "this internal endpoint is only reachable by other backend services").
    - Demonstrate the block working: a direct external request to the protected path is rejected by the front end as expected.
    - Construct a smuggled request (reusing Exercise 00's technique) whose smuggled second request targets the protected deserialization path directly against the back end, bypassing the front end's path-based block entirely, and carrying your Exercise 01 malicious payload — demonstrated achieving the same code-execution proof as Exercise 01, but through the smuggled path this time.
    - A written explanation of exactly why path-based access control implemented only at the front-end proxy is insufficient defense in depth, and what would have stopped this chain even with the smuggling vulnerability still present (e.g. the back end also enforcing the restriction, independent of the proxy).

!!! failure "Forbidden"

    - Skipping the "block works when tested directly" step — the chain's significance only lands if the direct path was genuinely blocked first.
    - Any tool automating either half of this chain.

!!! note "Norm"

    See §II.2, plus: the chain is demonstrated as one continuous, reproducible script from smuggled-request construction through observed code execution.

!!! tip "Bonus"

    Add the smuggling fix from Exercise 00 back and show the chain now fails at the smuggling step specifically, isolating exactly which of the two vulnerabilities the fix closed.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** the byte-level request construction from Exercise 00, timing-based inference (the same statistical discipline from Applied Cryptographic Attacks' timing side channel — a smuggling probe that isn't detected via an obvious victim response has to be inferred from response timing instead, since a "hanging" back end waiting for a smuggled request's phantom remaining bytes is a measurable delay), and enough understanding of common serialization formats' magic bytes/headers (Exercise 01) to flag likely deserialization endpoints from the outside without a source-code view. No single exercise above needed statistical timing inference; this capstone does, because the safe, non-destructive way to confirm smuggling against a target you don't control the back end of is to observe timing, not to attempt response-queue poisoning against unknown victims.

### Capstone — smuggledetect

- **Turn-in dir:** advweb1_smuggling_deserialization/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A differential-parsing detector: given a target behind a front-end/back-end stack, systematically probes for CL.TE/TE.CL/TE.TE disagreement using timing-based detection (a technique that works even when there's no obvious response-queue-poisoning victim to observe), and separately fingerprints any reachable endpoint that appears to accept a serialized-object format for potential deserialization risk.

!!! success "Mandatory"

    - CL.TE/TE.CL timing probe: sends a request designed so that, if the target is vulnerable, the back end will hang waiting for bytes that never arrive (a smuggled "request" with a declared body longer than what's sent) — and measures response time against a baseline, using the statistical methodology from Applied Cryptographic Attacks (multiple samples, documented threshold) rather than a single request.
    - TE.TE probe: sends a small set of obfuscated `Transfer-Encoding` header variations and detects behavioral differences suggesting the two tiers disagree on which are valid.
    - Serialized-format fingerprinting: for any endpoint accepting a body, checks for recognizable serialization-format signatures (e.g. a pickle opcode preamble, a Java-serialization magic-byte header `0xACED`, a suspiciously structured base64 blob) and flags it as a candidate deserialization risk worth manual follow-up — explicitly not attempting exploitation automatically, since a wrong guess here risks actually executing an unintended payload against a target you don't fully control.
    - Safety governor: every timing probe is rate-limited and capped in total requests per target, with a hard stop and clear reporting if early probes suggest the target might be produring real, unbounded back-end hangs (a smuggling probe that works can also resemble a mini denial-of-service if run carelessly at volume).
    - One consolidated report: per-target smuggling-likelihood (with confidence from the timing evidence), and any flagged candidate deserialization endpoints — explicitly labeled as requiring manual confirmation, not auto-exploited.
    - Demonstrated against your own Exercise 00 vulnerable and fixed proxy stacks, correctly distinguishing them via timing evidence alone (no response-queue-poisoning victim setup required for detection), plus your Exercise 01 endpoint correctly flagged as a serialization-format candidate.

!!! failure "Forbidden"

    - Smuggler or any existing detection tool.
    - Automatically attempting a deserialization exploit against a fingerprinted candidate endpoint — detection and exploitation are deliberately kept separate here for safety.
    - A probe with no rate limit or request cap that could turn a detection scan into an unintended denial-of-service.

!!! note "Norm"

    See §II.2, plus: timing-probe, TE.TE-probe, and serialization-fingerprint each in their own module with a shared rate-governed request layer.

!!! tip "Bonus (§II.7)"

    A confirmation mode (opt-in, clearly separated from the default safe scan) that, only against your own explicitly-owned lab targets, attempts the full Exercise 00 response-queue-poisoning proof once timing evidence suggests a likely finding.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
advweb1_smuggling_deserialization/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live against your own proxy stack, which the evaluator may reconfigure (swap which header each tier honors) immediately before the defense. The capstone is run live and must justify its confidence level from actual timing evidence shown during the defense, not from a pre-recorded run.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — smuggle0

**Defense questions**

1. Walk through your CL.TE payload byte by byte — show me exactly where the front end and back end disagree.
2. Why does response-queue poisoning make this attack affect victims other than the attacker's own request — trace the mechanism.
3. What single configuration change on both tiers closes CL.TE and TE.CL simultaneously, and why?
4. Why is request smuggling specifically a multi-component infrastructure problem that can't be found by testing either server in isolation?

### A.1 — deserialize0

**Defense questions**

1. Walk through your malicious pickle payload byte by byte, or at minimum opcode by opcode — what does the deserializer actually execute and when?
2. Why is this fundamentally not fixable by "just validating the deserialized data afterward" — where in the process does the damage already happen?
3. Show your blocklist bypass — same lesson as command injection and XSS, in your own words, applied to this class.
4. Why is switching to JSON a complete fix here rather than a mitigation — what capability disappears entirely?

### A.2 — smugglechain

**Defense questions**

1. Run the full chain live: direct block first, then the smuggled bypass achieving code execution.
2. Why does this chain illustrate defense-in-depth failure specifically — name the second, independent control that would have stopped it.
3. Which of the two underlying bugs (smuggling or deserialization) is the "root cause" here, and does fixing only one fully close the chain — defend your answer.

### A.3 — Capstone: smuggledetect

**Defense questions**

1. Run the timing probe against your vulnerable and fixed Exercise 00 stacks live — show the measurable difference and your confidence threshold.
2. Why is timing-based detection the safer default here compared to attempting response-queue poisoning against a target whose other traffic/victims you don't control?
3. Walk through your serialization-format fingerprinting on your Exercise 01 endpoint — what specific bytes triggered the flag?
4. Why does this capstone deliberately not auto-exploit a fingerprinted deserialization candidate — what could go wrong if it did?
5. What's your rate-limit/request-cap policy, and how did you choose the numbers?

**Test / edge cases**

- [ ] A target with naturally high/variable baseline latency: timing probe correctly reports lower confidence rather than a false positive, mirroring the calibration discipline from earlier timing work.
- [ ] A back end that returns an error quickly on a malformed smuggling probe instead of hanging (a partially-hardened target): correctly classified as likely-not-vulnerable, not misread as "inconclusive."
- [ ] A serialization-format false-positive candidate: a base64 blob that's actually just an encoded image or JWT, not a pickle/Java-serialized object: fingerprinting logic specific enough to avoid flagging it, or explicitly documented as a known limitation.
- [ ] Target stops responding entirely mid-scan (real or simulated outage): tool reports the interruption clearly and does not silently mark remaining probes as "not vulnerable."
- [ ] Two different back-end pool members behind a load balancer with different configurations (one patched, one not): tool's behavior/limitation here (result may flap between requests) is explicitly documented rather than presented as one confident answer.
