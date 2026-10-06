---
title: "The Subject"
description: "Build the protocol by hand, then attack the security semantics layered on top of it — headers, cookies, CORS, CSP, and the auth flows that live or die by …"
---
# HTTP Internals: The Subject

*Subject 3 of 6 — Foundations Reset · Version 1.0 — September 2026*

> Build the protocol by hand, then attack the security semantics layered on top of it — headers, cookies, CORS, CSP, and the auth flows that live or die by them — until every response your browser trusts is a response you can explain byte by byte.

## Chapter 00 — Foreword

> *A browser trusts a server the way a stranger trusts a business card — entirely, and for reasons that have nothing to do with the paper stock.*

HTTP itself has almost no security model. Everything that keeps the modern web from being a free-for-all — same-origin policy, cookie flags, CORS, CSP — is a set of conventions bolted on afterward, enforced by the client, and routinely misconfigured by the server. You cannot audit what you have only ever consumed through a library.

## Chapter I — Introduction

This subject moves from "I sent a request with `requests`" to "I wrote the client and the server, and separately, the tool that finds the fourteen ways people misconfigure the security semantics on top of both." You will parse and construct raw HTTP/1.1 over a socket, build a header-security auditor, break a deliberately misconfigured session/cookie implementation, and end by building a single tool that audits headers, cookies, CORS, and redirect/host-header handling against a live target.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input, an unreachable host, or unexpected data. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline), applies to every exercise.** Functions do one thing and are named for what they do. No magic numbers — ports, offsets, thresholds, and protocol constants are named constants, never bare literals. No block of code you cannot explain, unprompted, line by line, during defense. Every non-obvious line carries a comment explaining why, not what.

**II.3** **Evidence, not assertions.** Every claim of the form "this detects X" or "this parses Y correctly" must be backed by a reproducible capture, transcript, or log — captured in your turn-in. Assertions without evidence are treated as unmet requirements during defense.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct. A single mandatory-part flaw — even a minor one — zeroes the bonus evaluation for that exercise, no exceptions.

**II.5** **Scope.** Exercises 00–02 target hosts and apps you build or own. The capstone may audit any host you own, plus DVWA/Juice Shop/WebGoat instances you run locally — never a third party without written authorization.

**II.6** **Global forbidden list.** Unless an exercise explicitly says otherwise: no Nikto, no automated header-scanning SaaS, no `securityheaders.com` API as a substitute for your own logic. Reading their output for comparison after your own tool runs is fine.

## Chapter III — Mandatory Part

### Exercise 00 — httpanatomy0

- **Turn-in dir:** http_internals/ex00/
- **Files:** httpserver.py, httpclient.py, README.md
- **Allowed:** socket, standard library only
- **Forbidden:** requests, http.client, any HTTP library

**Description.** A minimal HTTP/1.1 client and server pair built directly on TCP sockets, handling request/response anatomy, methods, status lines, headers, and both content-length and chunked transfer encoding by hand.

!!! success "Mandatory"

    - Server: accepts a connection, parses the request line (method, target, version), parses headers into a case-insensitive map, and correctly reads a body using either `Content-Length` or `Transfer-Encoding: chunked` — implementing chunk-size-line parsing yourself.
    - Client: constructs a well-formed request by hand (request line, headers, blank line, body) for GET, POST, HEAD, OPTIONS, and TRACE, and parses the response status line, headers, and body symmetrically.
    - Server responds correctly to HEAD (headers only, no body) and OPTIONS (an `Allow` header listing supported methods) — and your README explains, from an attacker's perspective, what an unexpectedly-enabled TRACE or unrestricted OPTIONS response can leak.
    - Server returns at least 200, 301, 302, 400, 403, 404, and 500 in the right situations, and the client correctly follows a 301/302 redirect chain up to a configurable hop limit (never infinitely).
    - Keep-alive: the server correctly reuses one TCP connection for multiple sequential requests when `Connection: keep-alive` is negotiated, and closes cleanly on `Connection: close`.

!!! failure "Forbidden"

    - Any HTTP parsing/construction library, including `http.client`, `http.server`, or `requests`.
    - Treating the body as "everything until the socket closes" instead of respecting `Content-Length`/chunked framing — this is exactly the class of bug behind real request-smuggling vulnerabilities.
    - A 500 response leaking a Python traceback to the client.

!!! note "Norm"

    See §II.2, plus: request-line parsing, header parsing, body framing, and response construction each in their own function; status codes referenced by named constants, never bare integers.

!!! tip "Bonus"

    HTTP/1.0 vs 1.1 negotiation handling; a pipelining demonstration showing why HTTP/1.1 pipelining is fragile enough that browsers abandoned it.

### Exercise 01 — headersec0

- **Turn-in dir:** http_internals/ex01/
- **Files:** headersec0.py, README.md
- **Allowed:** requests or raw sockets, ssl standard module
- **Forbidden:** securityheaders.com API, Nikto, any prebuilt header-audit library

**Description.** A CLI that fetches a URL, follows redirects, and produces a structured, color-coded report of every security-relevant header and cookie flag present, missing, or misconfigured, plus the TLS version/cipher in use.

!!! success "Mandatory"

    - Reports presence/absence and value of: `Strict-Transport-Security` (and whether `includeSubDomains`/`preload` are set), `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`.
    - For every `Set-Cookie` header, parses and reports `HttpOnly`, `Secure`, `SameSite` (and flags the absence of `SameSite` as defaulting to `Lax` in modern browsers, explaining what that does and does not prevent), `Domain`, and `Path`.
    - Reports the full redirect chain followed to reach the final response, flagging any hop that downgrades HTTPS→HTTP.
    - Reports negotiated TLS version and cipher suite for the final host.
    - Severity-ranks findings (e.g. missing HSTS on an HTTPS site is higher severity than a missing `Permissions-Policy`) with your ranking justified in writing, not just asserted.

!!! failure "Forbidden"

    - Calling an external header-scanning API and relabeling its output as your own analysis.
    - Flagging a header as "missing" without checking case-insensitively — HTTP headers are case-insensitive and a naive exact-match check produces false positives.
    - Ignoring multiple `Set-Cookie` headers on one response (a common parsing bug when using low-level socket reads).

!!! note "Norm"

    See §II.2, plus: fetch/parse/classify/report as separate functions; a single table of header-name → check-function rather than one long if/elif chain.

!!! tip "Bonus"

    CSP directive-level analysis (flagging `unsafe-inline`/`unsafe-eval`/wildcard sources specifically, not just "CSP present"); batch mode over a list of hosts producing a comparison table.

### Exercise 02 — cookielab

- **Turn-in dir:** http_internals/ex02/
- **Files:** app.py, ANALYSIS.md, evidence/
- **Allowed:** Flask, Burp Suite Community, your own instrumentation
- **Forbidden:** any session-management library beyond Flask's own default session handling for the "before" state

**Description.** A minimal Flask app with intentionally broken session/cookie security, exploited by hand via Burp/devtools, then fixed field by field with a before/after comparison.

!!! success "Mandatory"

    - The "before" app ships with at least three real misconfigurations: a session cookie missing `HttpOnly`, a session ID that does not rotate on login (session fixation), and a cookie scoped with a `Domain` broader than necessary.
    - A working session-fixation exploit demonstrated end to end: attacker sets a known session ID in the victim's browser before login, victim logs in, attacker reuses the same ID to inherit the authenticated session — captured with Burp/devtools evidence at every step.
    - A working demonstration that the missing `HttpOnly` flag lets a simulated injected script (in your own test page, not a real XSS) read `document.cookie` and exfiltrate the session value.
    - Each vulnerability fixed one at a time in an "after" version, with the exact diff shown and a before/after Burp capture proving the fix closes the exploit.
    - A written explanation of what `SameSite=Strict` versus `Lax` would each have additionally prevented in this specific app's login flow.

!!! failure "Forbidden"

    - Fixing all three issues simultaneously with no isolated before/after evidence per issue.
    - Claiming the session-fixation fix works because "the docs say session.regenerate() is called" without capturing the actual session ID changing across the login boundary.
    - Testing this against anything other than your own local instance.

!!! note "Norm"

    See §II.2, plus: the "before" and "after" apps are separate files/branches, not one app with a feature flag; ANALYSIS.md follows vulnerability → exploit → root cause → fix → verification per issue.

!!! tip "Bonus"

    Add and then defeat a CSRF vulnerability in the same app using a crafted auto-submitting HTML form, then fix it with a synchronizer token.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** full request/response anatomy (to correctly parse edge-case responses), every cookie security attribute, CORS preflight mechanics, CSP directive semantics, auth-flow awareness (where tokens live and how they can be stolen), and the open-redirect/Host-header-injection surface that request smuggling and cache poisoning research builds on. No exercise above combines more than two of these; a CORS finding is meaningless without understanding cookies (is the response credentialed?), and a CSP finding is meaningless without understanding what inline-script blocking actually defeats. The tool does not produce a coherent report on partial knowledge — it produces a pile of unrelated true/false flags.

### Capstone — httpsentinel

- **Turn-in dir:** http_internals/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A single audit tool that combines header/cookie security analysis with CORS misconfiguration testing, CSP bypass reasoning, open-redirect detection, and Host-header-injection probing against a target you own or run locally — producing one structured report an engineering team could act on.

!!! success "Mandatory"

    - Everything from `headersec0` (Exercise 01), refactored into this tool as its baseline module.
    - CORS module: sends preflight and simple requests with varying `Origin` headers (including `null`, a reflected arbitrary origin, and a subdomain), and reports whether `Access-Control-Allow-Origin` is reflected/wildcarded, and critically, whether `Access-Control-Allow-Credentials: true` is combined with an overly permissive origin — the specific combination that turns a CORS misconfiguration into an authenticated data leak.
    - CSP module: parses the policy (if any) into directives and flags `unsafe-inline`, `unsafe-eval`, wildcard (`*`) sources, and the complete absence of `script-src`/`default-src`, with a plain-language note on what each specific gap actually enables.
    - Open-redirect module: given a list of parameter names commonly used for redirects (e.g. `next`, `redirect`, `url`, `return`), tests each against the target and reports any that redirect to an attacker-controlled external domain unchecked.
    - Host-header-injection module: sends requests with a manipulated `Host` header (and, separately, `X-Forwarded-Host`) and detects whether the response (e.g. a password-reset link, a canonical-URL tag, a redirect) reflects the attacker-controlled value — with a written explanation of the password-reset-poisoning attack this enables.
    - One consolidated report per target: every finding tagged by category (headers/cookies/CORS/CSP/redirect/host-injection), severity, and the exact request/response evidence that produced it.
    - Demonstrated end to end against DVWA or Juice Shop running locally, with at least one real finding per module — or, for a module with no finding, an explicit "checked, not present" line, never silence.

!!! failure "Forbidden"

    - Any existing header/CORS/CSP scanner wrapped and relabeled.
    - Flagging every CORS response with any `Access-Control-Allow-Origin` as a vulnerability without checking the credentials combination — that is the actual bug, not the header's mere presence.
    - Testing the open-redirect or Host-header modules against anything but your own local instances.
    - A module that silently no-ops on an unexpected response shape instead of reporting "inconclusive."

!!! note "Norm"

    See §II.2, plus: one module per finding category, a shared HTTP-fetch layer reused by all modules (not five copies of request logic), and a single reporting function that all modules feed into.

!!! tip "Bonus (§II.7)"

    A CSP bypass-payload suggester for a given weak policy (e.g. a JSONP endpoint on an allowed script-src host); a diff mode comparing two scans of the same target over time.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
http_internals/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live against a target the evaluator selects (your own local instance or DVWA/Juice Shop they stand up). For the capstone, the evaluator may add a header/cookie/CORS/CSP misconfiguration to their own test instance not covered by your demonstrated findings and expects your tool to either catch it or produce an honest "not covered by this module" rather than silence.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — httpanatomy0

**Defense questions**

1. Show me, live, a request whose body length is declared by `Content-Length` and one declared by chunked encoding — walk through exactly how your parser knows where each body ends.
2. What happens if a request declares both `Content-Length` and `Transfer-Encoding: chunked` with conflicting values? What does your server do, and why does this exact ambiguity matter for request smuggling?
3. Why is an open TRACE method historically dangerous (Cross-Site Tracing), even though modern browsers block it from JavaScript?
4. Show your redirect-chain following — what stops it from looping forever on a server that redirects A→B→A?
5. What is the actual difference, on the wire, between a HEAD and a GET response?

### A.1 — headersec0

**Defense questions**

1. Point this at a site missing `SameSite` entirely — what does your tool report, and what does the browser actually do by default in 2026?
2. Walk me through your CSP directive parser on a real policy string — where do you split on semicolons vs spaces, and what happens on a malformed directive?
3. Why does a missing `X-Content-Type-Options: nosniff` matter specifically for a file-upload feature?
4. Show a host where your tool follows an HTTPS→HTTP downgrade redirect — what would an on-path attacker do with that hop?
5. Justify your severity ranking for at least two findings, live, without your notes.

### A.2 — cookielab

**Defense questions**

1. Show me the exact session ID before and after login in your fixation exploit — where in Flask's session handling does the rotation (or lack of it) actually happen?
2. Your XSS-flag demo reads `document.cookie` — what specifically about `HttpOnly` stops this in a real attack, and what does it not stop?
3. What is the practical difference between narrowing the cookie's `Domain` and narrowing its `Path` — give a concrete scenario where each one matters.
4. If this app also had a subdomain takeover somewhere under its cookie's `Domain` scope, what would that let an attacker do to your fixed cookie?
5. Show your before/after Burp captures side by side for one vulnerability, live.

### A.3 — Capstone: httpsentinel

**Defense questions**

1. Show me the specific CORS response where credentials-plus-reflected-origin fires — what could an attacker actually steal with that combination, concretely, for this target?
2. Walk through your CSP parser on a policy using both `default-src` and a more specific `script-src` — which one governs script execution, and does your tool get that precedence right?
3. Your open-redirect module found (or didn't find) a vulnerable parameter — show me the exact request/response, and explain why a redirect to an attacker domain is a real security issue and not just a UX quirk.
4. Demonstrate the Host-header-injection finding live — trace exactly where the reflected value would end up in a real password-reset email.
5. Why does this tool need to understand cookies at all to correctly evaluate a CORS finding?
6. What would this tool report on a target that's completely well-configured — show me that a clean bill of health is actually a positive assertion per check, not just an empty output.

**Test / edge cases**

- [ ] Target with no CSP at all: flagged as a finding, not silently skipped.
- [ ] Target with a CSP that has `default-src 'none'` and nothing else: correctly interpreted as restrictive, not flagged as broken.
- [ ] CORS preflight (OPTIONS) response that differs from the actual request response: both captured and reconciled.
- [ ] `Access-Control-Allow-Origin: *` with no credentials header: correctly classified as lower severity than reflected-origin-plus-credentials.
- [ ] A redirect parameter that only accepts relative paths: correctly classified as not vulnerable.
- [ ] A redirect parameter vulnerable only to protocol-relative URLs (`//evil.com`): still detected.
- [ ] Host header reflected into a `Location` header but the app also validates against an allow-list: correctly classified as not vulnerable, with evidence.
- [ ] Multiple `Set-Cookie` headers on one response: all parsed, none dropped.
- [ ] A target that times out or refuses connection mid-scan: reported as inconclusive for that module, tool does not crash.
- [ ] Self-referential CORS check (target reflects the tool's own request Origin back exactly): correctly distinguished from a genuinely permissive wildcard policy.
