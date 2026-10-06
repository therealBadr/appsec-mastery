---
title: "The Subject"
description: "Authentication answers \"who are you.\" Access control answers the much more frequently broken question: \"what are you allowed to touch.\" Build a real RBAC …"
---
# Access Control Models and IDOR: The Subject

*Subject 4 of 7 — Security Fundamentals · Version 1.0 — September 2026*

> Authentication answers "who are you." Access control answers the much more frequently broken question: "what are you allowed to touch." Build a real RBAC engine, then break a deliberately careless one by walking straight through it — no exploit needed, just a changed ID.

## Chapter 00 — Foreword

> *Broken access control doesn't announce itself with an error. It announces itself with a 200 OK for a request that should never have been allowed to ask.*

OWASP has ranked broken access control the single most common web vulnerability class for years running, and the reason is structural: authentication is one check, run once, at login. Access control is thousands of checks, one per sensitive action, and every single one of them has to be implemented correctly — the classic every-defender-must-win, one-attacker-success asymmetry, playing out at the level of individual API endpoints.

## Chapter I — Introduction

You will implement DAC, then RBAC, as real enforcement layers (not just data models) around a small app, then attack a deliberately careless second app for IDOR (Insecure Direct Object Reference) by simply changing IDs in otherwise-legitimate requests, and finally attack function-level access control by discovering and calling admin-only endpoints as a low-privilege user. The capstone builds an authorization fuzzer that systematically tests every discovered endpoint across every discovered role.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of the form "this is exploitable" or "this fix works" must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation in this subject targets DVWA, Juice Shop, WebGoat, or an application you wrote — running locally or on a VPS you own. Never a third party without written authorization.

## Chapter III — Mandatory Part

### Exercise 00 — rbacengine0

- **Turn-in dir:** access_control_idor/ex00/
- **Files:** rbacengine0.py, README.md
- **Allowed:** Flask/minimal WSGI app, your own authz layer
- **Forbidden:** Flask-Principal, casbin, or any prebuilt authz/RBAC library

**Description.** A small app implementing DAC (owner-only object access) and RBAC (role-gated actions) as a real, centrally-enforced authorization layer — not scattered `if user.role == "admin"` checks copy-pasted into every route.

!!! success "Mandatory"

    - DAC: every object (e.g. a document, a post) has an owner; a decorator/middleware you write enforces that only the owner (or an explicitly-shared collaborator, if you implement sharing) can read/modify/delete it — enforced in one central place, not per-route.
    - RBAC: at least three roles (e.g. viewer/editor/admin) with a defined permission matrix (which role can perform which action on which resource type), enforced through a single `require_permission(action, resource)`-style check reused across every route, not reimplemented per route.
    - A demonstration that removing a user's role mid-session immediately revokes access on their next request — no caching of stale permissions.
    - A negative-testing suite: for every route, a test proving the wrong role/non-owner gets a 403, not merely that the right role gets a 200 — access control bugs are almost always "forgot to add a check," so the tests must specifically probe for the check's absence.
    - A written explanation of the DAC/MAC/RBAC distinction: why DAC (owner discretion) and RBAC (centrally defined roles) solve different problems, and where MAC (mandatory, centrally enforced regardless of owner preference — think classified data levels) would be the right model instead of either.

!!! failure "Forbidden"

    - Any prebuilt authorization library or framework extension.
    - A permission check duplicated inline in multiple routes instead of one central, reused enforcement function.
    - A test suite that only proves authorized access works, with no negative (should-be-denied) cases.

!!! note "Norm"

    See §II.2, plus: the permission matrix as an explicit, inspectable data structure, not implicit in scattered conditionals.

!!! tip "Bonus"

    Attribute-based access control (ABAC) extension: a rule that depends on a resource attribute at request time (e.g. "editors can only edit posts created in the last 24 hours") layered on top of the RBAC check.

### Exercise 01 — idorhunt0

- **Turn-in dir:** access_control_idor/ex01/
- **Files:** EXPLOIT.md, evidence/
- **Allowed:** Burp, browser, manual requests against your own deliberately vulnerable target
- **Forbidden:** Autorize or any automated IDOR-detection Burp extension (build the understanding first; the capstone builds the automation)

**Description.** A deliberately careless multi-tenant app (you build it, modeled on a real SaaS pattern — e.g. invoices, private messages, or account settings keyed by a sequential or guessable ID) exploited entirely by hand for IDOR, horizontal and vertical, with every finding proven by actually retrieving another user's data.

!!! success "Mandatory"

    - Horizontal IDOR: as User A, access User B's private resource (e.g. `GET /invoices/1042` belonging to another account) purely by changing the ID in an otherwise-legitimate authenticated request, and retrieve real (seeded) private data belonging to User B.
    - At least one IDOR in a non-GET action: not just reading another user's data but modifying or deleting it (e.g. `PUT /account/1042/email` changing another user's email) via the same ID-substitution technique — proving IDOR is a write/business-logic problem, not only an information-disclosure one.
    - Vertical privilege escalation via IDOR: a low-privilege user accessing or modifying an admin-only resource through an object reference the app fails to role-check, not just owner-check (e.g. a regular user hitting `/admin/users/7/promote` because the endpoint checks "does this user ID exist" but not "is the caller an admin").
    - An enumeration proof: given the ID scheme is sequential or otherwise predictable, demonstrate that this isn't a one-off — write a short script that walks a range of IDs and confirms multiple different users' data is accessible, with the count of accessible-vs-total.
    - A written root-cause explanation for each finding: precisely which check is missing (no ownership check at all vs. ownership checked but role never checked vs. object existence checked but ownership never checked) — these are three different code-level bugs that all present as "IDOR."

!!! failure "Forbidden"

    - Autorize or any automated IDOR-detection extension for the mandatory part.
    - Testing against a target you did not build/seed yourself with known test data.
    - A finding you can't reproduce on demand from a clean re-login.

!!! note "Norm"

    See §II.2, plus: EXPLOIT.md structured finding → request/response evidence → precise root cause, per issue.

!!! tip "Bonus"

    Use non-sequential but still-predictable IDs (e.g. a poorly-implemented "random" ID generator with insufficient entropy) and demonstrate the enumeration still succeeding at a measurably slower but still practical rate.

### Exercise 02 — functionlevel0

- **Turn-in dir:** access_control_idor/ex02/
- **Files:** EXPLOIT.md, evidence/
- **Allowed:** Burp, browser dev tools, manual requests
- **Forbidden:** any automated endpoint-discovery/fuzzing tool (manual/JS-source-reading discovery only for this exercise)

**Description.** Broken Function Level Authorization: discover admin-only or hidden functionality through client-side artifacts (JS source, hidden form fields, API responses that reveal endpoint names) and successfully call it as an unprivileged user — the exact class of bug behind most "hidden admin panel" real-world reports.

!!! success "Mandatory"

    - Discover at least two admin-only or otherwise privileged endpoints without being told what they are — by reading client-side JavaScript source for API routes referenced but not linked in the low-privilege UI, by noticing an API response that includes fields/links only relevant to a higher role, or by noticing a predictable naming pattern (e.g. `/api/users/list` existing alongside a linked `/api/users/me`).
    - Successfully call each discovered endpoint as a low-privilege authenticated user (not unauthenticated — this is about role-checking, distinct from Access Control 101) and demonstrate it returning privileged data or performing a privileged action.
    - A written distinction between this and Exercise 01's vertical-IDOR case: here, the endpoint itself has no object-ID-based check to exploit — the bug is purely "this route has no role/permission check at all," discoverable through UI/client asymmetry rather than ID guessing.
    - A demonstration of the discovery method itself as a reusable technique: show the specific JS source line, hidden field, or response artifact that led you to the endpoint, so the technique — not just the one finding — is documented.
    - A note on why "security through obscurity" (hiding the link in the UI without also checking permissions server-side) fails completely once client-side code is inevitably readable.

!!! failure "Forbidden"

    - Brute-forcing/fuzzing a wordlist of common admin paths for this exercise — the point is demonstrating discovery from actual client-side artifacts, not guessing (a wordlist-based approach is exactly what the capstone automates).
    - A finding you discovered by being told the endpoint name out of band instead of through the documented discovery method.

!!! note "Norm"

    See §II.2, plus: EXPLOIT.md documents discovery method and exploitation as two distinct, evidenced steps per finding.

!!! tip "Bonus"

    Find and exploit a case where the frontend correctly hides a button/link based on role, but the same action is also reachable through a slightly different, unprotected API path (e.g. a bulk/legacy endpoint) — a "second door" the developer forgot.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** the full access-control model from Exercise 00 (to know what "should" be allowed per role, as a baseline to diff against), the ID-substitution technique from Exercise 01, and the endpoint-discovery/role-asymmetry reasoning from Exercise 02 — because a matrix tester that doesn't understand ownership will flag every legitimate "user reads their own resource" call as a false positive the moment it replays that request under a different user's session with the same object ID, and one that doesn't understand role hierarchy will flag an admin successfully calling a viewer-level endpoint as a "finding" when it's actually expected behavior.

### Capstone — authzfuzz

- **Turn-in dir:** access_control_idor/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** An authorization fuzzer: given a captured set of authenticated requests (a HAR file or Burp export) from multiple roles, systematically replays every request under every other role's session and flags any response that shouldn't have succeeded — turning the manual hunting from Exercises 01-02 into a repeatable matrix test.

!!! success "Mandatory"

    - Ingests a set of captured authenticated requests spanning at least three distinct role sessions (reusing your Exercise 00 app's three roles is expected) — a HAR file, a Burp XML/JSON export, or your own capture format.
    - For every captured request, replays it under every *other* captured role's session/auth material, producing a full role × request matrix.
    - Classifies each replayed result as expected-deny (403/401 or equivalent — correct), expected-allow (a lower-privilege action a higher role should also be able to do — correct), or **unexpected-allow** (a request that succeeded under a role that should have been denied — a finding), using a configurable expected-permission-matrix you define (reusing Exercise 00's matrix structure) rather than guessing correctness from status code alone.
    - Specifically handles the object-ownership dimension: when a request references an object ID, the tool must recognize whether the replaying role legitimately owns a *different* object with the same shape (and therefore a same-role replay against their own ID is expected-allow) versus is reaching into another user's object entirely (unexpected-allow) — not simply "role X got a 200, flag it."
    - One consolidated report: every unexpected-allow finding with the original request, the replayed request/response, the role pairing, and a severity note (read vs. write/delete, and horizontal vs. vertical, distinguished as in Exercises 01-02).
    - Demonstrated end to end against your own Exercise 00 (clean) and Exercise 01/02 (vulnerable) targets — correctly reporting zero unexpected-allow findings against the clean target and correctly rediscovering your manually-found Exercise 01/02 vulnerabilities automatically, unattended.

!!! failure "Forbidden"

    - Autorize or any existing authorization-testing Burp extension doing the classification for you.
    - Flagging every cross-role 200 as a finding without the ownership-aware reasoning described above — this produces overwhelming false positives and is explicitly graded against.
    - A false positive against the Exercise 00 clean target — this capstone is graded on the same zero-false-positive standard as Cryptography Fundamentals' capstone, for the same reason: a noisy authz scanner gets ignored.

!!! note "Norm"

    See §II.2, plus: ingestion, matrix-replay, classification (with the ownership-aware logic isolated and independently testable), and reporting each in their own module.

!!! tip "Bonus (§II.7)"

    Auto-discovery mode: given only one role's captured traffic plus a wordlist of common endpoint-name variations, propose likely sibling endpoints for other roles (extending Exercise 02's discovery technique) before the matrix-replay stage even runs.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
access_control_idor/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live against a fresh instance of your target, reseeded by the evaluator with different user IDs. The capstone is run live against a target the evaluator modifies immediately beforehand — a permission check added or removed — and is expected to correctly detect the change.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — rbacengine0

**Defense questions**

1. Walk me through your central permission-check function, live, tracing one request through it end to end.
2. Show me a negative test failing on purpose (temporarily remove a check) — prove your tests actually catch a real regression.
3. Why would scattering `if role == admin` checks across fifty routes make this app's security posture fundamentally harder to audit than your centralized approach, even if both are "correct" on day one?
4. Give a concrete resource/action where MAC, not RBAC, would be the correct model, and explain why RBAC alone can't express it.

### A.1 — idorhunt0

**Defense questions**

1. Reproduce your horizontal IDOR live, from a fresh login as User A, right now.
2. For your vertical-escalation finding, trace exactly which authorization check is present and which is missing in the endpoint's logic.
3. Why does an IDOR on a write/delete action rate more severely than one on a read — walk through a concrete worst case.
4. Show your enumeration script live and explain how you'd responsibly bound its request rate if this were a real, authorized engagement against a production system.

### A.2 — functionlevel0

**Defense questions**

1. Show me the exact client-side artifact that led you to each discovered endpoint.
2. Why is hiding a link in the UI, without a server-side check, equivalent to no security at all once someone reads the JavaScript?
3. What's the precise difference, in terms of what code is missing, between this exercise's findings and Exercise 01's vertical IDOR?
4. If you were writing the fix for one of your findings, what exactly would you add, and where — the same central-permission-check pattern from Exercise 00?

### A.3 — Capstone: authzfuzz

**Defense questions**

1. Run this against your Exercise 01 target live and narrate the matrix as it builds — show me exactly where an unexpected-allow gets classified and why.
2. Run it against your clean Exercise 00 target live — walk through why a same-role, same-owner replay correctly does not get flagged.
3. How does your tool distinguish "this role should legitimately be able to do this" from "this succeeded but shouldn't have" — show me the actual logic, not just the output.
4. What's the worst-case request volume for this tool against an app with N endpoints and M roles, and how would you make that practical against a real engagement with rate limits?
5. Explain a finding your tool produces that a naive "flag every unexpected 200" version would have missed or gotten wrong.

**Test / edge cases**

- [ ] A role attempting an action on a resource type that doesn't exist for them at all (e.g. viewer role replaying an admin-only bulk-delete against no matching object): correctly classified, not a crash.
- [ ] Two different users under the same role, replaying each other's object IDs: correctly recognized as horizontal — same role, different owner — distinct from a vertical finding.
- [ ] A captured request whose auth material has since expired: reported as inconclusive for that specific replay, not silently treated as a deny (which would hide a real vulnerability) or an allow (false positive).
- [ ] An endpoint that is genuinely public/unauthenticated by design (e.g. a public read endpoint): correctly excluded from the authz matrix entirely rather than flagged as "every role can access this."
- [ ] A write request replayed under a different role that would, if actually executed, corrupt your test data for subsequent replays: the tool's handling of this (dry-run mode, test-data isolation, or explicit ordering) is documented and justified.
- [ ] A role hierarchy where a higher role should be able to do everything a lower role can (admin ⊇ editor ⊇ viewer): correctly modeled as inheritance in the expected-permission-matrix rather than requiring every combination spelled out by hand.
