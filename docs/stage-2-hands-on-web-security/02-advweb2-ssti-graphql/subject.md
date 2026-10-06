---
title: "The Subject"
description: "A template engine given attacker-controlled template syntax is a code-execution primitive wearing the costume of a rendering bug."
---
# Advanced Web Exploitation II: SSTI and GraphQL Security: The Subject

*Subject 2 of 7 — Hands-On Web Security + Code Review · Version 1.0 — September 2026*

> A template engine given attacker-controlled template syntax is a code-execution primitive wearing the costume of a rendering bug. A GraphQL API with introspection on and no query-cost limiting is a full schema map handed to an attacker for free, plus a denial-of-service lever built into the query language itself.

## Chapter 00 — Foreword

> *A template engine and a SQL parser solve the same problem — turning a mini-language into output — and inherit the same vulnerability the moment user input is allowed to write the mini-language instead of fill in its blanks.*

Server-Side Template Injection gets less attention than SQLi or XSS, but it routinely escalates directly to remote code execution because template engines are, by design, small programming languages with filesystem and object access built in. GraphQL, meanwhile, inverts the REST attack surface: instead of many opaque endpoints, one endpoint exposes an entire queryable schema, and the query language itself — nesting, aliasing, batching — is the attack surface.

## Chapter I — Introduction

You will fingerprint and exploit SSTI against a real template engine (Jinja2), escalating from a rendering quirk to full remote code execution via Python object-introspection gadgets, then attack a GraphQL API for introspection-based schema disclosure, excessive-nesting denial-of-service, and an authorization bug that only exists because REST-style per-endpoint checks were bolted onto a single GraphQL endpoint incorrectly. The capstone builds one tool covering both.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of exploitability or of a fix working must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation targets DVWA, Juice Shop, WebGoat, PortSwigger Academy labs, HackTheBox/lab machines, or an application you wrote — never a third party without written authorization.

## Chapter III — Mandatory Part

### Exercise 00 — sstichain0

- **Turn-in dir:** advweb2_ssti_graphql/ex00/
- **Files:** vuln_app.py, EXPLOIT.md, evidence/
- **Allowed:** Jinja2 (deliberately misused), Flask
- **Forbidden:** tplmap or any automated SSTI exploitation tool

**Description.** A deliberately vulnerable Flask app that renders user input directly as a Jinja2 template string (instead of passing it as data into a template), exploited from initial fingerprinting through full remote code execution via Python's object-introspection chain.

!!! success "Mandatory"

    - A vulnerable endpoint using `render_template_string(user_input)` or equivalent — user input becomes template source, not template data.
    - Fingerprinting: demonstrate the classic detection payload (e.g. `{{7*7}}`) confirming template evaluation is happening, and explain what distinguishes this from a false-positive (e.g. the app merely echoing the string back unrendered).
    - Escalation via Python's object model: starting from an accessible template object (e.g. a string literal's `__class__`), walk the `__mro__`/`__subclasses__` chain by hand to reach a class useful for code execution (e.g. one wrapping `subprocess.Popen` or `os.system`), and execute an arbitrary command — with every step of the chain shown and explained, not a copy-pasted one-liner payload.
    - A written explanation of exactly why this differs from XSS even though both involve injecting into a rendering process: SSTI payloads execute *server-side*, in the template engine's own execution context, with access to server-side objects — not client-side JavaScript in a victim's browser.
    - The fix applied and verified: separate template (trusted, developer-authored) from data (untrusted, user-supplied) by passing user input as a template *variable* rather than concatenating it into the template *source*, with your exploit chain shown failing (the payload is now rendered as inert text, not evaluated).

!!! failure "Forbidden"

    - tplmap or any automated SSTI tool.
    - A "payload" copy-pasted from a cheat sheet without being able to walk the object-chain reasoning behind it during defense.
    - A fix that tries to sanitize/blocklist template-looking syntax instead of architecturally separating template from data.

!!! note "Norm"

    See §II.2, plus: fingerprinting and the escalation chain each documented as separate, reproducible steps.

!!! tip "Bonus"

    Demonstrate the equivalent vulnerability class in a second template engine (e.g. Jinja2 vs. a Node/EJS-style engine you set up) and note the escalation-path differences.

### Exercise 01 — graphqlrecon0

- **Turn-in dir:** advweb2_ssti_graphql/ex01/
- **Files:** EXPLOIT.md, evidence/
- **Allowed:** a GraphQL server you stand up (e.g. Graphene/Ariadne) with introspection enabled, Burp/GraphiQL/manual requests
- **Forbidden:** InQL or any automated GraphQL security scanner (for the mandatory part — cross-checking afterward is fine)

**Description.** A GraphQL API with introspection enabled and no query-complexity limiting, attacked to fully map its schema without documentation, then abused for a resource-exhaustion denial-of-service via deeply nested/circular queries.

!!! success "Mandatory"

    - Full schema recovery via the standard introspection query (`__schema`) sent by hand, parsed into a readable map of every type, field, and mutation — including any fields/mutations not exposed in the application's own documented UI, demonstrating that introspection alone defeats "security by not documenting it."
    - Identify at least one sensitive field or mutation discoverable only through introspection (e.g. an internal-sounding field, or a mutation with no corresponding UI control) and demonstrate querying/calling it directly.
    - A deeply nested query attack: construct a query exploiting GraphQL's natural support for nested/recursive field selection (e.g. a self-referential relationship queried many levels deep) to force the server to do exponentially more work than a normal query, measured as a real, demonstrated response-time/resource spike on your own instance — not just asserted as theoretically possible.
    - A batching/aliasing attack: demonstrate using GraphQL query aliasing to submit what is effectively dozens of duplicate queries (e.g. dozens of aliased login-mutation attempts) in a single HTTP request, and explain why an endpoint-level rate limiter (counting HTTP requests) completely misses this.
    - The fixes applied and verified: introspection disabled in production (or gated behind auth), and a query-complexity/depth limiter added and shown correctly rejecting your nested-query and aliasing attacks afterward.

!!! failure "Forbidden"

    - InQL or any automated GraphQL scanner for the mandatory schema-recovery/exploitation steps.
    - Claiming the DoS attack works without a real measured resource/time impact on your own instance.
    - A fix that merely rate-limits by HTTP request count without addressing query complexity/depth directly — shown to still be bypassable by the aliasing technique otherwise.

!!! note "Norm"

    See §II.2, plus: EXPLOIT.md documents the recovered schema, then each attack with its query and measured impact.

!!! tip "Bonus"

    A GraphQL-specific IDOR: find an object-fetching query (e.g. `user(id: X)`) with no ownership check, reusing your Access Control and IDOR technique directly against this new query shape.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** the object-introspection escalation reasoning from Exercise 00, GraphQL schema-graph reasoning and complexity estimation from Exercise 01, and OOB confirmation (reused from the Server-Side Injection and Client-Side Injection capstones) as the common confirmation technique across both — an SSTI finding and a GraphQL-exposed dangerous mutation are both confirmed the same way: get the target to do something observable outside the response itself. Someone who only learned SSTI has no model for why a GraphQL schema graph needs its own complexity-scoring algorithm; someone who only learned GraphQL has no path from "found a template-looking field" to actual code execution.

### Capstone — ssti_graphql_auditor

- **Turn-in dir:** advweb2_ssti_graphql/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** One tool combining SSTI fingerprinting/OOB-confirmed exploitation with a GraphQL security auditor that performs introspection recovery, flags overly permissive/sensitive fields, and estimates query-complexity DoS risk — producing a report spanning both attack surfaces for a target that exposes either or both.

!!! success "Mandatory"

    - SSTI module: given a target endpoint, sends a small set of engine-fingerprinting payloads (Jinja2-style and at least one alternate-engine-style, e.g. a different delimiter convention), detects which (if any) evaluates, and — only on confirmed evaluation — attempts an OOB-confirmed code-execution payload (reusing the shared OOB-listener pattern from the Server-Side Injection capstone) rather than assuming success from a reflected calculation result alone.
    - GraphQL introspection module: sends the standard introspection query, parses the full schema, and produces a readable map of types/fields/mutations, flagging any field/mutation whose name suggests elevated sensitivity (an admin/internal/debug-sounding name) for manual follow-up.
    - GraphQL complexity-estimation module: given the recovered schema, statically estimates which fields participate in circular/self-referential relationships that could be exploited for nested-query DoS (reusing Exercise 01's attack shape), and generates a candidate deeply-nested query for each, without necessarily firing it destructively by default (a safe "would be exploitable" static estimate, with an opt-in live-fire confirmation mode against your own lab only).
    - GraphQL auth-boundary module: for each discovered query/mutation, attempts it both unauthenticated and under a low-privilege session (reusing your Access Control and IDOR test-harness pattern), flagging any that unexpectedly succeed.
    - One consolidated report spanning both SSTI and GraphQL findings for a target, each with evidence (OOB confirmation for SSTI, schema/query evidence for GraphQL) and severity.
    - Demonstrated end to end against your Exercise 00 (SSTI) and Exercise 01 (GraphQL) targets, correctly confirming each finding, plus fixed versions of both showing zero false positives.

!!! failure "Forbidden"

    - tplmap or InQL doing either module's core work for you.
    - Live-firing a destructive/high-resource-consumption complexity attack by default against any target — this must be an explicit, separately-invoked, own-lab-only mode.
    - A false positive against either fixed target.

!!! note "Norm"

    See §II.2, plus: SSTI-fingerprint, GraphQL-introspection, GraphQL-complexity-estimation, and GraphQL-auth-boundary each in their own module sharing the OOB-listener and HTTP layers.

!!! tip "Bonus (§II.7)"

    Extend the SSTI module to attempt engine-specific escalation chains for at least one engine beyond Jinja2, selecting the chain automatically based on the fingerprinting result.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
advweb2_ssti_graphql/
├── ex00/
├── ex01/
└── capstone/
```

Each exercise is defended live against your own targets. The capstone is defended live against a target the evaluator selects, with SSTI and GraphQL findings both required to show OOB or direct-evidence confirmation, never response-content inference alone.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — sstichain0

**Defense questions**

1. Walk the object-introspection chain live, from `{{7*7}}` to code execution, narrating what each step of the chain actually is.
2. Why does this specific payload structure work — what is Python's object model exposing that a template author never intended to expose?
3. What's the precise architectural difference between your vulnerable and fixed versions — show me the one-line diff and explain why it closes the entire class, not just this one payload.
4. Why is SSTI generally rated more severe than a comparable-looking XSS finding — what does the attacker gain?

### A.1 — graphqlrecon0

**Defense questions**

1. Walk through your introspection query and the schema map it produced, live.
2. Show your nested-query DoS live, with the measured impact — what specifically about GraphQL's execution model makes this possible in a way a REST endpoint typically isn't?
3. Explain the aliasing/batching attack and why an HTTP-request-count rate limiter is the wrong layer to stop it.
4. What does your query-complexity limiter actually measure, and how did you pick its threshold?

### A.2 — Capstone: ssti_graphql_auditor

**Defense questions**

1. Run the SSTI module against your Exercise 00 target live and narrate the fingerprint-then-confirm flow.
2. Run the GraphQL modules against Exercise 01 live — walk through the recovered schema and one flagged sensitive field.
3. Show your complexity-estimation logic on the schema — why does it estimate risk statically instead of always live-firing, and what's the tradeoff?
4. Why does OOB confirmation matter as much for SSTI here as it did for command injection and XXE earlier in the roadmap — what would a response-content-only confirmation get wrong?
5. Run everything against your fixed targets — confirm zero false positives, live.

**Test / edge cases**

- [ ] A target where the SSTI fingerprint payload is reflected but not evaluated (a false-positive trap, e.g. the app echoes `{{7*7}}` as literal text): correctly not flagged as vulnerable without OOB confirmation.
- [ ] A GraphQL schema with introspection disabled but a leaked schema file/documentation elsewhere: tool correctly reports introspection as blocked rather than silently failing with no explanation.
- [ ] A self-referential GraphQL relationship that is actually depth-limited server-side already: complexity module correctly detects the limit is enforced (via a live, bounded test) rather than flagging every circular relationship as exploitable.
- [ ] An SSTI target using a sandboxed template engine that blocks the object-introspection chain specifically: escalation correctly fails and is reported as "evaluation confirmed, escalation blocked" — a distinct, accurate finding rather than a false full-RCE claim.
- [ ] A GraphQL mutation that succeeds unauthenticated by design (e.g. a public signup mutation): auth-boundary module correctly excludes intentionally-public operations from findings, using a config/allowlist you define.
