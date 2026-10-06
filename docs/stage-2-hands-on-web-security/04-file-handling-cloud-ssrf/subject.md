---
title: "The Subject"
description: "Every feature that touches a filesystem path or a filename supplied by the user is a potential escape hatch out of the directory the developer imagined."
---
# File Handling Vulnerabilities and Cloud SSRF: The Subject

*Subject 4 of 7 — Hands-On Web Security + Code Review · Version 1.0 — September 2026*

> Every feature that touches a filesystem path or a filename supplied by the user is a potential escape hatch out of the directory the developer imagined. Every feature that fetches a URL on a server running inside a cloud provider is a potential escape hatch into the provider's own control plane.

## Chapter 00 — Foreword

> *A path is not a string with a security policy attached. "../" doesn't violate any rule the filesystem enforces — it violates an assumption the developer forgot to check.*

File upload, path traversal, and LFI/RFI are treated as beginner vulnerabilities the same way XSS is, and for the same wrong reason — the proof-of-concept is simple, so people stop there. This subject insists on real impact each time: an uploaded web shell that executes, a traversed path that reads a real secret, and — because this roadmap targets remote-friendly, cloud-native employers — an SSRF that reaches a hardened, IMDSv2-only metadata endpoint the way Exercise 02 of Server-Side Injection deliberately did not yet cover.

## Chapter I — Introduction

You will bypass file-upload restrictions to get a web shell executing, exploit path traversal and local file inclusion (including LFI-to-RCE via log poisoning) against a vulnerable PHP-style include pattern, and defeat IMDSv2's token-based hardening through an SSRF chain that a naive metadata-endpoint block would not catch. The capstone is a file-handling-and-SSRF auditor combining all three.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of exploitability or of a fix working must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation targets DVWA, Juice Shop, WebGoat, PortSwigger Academy labs, HackTheBox/lab machines, or an application you wrote — never a third party without written authorization.

## Chapter III — Mandatory Part

### Exercise 00 — uploadbypass0

- **Turn-in dir:** file_handling_cloud_ssrf/ex00/
- **Files:** vuln_app.py, EXPLOIT.md, evidence/
- **Allowed:** a file-upload feature you build with progressively stronger (but still bypassable) restrictions
- **Forbidden:** any automated upload-bypass fuzzer

**Description.** A file-upload feature defended by three progressively stronger but still-bypassable restrictions — client-side-only validation, then extension blocklisting, then content-type checking — each defeated in turn, ending in an uploaded web shell that actually executes.

!!! success "Mandatory"

    - Layer 1 (client-side only): a upload form validating file extension only in JavaScript, bypassed by sending the upload request directly (Burp/curl), skipping the browser entirely.
    - Layer 2 (server-side extension blocklist): the server rejects `.php`/`.py` (matching your backend) by extension, bypassed via an alternate executable extension the blocklist misses (e.g. `.phtml`, case variation, double extensions like `shell.php.jpg` if your server's handler config is naive about it) or a null-byte-style trick if your stack is vulnerable to one.
    - Layer 3 (content-type / magic-byte check): the server checks the uploaded file's declared `Content-Type` and/or magic bytes, bypassed by crafting a file that is simultaneously a valid image (passing the magic-byte check) and valid executable code in your backend language (a genuine polyglot, or a magic-byte-prepended script your server's handler still executes based on extension).
    - Full impact: the uploaded file, once reachable at a predictable/discovered URL, executes as code on the server (a minimal web shell responding to a command parameter), demonstrated with a command run and its output returned — not just "the file uploaded successfully."
    - The correct fix applied and verified: store uploads outside the webroot (or in a location with execution disabled at the web-server config level), re-derive the filename/extension server-side from an allowlist of permitted types, and re-check actual file content (not just declared type) — your polyglot shown uploading successfully but never executing.

!!! failure "Forbidden"

    - Any automated upload-bypass tool.
    - Stopping at "the file uploaded" without demonstrating actual code execution.
    - A fix that's just "a better blocklist" — the mandatory fix is architectural (execution-disabled storage + allowlist).

!!! note "Norm"

    See §II.2, plus: each of the three bypass layers demonstrated as a distinct, reproducible step.

!!! tip "Bonus"

    A race-condition variant: upload a malicious file and access it in the brief window between upload completion and any asynchronous malware/content scan completing, if you add one to your target.

### Exercise 01 — lfi_logpoison0

- **Turn-in dir:** file_handling_cloud_ssrf/ex01/
- **Files:** vuln_app.py, EXPLOIT.md, evidence/
- **Allowed:** a PHP-style (or equivalent) include-based app you build, access to your own server logs
- **Forbidden:** any automated LFI exploitation tool

**Description.** A deliberately vulnerable "include this page fragment by name" feature, exploited for path traversal to read arbitrary local files, then escalated to remote code execution via log poisoning — planting attacker-controlled PHP code inside a log file the vulnerable include can be tricked into including.

!!! success "Mandatory"

    - A vulnerable endpoint that includes a file based on user input with insufficient path restriction (e.g. `include($_GET['page'] . '.php')` or a Python/Flask equivalent using unsanitized path joining).
    - Path traversal to read a real local file outside the intended directory (e.g. your app's own config file containing a real, planted secret) using `../` sequences, including demonstrating at least one traversal-filter bypass (e.g. double-encoding, or a naive single-pass `str.replace('../', '')` defeated by an overlapping payload like `....//`).
    - LFI-to-RCE via log poisoning: send a request (e.g. as a crafted `User-Agent` header) containing PHP/executable code that gets written verbatim into a log file your application or web server writes to, then use the LFI to include that log file, causing the planted code to execute — with the full chain demonstrated and a command's output returned.
    - A written explanation of exactly why file inclusion is more dangerous than file reading: an "include" doesn't just display a file's contents, it *executes* them if they contain valid code in the host language — the same execute-vs-parse distinction that ran through SSTI and deserialization, applied here to the filesystem layer.
    - The correct fix applied and verified: replace the free-form include with an allowlist of permitted page names mapped to fixed file paths (no user-controlled path construction at all), with your traversal and log-poisoning payloads shown failing.

!!! failure "Forbidden"

    - Any automated LFI tool.
    - Stopping at file disclosure without attempting the log-poisoning RCE escalation.
    - A fix that just adds more traversal-sequence filtering instead of eliminating user-controlled path construction entirely.

!!! note "Norm"

    See §II.2, plus: traversal, log-poisoning-injection, and log-poisoning-inclusion each demonstrated as separate, clearly evidenced steps.

!!! tip "Bonus"

    A PHP-wrapper-style data-URI or base64-filter RCE variant (or your language's equivalent trick) as an alternative LFI-to-RCE path not relying on log poisoning.

### Exercise 02 — imdsv2_bypass0

- **Turn-in dir:** file_handling_cloud_ssrf/ex02/
- **Files:** EXPLOIT.md, evidence/
- **Allowed:** a real or faithfully simulated IMDSv2 endpoint in your lab, an SSRF-vulnerable app you build
- **Forbidden:** any automated cloud-SSRF exploitation tool

**Description.** An SSRF against a target hardened with IMDSv2 (token-required metadata access, specifically designed to defeat simple SSRF) — demonstrating why IMDSv2 stops a naive SSRF but not one with the right request-shape control, and why network-layer restriction remains the real fix.

!!! success "Mandatory"

    - Set up (or faithfully simulate) an IMDSv2-style metadata endpoint requiring a `PUT` request to a token endpoint (with a custom header like `X-aws-ec2-metadata-token-ttl-seconds`) to obtain a session token, which must then be presented via a custom header (e.g. `X-aws-ec2-metadata-token`) on subsequent `GET` requests to actually read metadata/credentials — the real hardening IMDSv2 adds over IMDSv1.
    - Demonstrate that a "simple" SSRF — one that can only control the target *URL* of a GET request the server makes on the attacker's behalf — genuinely fails against IMDSv2, because it cannot also control the HTTP method or set the custom token headers required. This negative result must be demonstrated, not just asserted, since it's the whole reason IMDSv2 is considered a real mitigation.
    - Demonstrate a specific SSRF variant that *can* defeat IMDSv2: an application feature that gives the attacker more request control than a simple GET-a-URL proxy — for example, a webhook/HTTP-client feature that lets the attacker specify method and custom headers (not just a URL), or a two-step SSRF chain where the vulnerable feature can be made to issue the token-fetch PUT and a separate step relays it — with the full token-fetch-then-metadata-read chain completed and simulated credentials extracted.
    - A written comparison table: what IMDSv1 allowed a bare URL-only SSRF to do, what IMDSv2 additionally requires, and precisely what application-level condition has to be true for an SSRF to still defeat IMDSv2 despite the hardening.
    - The correct, complete fix applied and verified: network-level enforcement (e.g. blocking the metadata IP at the host firewall/network policy for anything but the specific processes that legitimately need it, or requiring IMDSv2 with a hop-limit of 1 to prevent proxying from a container) layered on top of IMDSv2 itself, explicitly framed as defense in depth — IMDSv2 alone is a mitigation for a specific SSRF shape, not a complete fix for SSRF as a vulnerability class.

!!! failure "Forbidden"

    - Any automated cloud-SSRF exploitation tool.
    - Claiming IMDSv2 is "defeated" without first honestly demonstrating the simple-SSRF case failing against it — the negative result is a mandatory part of the exercise, not optional context.
    - Testing against a real cloud provider's actual metadata endpoint outside an instance you provisioned yourself for this exercise.

!!! note "Norm"

    See §II.2, plus: the token-fetch and metadata-read steps of your exploit chain kept as separate, individually-evidenced functions.

!!! tip "Bonus"

    Demonstrate the hop-limit mitigation specifically: show a containerized app where a same-host SSRF can still reach the metadata endpoint but a request proxied through an additional hop (e.g. from inside a container to the host) is correctly blocked once the metadata service's IMDSv2 hop-limit is set to 1.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** upload-bypass technique layering (Exercise 00), traversal/inclusion detection with OOB-safe confirmation (Exercise 01), and request-shape-aware SSRF/metadata risk assessment (Exercise 02) — specifically the discipline, carried from Exercise 02, of never claiming an SSRF/metadata finding without demonstrating the actual request-shape control required, since a shallow tool that just tries a bare metadata-IP URL and calls it "vulnerable" or "not vulnerable" gets the IMDSv1-vs-v2 distinction wrong in both directions.

### Capstone — filessrf_auditor

- **Turn-in dir:** file_handling_cloud_ssrf/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A single auditor covering file-upload restriction strength, LFI/path-traversal probing, and SSRF-to-cloud-metadata risk assessment (including IMDSv1-vs-v2-aware testing) against a target application — the three exercises' techniques combined into one coherent pre-engagement recon tool.

!!! success "Mandatory"

    - Upload-restriction probe: given a target upload endpoint, attempts the layered bypass techniques from Exercise 00 (extension blocklist bypass, polyglot content) in increasing sophistication, stopping and reporting at the first layer that isn't defeated, and reporting full compromise (with OOB or direct-execution confirmation, not just "upload accepted") if all layers fall.
    - LFI/traversal probe: given a target parameter suspected of file-path use, attempts traversal sequences (including at least one filter-bypass encoding) and confirms via OOB or a planted-file-content match (not merely an altered response length) — explicitly does not attempt the log-poisoning RCE escalation automatically (too destructive/stateful for an automated default), but reports the finding and flags it as a manual-follow-up candidate for that escalation.
    - SSRF/metadata risk module: given a target parameter suspected of server-side URL fetching, first confirms basic SSRF via your OOB listener (reusing the Server-Side Injection capstone's pattern), then — only on confirmed SSRF — assesses what request-shape control the vulnerable feature actually grants (URL only, or method+headers too), and reports an accurate IMDSv1-only-vulnerable vs. IMDSv2-also-vulnerable vs. metadata-inaccessible classification based on that assessed control, never guessing.
    - A unified severity model across all three modules consistent with the roadmap so far: confirmed RCE/credential-theft &gt; confirmed access to sensitive local data or internal network resources &gt; confirmed-but-contained finding &gt; untested.
    - One consolidated report covering all three modules per target, with the evidence trail for every finding.
    - Demonstrated end to end against your Exercise 00/01/02 vulnerable and fixed targets, correctly classifying each, including correctly distinguishing the IMDSv1-only-vulnerable case from the IMDSv2-defeating case based on actually-assessed request-shape control rather than a guess.

!!! failure "Forbidden"

    - Any automated upload/LFI/SSRF tool doing the core work for you.
    - Automatically attempting the log-poisoning RCE escalation as part of the default LFI scan — flagged for manual follow-up instead, consistent with the "don't auto-exploit a fingerprinted finding" discipline from the Server-Side Injection capstone.
    - Guessing the IMDSv1-vs-v2 classification instead of deriving it from an actually-assessed request-shape capability.

!!! note "Norm"

    See §II.2, plus: upload-probe, LFI-probe, and SSRF/metadata-risk each in their own module sharing the OOB-listener layer.

!!! tip "Bonus (§II.7)"

    Extend the upload-restriction probe with a magic-byte polyglot generator that automatically produces a valid-image-plus-executable-code file for a small set of common web-server/language combinations.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
file_handling_cloud_ssrf/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live against your own targets. The capstone is run live against a target set the evaluator selects, and its IMDSv1-vs-v2 classification must be justified from evidence shown in the run, not from a hardcoded assumption about the target.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — uploadbypass0

**Defense questions**

1. Walk through all three bypass layers live, from client-side-only validation through to a working shell.
2. Show your polyglot file — explain exactly which bytes satisfy the magic-byte check and which make it executable code.
3. Why does storing uploads outside the webroot close this completely, architecturally, rather than just making it harder?
4. What's the difference between validating a file's declared content-type and actually verifying its content — why does only the second one matter?

### A.1 — lfi_logpoison0

**Defense questions**

1. Walk through your traversal-filter bypass live — what exactly did the naive filter miss?
2. Explain the log-poisoning chain end to end — why does the log file end up containing executable code at all, and why does the include statement treat it as code rather than as log text?
3. Why is "include" fundamentally more dangerous than "read" here — tie this back to the execute-vs-parse distinction from earlier subjects.
4. Why does an allowlist of fixed page-name-to-path mappings close this permanently, versus any amount of traversal-sequence filtering?

### A.2 — imdsv2_bypass0

**Defense questions**

1. Walk through the honest negative result first — show a simple URL-only SSRF failing against IMDSv2, live, and explain exactly why.
2. Then walk through your successful bypass — what specific extra request control did the vulnerable feature give you that the simple case didn't?
3. Why is network-layer restriction still necessary even with IMDSv2 enabled — what threat does IMDSv2 not address at all?
4. Explain the hop-limit concept and why it specifically matters for containerized workloads.

### A.3 — Capstone: filessrf_auditor

**Defense questions**

1. Run all three modules against your vulnerable targets live, narrating each finding's evidence.
2. Walk through the SSRF module's request-shape assessment specifically — show me how it decides IMDSv1-only vs. also-defeats-IMDSv2 for a given finding.
3. Why does the LFI module stop short of the log-poisoning escalation by default — same reasoning as an earlier capstone's stop-short decision; name it.
4. Run everything against your fixed targets and confirm zero false positives.
5. What would a naive version of this tool (bare metadata-IP URL fetch, binary vulnerable/not) get wrong compared to yours?

**Test / edge cases**

- [ ] An upload endpoint that defeats the first bypass layer but falls to the second: correctly reported at the specific layer reached, not a binary pass/fail.
- [ ] A traversal payload that succeeds in reading a file but the file has no distinguishing planted marker (can't confirm via content match): tool reports "likely traversal, unconfirmed content" rather than a false-confident claim.
- [ ] An SSRF-vulnerable feature that only supports GET with no header control, tested against an IMDSv2-protected endpoint: correctly classified as "SSRF confirmed, metadata inaccessible under IMDSv2" — not silently reported as a full metadata-compromise finding.
- [ ] A metadata endpoint entirely unreachable from the network segment the SSRF lands in (properly network-segmented target): correctly reported as such, distinct from "IMDSv2 blocked it."
- [ ] An upload endpoint accepting the polyglot file but storing it with execution genuinely disabled (correct fix already in place): reported as upload-accepted-but-non-executable, a clean/low-severity result, not conflated with full compromise.
