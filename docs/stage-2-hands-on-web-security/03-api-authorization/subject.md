---
title: "The Subject"
description: "The API-specific vocabulary for exactly the bugs Access Control and IDOR already taught you to find, plus two failure modes that only really bite once an …"
---
# Modern API Authorization: BOLA, BFLA, and Rate-Limit Abuse: The Subject

*Subject 3 of 7 — Hands-On Web Security + Code Review · Version 1.0 — September 2026*

> The API-specific vocabulary for exactly the bugs Access Control and IDOR already taught you to find, plus two failure modes that only really bite once an application becomes a JSON API instead of a server-rendered site: mass assignment, and rate limits that exist per-endpoint instead of per-user-intent.

## Chapter 00 — Foreword

> *BOLA is IDOR with a job title. The bug is identical; what changed is that an API makes every single object reference explicit in the URL or body, which means an API has more of them, checked less often, by developers who assumed the frontend would never ask for the wrong one.*

The OWASP API Security Top 10 exists as a separate list from the web Top 10 because APIs concentrate certain bug classes: Broken Object Level Authorization (BOLA) and Broken Function Level Authorization (BFLA) are the API-native names for the vulnerabilities you already found by hand in Access Control and IDOR, but APIs also introduce mass assignment (a request body silently accepted as a full object update) and rate-limit bypass patterns specific to how API clients batch and paginate.

## Chapter I — Introduction

You will attack a small REST API for BOLA and BFLA using a systematic per-object, per-role test matrix, exploit mass assignment to set fields a client was never supposed to control (like a privilege flag), and defeat a naive IP-based rate limiter through header spoofing and distributed request patterns. The capstone extends your Access Control capstone into a full OpenAPI-spec-driven authorization test suite.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of exploitability or of a fix working must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation targets DVWA, Juice Shop, WebGoat, PortSwigger Academy labs, HackTheBox/lab machines, or an application you wrote — never a third party without written authorization.

## Chapter III — Mandatory Part

### Exercise 00 — bola_bfla0

- **Turn-in dir:** api_authorization/ex00/
- **Files:** vuln_api.py, EXPLOIT.md, evidence/
- **Allowed:** Postman/Burp/curl against your own REST API
- **Forbidden:** automated BOLA/BFLA scanners

**Description.** A small deliberately vulnerable REST API (e.g. a multi-tenant task-management API) attacked systematically for BOLA (object-level) and BFLA (function-level) across every documented endpoint, using a test matrix rather than opportunistic poking.

!!! success "Mandatory"

    - An OpenAPI/Swagger spec (yours, hand-written or generated) documenting every endpoint, method, and expected role — used as the systematic checklist for what follows, not skipped in favor of ad hoc exploration.
    - For every endpoint that takes an object ID, a demonstrated BOLA finding or an explicit "tested, not vulnerable" note with the negative-test evidence — reusing the ownership-aware testing discipline from Access Control and IDOR, applied API-wide rather than to one or two hand-picked endpoints.
    - For every endpoint intended to be role-restricted, a demonstrated BFLA finding or an explicit "tested, not vulnerable" note — including at least one finding where a documented-admin-only endpoint is reachable by a regular authenticated user with no role check at all.
    - At least one nested-object BOLA: an endpoint where the vulnerable object reference is not the primary resource ID but a nested/related ID (e.g. `/projects/5/tasks/99` where project 5 is the caller's own but task 99 belongs to a different project entirely) — a subtler variant than a flat "change the ID" case.
    - A written coverage table: every endpoint from the spec, tested/not-tested, and result — proving systematic coverage, not cherry-picked findings.

!!! failure "Forbidden"

    - Any automated BOLA/BFLA scanner for the mandatory part.
    - Skipping the OpenAPI spec and testing ad hoc — the systematic coverage table is a mandatory deliverable, not optional documentation.
    - A finding claimed without a fresh, reproducible request/response pair.

!!! note "Norm"

    See §II.2, plus: EXPLOIT.md organized by the same structure as the coverage table, one row per endpoint.

!!! tip "Bonus"

    A GraphQL-shaped BOLA on a nested field resolver (if you extend your Exercise 01 GraphQL target from Advanced Web Exploitation II), showing the same bug class appearing in a non-REST API shape.

### Exercise 01 — massassign0

- **Turn-in dir:** api_authorization/ex01/
- **Files:** vuln_api.py, EXPLOIT.md, evidence/
- **Allowed:** your Exercise 00 API extended, Burp/curl
- **Forbidden:** automated mass-assignment fuzzers

**Description.** A profile-update endpoint that naively binds the entire request body onto a user object (a common ORM/serializer convenience), exploited to set fields the client-facing form never exposes — including a privilege flag.

!!! success "Mandatory"

    - A vulnerable endpoint that accepts a JSON body and applies it to a user/account object using a naive "update all provided fields" pattern (e.g. `user.update(**request.json)` or an ORM's mass-assignment convenience) rather than an explicit allowlist of updatable fields.
    - Discover the existence of a non-exposed but present field (e.g. `is_admin` or `role`) via a source/schema leak (an API response that includes the field even though the client form doesn't let you set it, or an OpenAPI spec that documents it) — demonstrating the discovery step, not just assuming the field's name.
    - Successfully set that field via the mass-assignment endpoint (e.g. `PATCH /profile {"name": "x", "is_admin": true}`) and demonstrate the resulting privilege change taking effect (e.g. now able to reach a BFLA-protected endpoint from Exercise 00).
    - The correct fix applied and verified: rewrite the endpoint with an explicit allowlist of client-updatable fields, with your exploit payload shown either rejected or silently ignored for the disallowed field (your choice, documented and justified) while legitimate fields still update correctly.
    - A written note connecting this to Secure Coding Principles' "least privilege": mass assignment is what happens when a data-binding convenience is given more privilege (the ability to set any field) than the endpoint's actual purpose requires.

!!! failure "Forbidden"

    - Any automated mass-assignment fuzzing tool for the mandatory part.
    - Guessing the sensitive field name with no discovery evidence shown.
    - A fix that filters based on a denylist of dangerous field names instead of an allowlist of permitted ones.

!!! note "Norm"

    See §II.2, plus: the vulnerable and fixed endpoints clearly separated; the allowlist expressed as an explicit, inspectable data structure.

!!! tip "Bonus"

    Chain this with Exercise 00's BOLA: use mass assignment to modify a field on an object you shouldn't have write access to at all, combining both bug classes into one request.

### Exercise 02 — ratelimit_bypass0

- **Turn-in dir:** api_authorization/ex02/
- **Files:** EXPLOIT.md, evidence/
- **Allowed:** your own API with a naive rate limiter added, Burp/scripted requests
- **Forbidden:** none beyond the global list

**Description.** A naive IP-based rate limiter protecting a login/brute-force-sensitive endpoint, defeated through header-based IP spoofing and a distributed-source simulation — proving that rate limiting keyed on the wrong identity dimension is not real protection.

!!! success "Mandatory"

    - A rate limiter on your API's login endpoint keyed purely on source IP (e.g. N failed attempts per IP per minute) — the deliberate, realistic-looking weak design.
    - Bypass via trusted-header spoofing: if your app stack (reasonably) trusts an `X-Forwarded-For` header from a reverse proxy, demonstrate that sending a different spoofed value per request resets the rate limiter's per-IP counter each time, allowing unlimited attempts — with the exact header behavior shown.
    - Bypass via account-targeted distribution: demonstrate that even without header spoofing, an attacker attempting credential stuffing across *many different accounts* from one IP is rate-limited the same as an attacker attempting many passwords against *one* account — and explain why IP-based limiting fails to distinguish "one attacker brute-forcing one account" from "one attacker credential-stuffing many accounts," both of which it should catch but only actually bounds the former effectively.
    - The correct fix applied and verified: a rate limiter keyed on a combination of identity dimensions (e.g. per-account *and* per-IP, with the per-account limit being the one that actually matters for credential stuffing), with `X-Forwarded-For` only trusted when it genuinely comes from your known proxy (validated by connection source, not blindly trusted from any client) — your spoofing bypass re-run and shown failing.
    - A written note on the general principle: a rate limiter is a proxy for "is this the same attacker," and any bypass that finds an identity dimension the limiter isn't keyed on defeats it — the fix is choosing (or combining) the right dimension for the specific threat, not just "add a rate limiter."

!!! failure "Forbidden"

    - Testing against any target other than your own instance.
    - A fix that just raises the rate-limit threshold instead of addressing the identity-dimension problem.

!!! note "Norm"

    See §II.2, plus: the header-trust configuration and the rate-limit logic each isolated so the fix is a clean, defensible diff.

!!! tip "Bonus"

    Add a CAPTCHA or proof-of-work challenge after N failures as a second, orthogonal layer, and explain why this is a defense-in-depth addition rather than a replacement for fixing the identity-dimension problem.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** spec-driven systematic coverage (Exercise 00), the mass-assignment discovery-then-exploit pattern (Exercise 01), and identity-dimension-aware rate-limit probing (Exercise 02), all driven off one machine-readable source of truth (the OpenAPI spec) instead of three separately hand-run exercises. A real API has dozens to hundreds of endpoints; the entire point of Exercise 00's coverage table was proving systematic testing scales, and this capstone is what makes that scaling actually automatic rather than a manually-maintained spreadsheet.

### Capstone — apiauthz_suite

- **Turn-in dir:** api_authorization/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** An OpenAPI-spec-driven authorization test suite: given a target's OpenAPI/Swagger document and credentials for at least two roles, automatically generates and runs the full BOLA/BFLA/mass-assignment/rate-limit-identity test matrix from Exercises 00-02 across every documented endpoint — the systematic coverage from Exercise 00's hand-built table, fully automated and extended to the other two bug classes.

!!! success "Mandatory"

    - Spec ingestion: parses an OpenAPI/Swagger document, extracting every endpoint, method, parameter (including path-parameter object IDs), and request-body schema (including which fields exist even if not documented as client-settable, when discoverable from response schemas).
    - BOLA/BFLA module: for every endpoint with a path-parameter object ID, replays it under every provided role/account pair (reusing the Access Control and IDOR capstone's ownership-aware matrix logic) and reports unexpected-allow findings; for every endpoint, additionally checks whether a lower-privilege role can reach it at all (BFLA).
    - Mass-assignment module: for every write endpoint (POST/PUT/PATCH), compares the request-body schema's documented client-settable fields against any additional fields discoverable in corresponding GET-response schemas, and attempts submitting each additional field with a probe value, reporting any that are accepted and reflected/take effect.
    - Rate-limit-identity module: for the login/auth-sensitive endpoints identified from the spec (by path naming convention or explicit config), runs both the header-spoofing probe and the many-accounts-from-one-IP probe from Exercise 02, and reports which identity dimensions are and are not effectively bounded.
    - One consolidated, spec-referenced report: every finding tied back to its exact OpenAPI path/operation, with evidence and severity, plus an explicit coverage summary (X of Y endpoints tested per module, with reasons for any skipped).
    - Demonstrated end to end against your own Exercise 00/01/02 API (vulnerable) and a fixed version, correctly rediscovering all your manually-found vulnerabilities automatically and reporting zero false positives against the fixed version.

!!! failure "Forbidden"

    - Any existing API security scanner (e.g. a commercial DAST-for-APIs product) doing the work for you.
    - A tool that requires manual endpoint-by-endpoint configuration instead of driving itself from the spec.
    - False positives against the fixed target.

!!! note "Norm"

    See §II.2, plus: spec-parsing, and each of the three test modules, cleanly separable and independently runnable against a parsed-spec object.

!!! tip "Bonus (§II.7)"

    Auto-generate a minimal OpenAPI spec via black-box traffic observation (from a captured HAR/Burp export) for targets that don't publish one, feeding the same downstream modules.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
api_authorization/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live against your own API. The capstone is run live against a spec/target pair the evaluator selects (your vulnerable set or your fixed set), with the suite expected to produce an accurate, spec-referenced report either way.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — bola_bfla0

**Defense questions**

1. Walk through your coverage table — pick an endpoint at random and show me the test you ran and its result.
2. Explain the nested-object BOLA finding specifically — why is it subtler than a flat ID-substitution case, and why would a naive automated scanner likely miss it?
3. What's the actual difference in root cause between a BOLA and a BFLA finding, even though both often present as "wrong user got a 200"?
4. How would you prioritize fixing your findings for a real engagement report — which ones first, and why?

### A.1 — massassign0

**Defense questions**

1. Show me exactly how you discovered the hidden `is_admin` field before exploiting it.
2. Walk through the exploit live and show the resulting privilege change taking effect against an actual protected endpoint.
3. Why is an allowlist structurally better here than a denylist, using the same reasoning pattern from every earlier injection fix in this roadmap?
4. What's the ORM/framework-level habit that causes this bug class to recur across completely different codebases?

### A.2 — ratelimit_bypass0

**Defense questions**

1. Demonstrate the header-spoofing bypass live against your vulnerable version.
2. Explain precisely why per-account rate limiting catches credential stuffing in a way per-IP limiting structurally cannot.
3. Why is blindly trusting `X-Forwarded-For` from any client a security bug independent of rate limiting — what else could an attacker abuse it for (tie back to Host-header-injection style client-trust issues from HTTP Internals)?
4. Show the fixed version resisting your original bypass, live.

### A.3 — Capstone: apiauthz_suite

**Defense questions**

1. Run the full suite against your vulnerable API live and narrate findings as they appear, tied back to the spec.
2. Show me the coverage summary — what fraction of endpoints got fully tested, and what's the honest reason for anything skipped?
3. Walk through one BOLA finding's evidence trail from spec entry to confirmed vulnerability.
4. Run it against your fixed API and confirm zero false positives, live.
5. Why does driving everything from the OpenAPI spec matter more here than it did for the earlier, hand-run exercises?

**Test / edge cases**

- [ ] An endpoint documented in the spec but actually removed/404ing on the live target: reported as a spec-drift note, not a false vulnerability or a silent skip.
- [ ] A field present in a GET response only because of a serialization quirk (e.g. a computed/read-only field that looks assignable but isn't): mass-assignment module's probe correctly determines it doesn't actually take effect, avoiding a false positive.
- [ ] Two roles that are supposed to have identical access to one endpoint by design: BOLA/BFLA module correctly does not flag this as a finding.
- [ ] A spec with inconsistent or missing parameter types: tool degrades gracefully (skips that specific check with a clear note) rather than crashing the whole run.
- [ ] Rate-limit module run against an endpoint with no rate limiting configured at all (by design, e.g. a public read-only search): correctly reported as a separate, lower-severity or explicitly-out-of-scope note rather than conflated with a login-endpoint finding.
