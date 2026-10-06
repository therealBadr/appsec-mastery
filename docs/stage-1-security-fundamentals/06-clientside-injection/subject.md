---
title: "The Subject"
description: "The two vulnerability classes that exploit the trust a server places in a browser and the trust a browser places in a server — stored, reflected, and DOM-…"
---
# Client-Side Injection: XSS and CSRF: The Subject

*Subject 6 of 7 — Security Fundamentals · Version 1.0 — September 2026*

> The two vulnerability classes that exploit the trust a server places in a browser and the trust a browser places in a server — stored, reflected, and DOM-based XSS through to a full cookie-theft payload, and CSRF from a crafted page to a defeated synchronizer token.

## Chapter 00 — Foreword

> *XSS is not "the site is ugly with a popup." It is arbitrary JavaScript running with the full authority of the logged-in victim, inside the one place your session cookie was supposed to be safe.*

These two classes get treated as beginner material because `alert(1)` is the canonical proof-of-concept — and that framing does real damage, because it trains people to stop at proof of existence instead of proof of impact. This subject insists on the second half every time: not "I can inject a script tag" but "I can steal a session and CSRF is what an attacker does the moment they can't."

## Chapter I — Introduction

You will exploit stored, reflected, and DOM-based XSS against separate deliberately vulnerable pages, each ending in an actual session-cookie exfiltration to a listener you control (not an alert box), demonstrate CSRF against a state-changing action with a crafted auto-submitting page, and fix both correctly — output encoding and CSP for XSS, synchronizer tokens and SameSite for CSRF. The capstone is a payload-generation and confirmation tool that adapts to a target's specific context and CSP.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of the form "this is exploitable" or "this fix works" must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation in this subject targets DVWA, Juice Shop, WebGoat, or an application you wrote — running locally or on a VPS you own. Never a third party without written authorization.

## Chapter III — Mandatory Part

### Exercise 00 — xsstriad0

- **Turn-in dir:** clientside_injection/ex00/
- **Files:** vuln_app.py, EXPLOIT.md, evidence/
- **Allowed:** a small Flask/Node app you build, your own listener for exfiltration
- **Forbidden:** XSStrike or any automated XSS scanner

**Description.** Three separate deliberately vulnerable pages — one stored, one reflected, one DOM-based — each exploited to full impact: a working payload that exfiltrates the victim's session cookie to a listener you control, not merely a JavaScript alert.

!!! success "Mandatory"

    - Stored XSS: a comment/profile-bio feature that persists unsanitized HTML, exploited with a payload that runs on every subsequent visitor's page load and sends `document.cookie` to a listener endpoint you control, captured with the exfiltrated (test) cookie value arriving at your listener.
    - Reflected XSS: a search or error-message feature that reflects unsanitized input directly into the response, exploited via a crafted URL that a victim would have to click — with the full attack narrated including how such a link would realistically be delivered (a phishing email, a shortened URL).
    - DOM-based XSS: a page where the vulnerability is entirely client-side — JavaScript reads a value from `location.hash` or similar and writes it into the DOM via `innerHTML` with no server round-trip involved — exploited with a payload that never appears in any server log, and your writeup explains precisely why that makes DOM-based XSS invisible to server-side-only defenses (WAFs included).
    - For each of the three, demonstrate the payload surviving at least one naive filter (e.g. a blocklist stripping the literal string `<script>`) via an alternative injection vector (an event handler attribute like `onerror`, or a different tag), proving blocklist-based XSS filtering fails the same way blocklist-based injection filtering failed in Server-Side Injection.
    - A written classification table: for each of your three findings, source (where attacker input enters), sink (where it's unsafely written to the page), and whether the taint flow crosses the server at all — the actual mental model for finding new XSS, not payload memorization.

!!! failure "Forbidden"

    - XSStrike or any automated XSS scanner/fuzzer.
    - Stopping at an `alert(1)` proof-of-concept for any of the three — full impact (cookie exfiltration to your own listener) is mandatory for each.
    - Testing any payload against a target other than your own app.

!!! note "Norm"

    See §II.2, plus: the three vulnerable pages are separate, isolated routes, not variations of one shared vulnerable function.

!!! tip "Bonus"

    A CSP-bypass variant: add a real but weak CSP (e.g. allowing a JSONP endpoint or a wildcard script-src host) to one of the three pages and demonstrate exfiltration still succeeding through the CSP gap.

### Exercise 01 — csrfstrike0

- **Turn-in dir:** clientside_injection/ex01/
- **Files:** attack_page.html, EXPLOIT.md, evidence/
- **Allowed:** a state-changing endpoint you build with no CSRF protection, a crafted attacker HTML page
- **Forbidden:** any automated CSRF PoC generator (Burp's CSRF PoC generator may be used only to cross-check your own hand-written page afterward)

**Description.** A working CSRF exploit against a real state-changing action (e.g. "change account email" or "transfer funds") via a self-submitting malicious HTML page a victim only has to load, and a demonstration of exactly what SameSite cookie attributes do and don't prevent against it.

!!! success "Mandatory"

    - A target endpoint that changes account state (e.g. email address) based solely on a valid session cookie, with no CSRF token and no other request-origin verification.
    - A standalone `attack_page.html` — the kind that would be hosted on an attacker's own site — containing a form that auto-submits via JavaScript on page load, targeting the vulnerable endpoint, demonstrated working when a victim (your own second browser session/profile, authenticated to the target) simply opens the page.
    - A GET-based CSRF variant, if the vulnerable action can be triggered via GET (e.g. via an `<img src=>` tag) — demonstrating that CSRF isn't only a form-submission problem, and explaining why allowing state changes via GET is a separate, compounding mistake.
    - A demonstration of the exploit failing once the cookie is set with `SameSite=Lax`, succeeding again for the GET/image-tag variant specifically if the browser's Lax handling of top-level navigation allows it (document precisely which sub-case Lax does and does not stop), and failing entirely once set to `SameSite=Strict` — three real before/after captures, not an assertion.
    - The complete, correct fix implemented: a synchronizer token (a random, per-session or per-request token embedded in the legitimate form and validated server-side on submission) added to the vulnerable endpoint, with your original exploit re-run and shown failing even without relying on `SameSite` at all.

!!! failure "Forbidden"

    - Relying on `SameSite` alone as "the fix" in your writeup — modern browser defaults have reduced CSRF's reach, but a synchronizer token is the actual robust, defense-in-depth fix and must be implemented.
    - A CSRF PoC generated entirely by an external tool with no hand-built page of your own.
    - Testing this against anything other than your own local target.

!!! note "Norm"

    See §II.2, plus: token generation and token validation each in their own function; attack_page.html kept as a standalone artifact demonstrating it needs nothing from the target site itself.

!!! tip "Bonus"

    Demonstrate a CSRF exploit against a JSON API endpoint that naively accepts `Content-Type: text/plain` as a way around a simple-requests-only CORS assumption, showing CSRF isn't strictly a form-encoded-only problem.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** the source/sink/context reasoning from Exercise 00 (a payload that works inside an HTML attribute is shaped completely differently from one that works inside a `<script>` block or a URL context — a one-size-fits-all payload fails constantly in real applications), CSP-directive awareness from Applied HTTP/CSP work earlier in the roadmap, and the CSRF token/SameSite reasoning from Exercise 01. A tool that fires the same `<script>alert(1)</script>` payload everywhere — the beginner's mental model this subject explicitly rejected — misses the majority of real XSS, which lives in attribute contexts, JS-string contexts, and CSP-restricted pages where only a context-specific payload has any chance.

### Capstone — xsscsrf_confirm

- **Turn-in dir:** clientside_injection/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A context-aware payload tool: given a target injection point, it detects the surrounding HTML/JS/attribute context and the active CSP (if any), generates an appropriately-shaped XSS payload for that specific context, and — for any state-changing endpoint it also finds — automatically generates and tests a CSRF proof-of-concept, confirming both via real out-of-band callbacks exactly as the capstone before this one did for server-side injection.

!!! success "Mandatory"

    - Context detection: given a marker string reflected into a response, determines whether it landed in an HTML text node, an HTML attribute value, a `<script>` block, or a URL/href context, by inspecting exactly where the marker appears relative to surrounding tag/quote structure.
    - CSP detection: parses any `Content-Security-Policy` header present (reusing your HTTP Internals header-parsing logic) and determines whether inline scripts, specific external hosts, or JSONP-style callback endpoints on allowed hosts could serve as a bypass.
    - Context-appropriate payload generation: produces a different payload shape for each detected context (e.g. breaking out of an attribute with a quote-and-event-handler payload vs. breaking out of a script string vs. a plain tag injection), and, when a CSP would block a naive inline payload, attempts a CSP-aware alternative (an allowed host, or reports "no bypass found" honestly).
    - OOB confirmation: every candidate payload, when it fires, calls back to a listener you control (reusing the OOB-listener pattern from the previous capstone) with a unique token, so success is confirmed by actual execution, not by guessing from the reflected response alone.
    - CSRF auto-detection and PoC generation: for any discovered state-changing endpoint reachable with only cookie-based auth and no token/origin check, automatically generates a working `attack_page.html`-style PoC (per Exercise 01) and reports it as a paired finding alongside any XSS on the same application, since the two are commonly exploited together (XSS to steal a token, or CSRF to abuse the lack of one).
    - Demonstrated end to end against your own Exercise 00 (three XSS contexts) and Exercise 01 (CSRF) targets, correctly generating a firing, OOB-confirmed payload for each XSS context and a working CSRF PoC, plus a clean/fixed target set with zero false positives.

!!! failure "Forbidden"

    - XSStrike or any existing context-aware XSS tool doing the detection/generation for you.
    - A single fixed payload tried everywhere regardless of detected context.
    - Reporting an XSS finding based on the payload merely appearing unescaped in the response, without OOB execution confirmation.
    - A false positive against the clean/fixed targets.

!!! note "Norm"

    See §II.2, plus: context-detection, CSP-parsing, payload-generation (as a table of context → template, extensible), and CSRF-detection each in their own module.

!!! tip "Bonus (§II.7)"

    Auto-mutation: when the first context-appropriate payload is blocked (e.g. by output encoding the tool didn't anticipate), automatically try a small set of alternative encodings/techniques for that same context before giving up.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
clientside_injection/
├── ex00/
├── ex01/
└── capstone/
```

Each exercise is defended live against a fresh instance of your target. The capstone is run live against a target set — including at least one context or CSP configuration the evaluator modifies immediately beforehand — and is expected to adapt its generated payloads accordingly rather than relying on cached/hardcoded results from earlier testing.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — xsstriad0

**Defense questions**

1. Run all three exploits live, end to end, and show the exfiltrated cookie value arriving at your listener each time.
2. For the DOM-based case specifically, explain exactly why a server-side WAF, no matter how well configured, cannot see this payload at all.
3. Show your blocklist bypass for one of the three — what did the filter author's mental model get wrong?
4. Fill in the source/sink table live for a payload I describe to you that you haven't seen before.
5. What is the actual difference in real-world severity between stored and reflected XSS, and why?

### A.1 — csrfstrike0

**Defense questions**

1. Open your attack page live in an authenticated browser session and show the state change happen.
2. Walk through exactly what `SameSite=Lax` does and does not stop for this specific endpoint and this specific attack shape.
3. Why is a synchronizer token a stronger fix than relying on `SameSite` alone — what threat model gap does `SameSite` not cover (think: subdomain-hosted attacker content, or older/misbehaving browsers)?
4. Why does allowing this action via GET make the vulnerability strictly worse, independent of the CSRF-token question?

### A.2 — Capstone: xsscsrf_confirm

**Defense questions**

1. Run this against your three XSS contexts live — narrate how the detected context changes the generated payload each time.
2. Show a case where CSP detection correctly identifies that no bypass is available, and the tool honestly reports failure instead of firing a payload that won't execute.
3. Walk through the OOB confirmation for one finding — what specifically proves execution happened versus the payload merely being present in the HTML?
4. Run the CSRF module against your Exercise 01 target live and show the generated PoC actually working.
5. Why does pairing an XSS finding with a CSRF finding on the same application matter for a real report's severity assessment?

**Test / edge cases**

- [ ] A marker reflected inside an HTML comment: correctly detected as a distinct (usually low-value) context, not conflated with a text-node context.
- [ ] A marker reflected in a context where the surrounding quotes are inconsistent/malformed HTML (browser error-recovery territory): tool reports lower confidence rather than a confident wrong payload.
- [ ] A CSP with a `nonce`-based script-src: correctly recognized as effectively unbypassable by this tool's technique set, reported honestly rather than attempting a doomed inline payload.
- [ ] A state-changing endpoint that already has a correctly-implemented synchronizer token: CSRF module correctly reports not-vulnerable, not a false positive from merely finding a form.
- [ ] A reflected marker appearing in multiple contexts simultaneously on one page (e.g. once in an attribute, once in a script block): both contexts detected and payloaded separately.
- [ ] An OOB callback that arrives but with a corrupted/unexpected token: not falsely attributed to a candidate payload it didn't actually come from.
