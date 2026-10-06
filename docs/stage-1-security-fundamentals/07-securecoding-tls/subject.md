---
title: "The Subject"
description: "The closing Stage 1 subject: the general principles underneath every specific vulnerability class covered so far — input validation, output encoding, leas…"
---
# Secure Coding Principles and TLS Configuration: The Subject

*Subject 7 of 7 — Security Fundamentals · Version 1.0 — September 2026*

> The closing Stage 1 subject: the general principles underneath every specific vulnerability class covered so far — input validation, output encoding, least privilege, defense in depth — plus TLS configuration audit at the level a real engagement report demands, and a capstone that proves the whole stage by taking DVWA end to end.

## Chapter 00 — Foreword

> *Every vulnerability in this stage was a specific instance of a general failure: trusting input, over-privileging a component, or having exactly one layer of defense between an attacker and the target. Name the general failure and you can find the next specific instance yourself, without a tutorial.*

This subject is deliberately the synthesis point for Stage 1. Input validation, output encoding, least privilege, and defense in depth are not a checklist to memorize — they are the four lenses that, applied together, would have prevented or contained every single vulnerability in the six subjects before this one. The exit gate for this subject is DVWA end to end, because by now there should be nothing on it you haven't already broken once.

## Chapter I — Introduction

You will build and defend a small app against a battery of your own Stage 1 attacks using only the four general principles (not vulnerability-specific patches), audit a real TLS configuration to the depth a professional pentest report requires, and then take DVWA from a fresh instance to fully exploited across every category the roadmap has covered — SQLi, XSS, CSRF, command injection, broken auth, broken access control — in one sitting, with a written report for each.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of the form "this is exploitable" or "this fix works" must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation in this subject targets DVWA, Juice Shop, WebGoat, or an application you wrote — running locally or on a VPS you own. Never a third party without written authorization.

**II.6** **Certification note.** This is the Stage 1 exit gate. eJPT (~$249, confirm current price) is appropriate once every exercise and the capstone are cleared without notes — not before.

## Chapter III — Mandatory Part

### Exercise 00 — principledapp0

- **Turn-in dir:** securecoding_tls/ex00/
- **Files:** app.py, THREATNOTES.md
- **Allowed:** Flask/minimal WSGI, an output-encoding library (e.g. Jinja2 autoescaping) used correctly
- **Forbidden:** any vulnerability-specific patch library (a WAF, an XSS-filter package) as a substitute for architectural principles

**Description.** A small multi-feature app (login, a comment feature, a file-reference feature, an admin action) built from the start using input validation, output encoding, least privilege, and defense in depth as explicit, named design decisions — then attacked with your own Stage 1 exploit techniques and shown to hold.

!!! success "Mandatory"

    - Input validation: every user-supplied value is validated against an explicit allow-pattern (type, length, charset) at the boundary, before it reaches any business logic — not scattered ad hoc checks.
    - Output encoding: every point where user data is rendered back (HTML, into a shell command if any, into a SQL query) uses context-appropriate encoding or parameterization — reusing your parameterized-query pattern from SQL and Database Internals and your Jinja2 autoescaping (never manual string-building) for HTML.
    - Least privilege: the app's own database user has only the permissions its queries actually need (no DROP/ALTER on a login-only feature), and any shelled-out command (if present) runs as a dedicated low-privilege OS account, not the app's main process user — both demonstrated, not just configured.
    - Defense in depth: at least one feature is protected by two independent layers that would each, alone, have stopped a specific attack (e.g. parameterized queries *and* a least-privilege DB user together — demonstrate that even if the parameterization were somehow bypassed, the DB user's restricted grants would still block the worst-case outcome).
    - A THREATNOTES.md mapping each of your own Stage 1 exploit techniques (SQLi, XSS, CSRF, command injection, session fixation, IDOR) against this specific app, and for each, which of the four principles is the reason it fails here — with the failed exploit attempt captured as evidence for at least four of the six.

!!! failure "Forbidden"

    - A WAF, filter library, or other bolt-on defense presented as satisfying "defense in depth" instead of genuine independent architectural layers.
    - An input-validation scheme that is really just an XSS/SQLi blocklist wearing a different name.
    - Claiming a technique "fails" against this app without actually attempting it and capturing the failure.

!!! note "Norm"

    See §II.2, plus: validation, encoding, and privilege configuration each clearly separated and independently inspectable/auditable.

!!! tip "Bonus"

    Add a rate-limiting layer as a fifth, orthogonal defense against the login endpoint specifically, and demonstrate it independently blocking a credential-stuffing simulation even if the password policy were otherwise weak.

### Exercise 01 — tlsaudit0

- **Turn-in dir:** securecoding_tls/ex01/
- **Files:** AUDIT_REPORT.md, evidence/
- **Allowed:** your Networking Depth tlsinspect tool, openssl s_client, testssl.sh for cross-checking only
- **Forbidden:** testssl.sh/sslyze as your primary evidence source — your own tooling must produce the core findings

**Description.** A professional-grade TLS configuration audit of a real host (your own VPS) using your own tooling from Networking Depth and Cryptography Fundamentals, written up exactly as a pentest report would present it — finding, evidence, risk, remediation.

!!! success "Mandatory"

    - Full protocol/cipher enumeration: which TLS versions the server accepts (flagging any below 1.2), and the actual cipher suites negotiated for each, using your own `tlsinspect`/`chaininspect` tooling, with `openssl s_client -connect host:443 -tls1` (and similar per-version flags) used to individually confirm which legacy versions are actually rejected versus accepted.
    - Certificate chain audit reusing Cryptography Fundamentals' `chaininspect`: full chain validity, signature algorithm strength (flagging SHA-1 anywhere in the chain), key size, and expiry — with expiry specifically checked against a "renews with enough lead time" policy you define and justify.
    - HSTS and mixed-content posture: `Strict-Transport-Security` header presence/value (reusing HTTP Internals' header work), and whether any HTTP→HTTPS redirect chain has an insecure hop, with the exact request/response evidence.
    - A finding severity model applied consistently: at minimum, distinguish "actively exploitable now" (e.g. TLS 1.0 still accepted) from "best-practice gap, not currently exploitable" (e.g. HSTS present but missing `preload`), and justify the distinction in writing for each finding.
    - A written remediation section per finding specific enough that an engineer could act on it directly (exact config directive/change), not a generic "upgrade your TLS configuration."

!!! failure "Forbidden"

    - testssl.sh/sslyze output presented as your own analysis — cross-checking your findings against them afterward is expected and good practice, but the core evidence must come from your own tooling.
    - A report with findings but no evidence (request/response, openssl output, or your tool's captured output) attached per finding.
    - Auditing any host you do not own.

!!! note "Norm"

    See §II.2, plus: AUDIT_REPORT.md follows a consistent professional structure — executive summary, findings table, detailed findings with evidence and remediation, appendix with raw tool output.

!!! tip "Bonus"

    Compare the same host's configuration against the current Mozilla TLS configuration guidelines (Modern/Intermediate/Old) and classify which tier it actually meets.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** literally everything from Stage 0 and Stage 1 at once, against one real (if intentionally vulnerable) application, under DVWA's "high" difficulty setting specifically because it adds partial mitigations to each category — DVWA at "low" difficulty tests whether you memorized a payload; DVWA at "high" tests whether you understand the underlying mechanism well enough to adapt when the obvious payload is blocked, which is the entire point of everything this stage has built toward.

### Capstone — dvwa_fullsweep

- **Turn-in dir:** securecoding_tls/capstone/
- **Files:** REPORT.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A complete, professional-report-style engagement against a fresh DVWA instance: every category the roadmap has built toward so far — SQL injection, XSS (stored/reflected), CSRF, command injection, broken authentication, and IDOR/broken access control — exploited manually at DVWA's "high" security level, written up as one coherent report.

!!! success "Mandatory"

    - SQL injection exploited manually (no SQLMap) against DVWA "high," including bypassing its input-length/character restrictions at that level, extracting the full `users` table.
    - Stored and reflected XSS exploited against DVWA "high," including bypassing its regex-based filtering, each ending in a real payload (not just an alert) — session-token exfiltration to a listener you control, reusing your Client-Side Injection capstone tooling if helpful.
    - CSRF exploited against DVWA "high" (the password-change function), including working around its anti-CSRF-token implementation's specific weakness at that level (DVWA "high" uses a token that has a real, documented flaw worth rediscovering rather than being told).
    - Command injection exploited against DVWA "high," bypassing its input filtering using a technique from your Server-Side Injection work.
    - Broken authentication/brute-force and broken access control (IDOR) both demonstrated against the relevant DVWA modules, each with the specific missing/broken check identified precisely, as in Access Control and IDOR.
    - One consolidated REPORT.md: executive summary, a findings table (category, severity, DVWA module), and one detailed finding per category with request/response evidence and remediation — written as if for a client who has never seen DVWA and needs to understand real risk, not "I completed the DVWA challenge."

!!! failure "Forbidden"

    - SQLMap, XSStrike, commix, or any automated exploitation tool anywhere in this capstone — every finding must be manually driven, even if you reuse your own capstone tooling from earlier subjects as an assist.
    - Testing at DVWA "low" or "medium" and reporting it as equivalent — "high" is the mandatory bar specifically because its partial mitigations are what separate memorized payloads from real understanding.
    - A report that reads as a walkthrough ("click here, then here") instead of a findings-and-risk report a client could act on.

!!! note "Norm"

    See §II.2, plus: REPORT.md follows the same professional structure as Exercise 01's TLS audit, extended to cover six finding categories instead of one.

!!! tip "Bonus (§II.7)"

    Repeat the full sweep against Juice Shop or WebGoat as a second target, and note in writing at least three ways its vulnerable-by-design patterns differ from DVWA's (different framework, different specific mistakes) despite the underlying vulnerability classes being identical.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
securecoding_tls/
├── ex00/
├── ex01/
└── capstone/
```

Each exercise is defended live. The capstone is defended against a freshly reset DVWA instance at "high" security level, with the evaluator free to reset individual modules mid-defense and request re-exploitation — this is the Stage 1 exit gate and is graded to that standard: every category, unaided, without notes.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — principledapp0

**Defense questions**

1. Attack this app live with three of your own Stage 1 techniques — narrate which specific design decision stops each one.
2. Show me your defense-in-depth example — walk through what would actually happen if the first layer were somehow bypassed.
3. Why is your least-privilege DB user a real independent control and not just "the same parameterization wearing a different hat"?
4. Pick one principle and explain a vulnerability class from an earlier Stage 1 subject that it alone would not have stopped, and what the missing second principle would have to be.

### A.1 — tlsaudit0

**Defense questions**

1. Walk me through one finding exactly as you'd present it in a client-facing report — finding, evidence, risk, fix.
2. Why does distinguishing "actively exploitable" from "best-practice gap" matter for how a client prioritizes remediation work?
3. Show your own tool's output for the certificate chain finding and explain what it caught that a plain browser padlock icon would not show a user.
4. If this host showed TLS 1.0 still accepted alongside TLS 1.3, what would you actually recommend — disable 1.0 immediately, or is there ever a legitimate reason to keep it, and how would you find out?

### A.2 — Capstone: dvwa_fullsweep

**Defense questions**

1. Pick one finding at random from your report and re-exploit it live, from a fresh DVWA reset, at "high" difficulty.
2. For the CSRF finding specifically, explain the exact weakness in DVWA "high"'s anti-CSRF token implementation that you exploited.
3. Walk through your report's executive summary as if I were a non-technical client — does it communicate real business risk, or just a list of bug names?
4. Which of your six findings would you rate highest severity for a real production application, and why — defend the ranking.
5. What's the single biggest difference between exploiting DVWA at "low" versus "high" difficulty, in terms of what it actually tests about your understanding?

**Test / edge cases**

- [ ] A DVWA reset between attempts (session/state cleared): every exploit reproducible from a clean instance, not dependent on leftover state from a previous run.
- [ ] The evaluator changes DVWA's security level live between two categories during the defense: you correctly identify the new level's specific mitigation before attempting exploitation, rather than reflexively reusing a "high"-level payload that may not even be necessary at "medium."
- [ ] A finding where the "high"-level mitigation genuinely defeats your first three payload attempts: your report/defense shows the iterative adaptation process, not just the final working payload with no trace of the reasoning that got you there.
- [ ] The evaluator asks you to explain why a given DVWA "impossible" level (if enabled) fully closes a category: you can articulate the fix at the same depth as Exercise 00's principled app, connecting DVWA's actual source-level fix back to input validation/output encoding/least privilege/defense in depth.
