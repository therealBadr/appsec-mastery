---
title: "The Subject"
description: "Every auth scheme is a promise about who a request is from."
---
# Authentication and Session Security: The Subject

*Subject 1 of 7 — Security Fundamentals · Version 1.0 — September 2026*

> Every auth scheme is a promise about who a request is from. Session cookies, JWTs, OAuth 2.0, and SAML each make that promise differently — and each breaks differently. Build a session store, break a JWT implementation six distinct ways, and walk through a full OAuth 2.0 authorization-code flow by hand.

## Chapter 00 — Foreword

> *A JWT is not "encrypted." It is a signed, base64-encoded confession the client is trusted to keep honest — and half the internet's auth bugs are one missing verification call away from that trust being misplaced.*

Authentication design failures outrank almost every other vulnerability class in real-world impact because they sit upstream of everything else — a broken auth check makes every other control irrelevant. This subject treats session-based auth, JWTs, and OAuth 2.0/SSO not as configuration options but as protocols with real state machines, real trust boundaries, and real, repeatedly-exploited failure modes.

## Chapter I — Introduction

You will build a minimal server-side session store from scratch (to understand what a framework is doing for you), attack a deliberately vulnerable JWT implementation across algorithm confusion, key confusion, and claim-tampering, and manually walk an OAuth 2.0 authorization-code flow end to end — including the redirect_uri and state-parameter attacks that account for most real OAuth bug bounty reports. The capstone builds an auth-scheme auditor that fingerprints and probes whichever of the three a target is using.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of the form "this is exploitable" or "this fix works" must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation in this subject targets DVWA, Juice Shop, WebGoat, or an application you wrote — running locally or on a VPS you own. Never a third party without written authorization.

## Chapter III — Mandatory Part

### Exercise 00 — sessionstore0

- **Turn-in dir:** auth_session_security/ex00/
- **Files:** sessionstore0.py, README.md
- **Allowed:** Flask/a minimal WSGI app, secrets module, your own store
- **Forbidden:** Flask-Login, Flask-Session, or any prebuilt session-management extension

**Description.** A hand-built server-side session store (session ID generation, storage, expiry, and rotation-on-privilege-change) used to back a minimal login flow — so the mechanics a framework usually hides are ones you've implemented and can break.

!!! success "Mandatory"

    - Session IDs generated with a cryptographically secure random source (`secrets.token_urlsafe` or equivalent) at sufficient length/entropy — justified in writing against a brute-force-guessing threat model, not assumed sufficient.
    - Server-side session store (in-memory dict is fine) keyed by session ID, storing user identity and an expiry timestamp; expired sessions are rejected and purged, not just ignored.
    - Session ID **rotates** on login and on any privilege escalation (e.g. becoming admin) — the pre-auth session ID must never be valid post-auth, demonstrated with a captured before/after.
    - Idle timeout and absolute timeout both enforced and independently testable (a session inactive too long is rejected even if within its absolute lifetime, and vice versa).
    - A written comparison: what a stateful (server-side) session buys you over a stateless token that a stolen valid session ID does not — specifically, the ability to revoke.

!!! failure "Forbidden"

    - Any session-management framework extension.
    - Session IDs derived from predictable data (timestamp, incrementing counter, username hash) — must be demonstrated to not be your scheme, not just asserted.
    - A revocation/logout that doesn't actually invalidate the server-side entry.

!!! note "Norm"

    See §II.2, plus: ID generation, storage, validation, and expiry each isolated in their own function.

!!! tip "Bonus"

    Concurrent-session policy: detect and optionally reject a second simultaneous login for the same account, with the detection logic shown working live.

### Exercise 01 — jwtbreak0

- **Turn-in dir:** auth_session_security/ex01/
- **Files:** jwtbreak0.py, EXPLOITS.md, evidence/
- **Allowed:** a deliberately vulnerable JWT-auth app you build, PyJWT or manual base64/HMAC for forging
- **Forbidden:** jwt_tool as a substitute for understanding — you may use it to cross-check after your own manual exploit works

**Description.** A small JWT-authenticated app with at least three real implementation flaws, exploited entirely by manually constructing forged tokens — base64-decoding, editing, and re-encoding JSON by hand, not through a GUI tool.

!!! success "Mandatory"

    - `alg:none` attack: given a server that fails to reject the `none` algorithm, forge a token with an arbitrary payload and no signature, and get it accepted — with the exact header/payload/signature-section bytes shown.
    - Algorithm confusion (RS256→HS256): given a server whose public key is discoverable (e.g. exposed via an endpoint or bundled client-side), forge an HS256 token signed with that public key as the HMAC secret, and get it accepted as if it were RS256-verified — with the verification-logic bug in the target app pointed out precisely.
    - Claim tampering against a weak-secret HS256 token: brute-force or dictionary-crack a deliberately weak signing secret offline, then forge a token with an escalated `role`/`sub` claim.
    - A JWT with no `exp` claim, or an `exp` claim the server never checks: demonstrate a token remaining valid indefinitely, and explain why this is a session-revocation problem structurally identical to what Exercise 00 solved with server-side state.
    - For each of the four exploits, a written root-cause explanation of the exact line of verification logic that is missing or wrong in the target — not just "JWTs are insecure."

!!! failure "Forbidden"

    - jwt_tool or jwt.io's debugger as your primary exploitation method (fine for double-checking your own manual forgery afterward).
    - A forged token you cannot rebuild by hand, live, without your saved script.
    - Testing against a JWT-auth service you do not own/run locally.

!!! note "Norm"

    See §II.2, plus: base64url encode/decode, HMAC signing, and token assembly each in their own function — no JWT library used for the actual forgery logic in Ex. 00–02 (a library is fine for the target app itself).

!!! tip "Bonus"

    A `kid` (key ID) header injection attack: manipulate the `kid` parameter to point the server at a file/key you control (e.g. path traversal into a predictable file, or SQL injection into a key-lookup query) and get your own signature accepted.

### Exercise 02 — oauthflow0

- **Turn-in dir:** auth_session_security/ex02/
- **Files:** OAUTH_WALKTHROUGH.md, evidence/
- **Allowed:** Burp, a real or sandboxed OAuth 2.0 provider (your own minimal implementation or a test app on a real provider)
- **Forbidden:** any OAuth client library as a black box you cannot narrate step by step

**Description.** A full OAuth 2.0 authorization-code flow captured and annotated request-by-request through Burp, followed by manual demonstrations of the two most common real-world OAuth bugs: `redirect_uri` manipulation and CSRF via a missing/unvalidated `state` parameter.

!!! success "Mandatory"

    - Full authorization-code flow captured end to end: authorization request, user consent, redirect back with `code`, code exchanged for an access token (and refresh token if issued), token used against a protected resource — every request and response annotated with what each parameter does.
    - A written, precise explanation of why the authorization code is exchanged server-side (confidential client) rather than the token being returned directly to the browser, and what specifically an implicit-grant flow gives up by skipping that step.
    - `redirect_uri` manipulation: against an app with loose redirect_uri validation (a test app you configure this way, since providers increasingly reject this by default), demonstrate the authorization code or token being redirected to an attacker-controlled URI, and explain the exact validation gap (exact match vs. prefix match vs. no validation).
    - Missing/predictable `state` parameter: demonstrate a login CSRF — an attacker's pre-generated authorization code/session bound to the victim's browser via a crafted link, resulting in the victim being logged into the attacker's account (session-swapping) — with the exact absence of state-parameter validation shown as root cause.
    - A written comparison of authorization-code, implicit, and client-credentials grant types: which is appropriate for which client type (server-side web app, SPA, machine-to-machine), and why using the wrong one is itself a vulnerability class.

!!! failure "Forbidden"

    - An OAuth client SDK used as a black box for the annotated flow — the point is narrating every parameter yourself.
    - Testing redirect_uri/state attacks against a real third-party provider's production app without authorization — use a provider's sandbox/test-app mode or your own minimal implementation.

!!! note "Norm"

    See §II.2, plus: OAUTH_WALKTHROUGH.md structured request → parameters → purpose → what-if-tampered, per step.

!!! tip "Bonus"

    Demonstrate PKCE (Proof Key for Code Exchange) closing the redirect_uri-interception attack for a public client (mobile/SPA), with a before/after.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** session-lifecycle reasoning, JWT structure/verification-bug patterns, and OAuth flow mechanics, plus the ability to first correctly identify which of the three schemes is even in play from raw traffic — a session cookie, a JWT in an Authorization header, and an OAuth redirect chain look completely different on the wire, and running the wrong probe set wastes an engagement's time and produces false negatives. Someone who only learned JWTs will misdiagnose a session-cookie app and find nothing; someone who only learned OAuth has no probes to run against the far more common plain session-cookie case.

### Capstone — authfingerprint

- **Turn-in dir:** auth_session_security/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A tool that, given a target login flow, identifies which authentication scheme (server-side session, JWT, or OAuth/SSO redirect) it uses, then runs the appropriate probe set from Exercises 00-02 automatically — session-fixation and rotation checks for session-based auth, algorithm/claim probes for JWTs, and redirect_uri/state checks for OAuth.

!!! success "Mandatory"

    - Scheme detection: given a captured login flow (a HAR file or a live target you drive through it), identifies which of session/JWT/OAuth is in use — cookie with an opaque value plus no client-side-decodable structure (session), a compact three-part base64url token (JWT), or a redirect chain through an `/authorize`-shaped endpoint with `client_id`/`redirect_uri`/`state` (OAuth) — reporting its confidence and the specific evidence.
    - For a detected session-cookie scheme: checks session-ID entropy (length/charset), whether the ID rotates across the login boundary (replay the pre-login cookie post-login and check if it's now authenticated), and whether logout actually invalidates server-side state (replay a cookie after logout).
    - For a detected JWT scheme: decodes and reports header/payload without verification, flags `alg:none` acceptance, flags missing `exp`, and — where a public key or JWKS endpoint is discoverable — attempts the RS256→HS256 confusion forgery and reports whether it was accepted.
    - For a detected OAuth scheme: extracts the authorization request's `redirect_uri` and `state` parameters, tests at least one redirect_uri variation (subdomain/path append/different domain) for acceptance, and checks whether the same authorization code/state can be replayed a second time (should fail — codes are single-use).
    - One consolidated report: detected scheme, every probe run for that scheme, pass/fail per probe with evidence, and an overall risk summary.
    - Demonstrated against all three of your own Exercise 00/01/02 targets, correctly identifying the scheme and correctly reproducing the known vulnerabilities in each — plus one clean target (a scheme with the relevant bugs fixed) showing all-pass with no false positives.

!!! failure "Forbidden"

    - Assuming the scheme instead of detecting it from evidence — a hardcoded "assume JWT" mode does not satisfy this capstone.
    - jwt_tool, an OAuth testing extension, or any existing auth-auditing tool doing the probing for you.
    - A false positive on the clean target — reporting a vulnerability that doesn't exist is graded as a failure, not a cautious miss.

!!! note "Norm"

    See §II.2, plus: detection, and each of the three probe modules, fully separable and independently testable; a shared HTTP/traffic-capture layer underneath all of them.

!!! tip "Bonus (§II.7)"

    SAML awareness module: detect a SAML-based SSO redirect (an `/saml`-shaped POST binding with a base64-encoded XML `SAMLResponse`) and, at minimum, decode and report the assertion's claims and validity window without necessarily forging a signature.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
auth_session_security/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live against your own running target, which the evaluator may reconfigure (a different weak secret, a different redirect_uri policy) immediately before the defense. The capstone is run against a target the evaluator chooses from your three plus the clean control, live, with no advance notice of which one.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — sessionstore0

**Defense questions**

1. Show me the session ID before and after login — prove rotation actually happens, live.
2. What's your session ID's entropy in bits, and what does that mean for brute-force feasibility against your idle timeout window?
3. Walk through what "logout" actually deletes in your store, and what a stolen pre-logout session ID could still do if you got this wrong.
4. Why is a stateful session fundamentally revocable in a way a bare JWT is not — tie this to Exercise 01.

### A.1 — jwtbreak0

**Defense questions**

1. Forge an `alg:none` token live, right now, by hand — no saved script.
2. Walk through exactly why signing with the RS256 public key as an HMAC secret produces a signature the server's (buggy) verification code accepts.
3. What is the actual fix for algorithm confusion — not "don't use RS256," but what should the verification call specify explicitly?
4. Why does a JWT with no revocation mechanism recreate the exact problem Exercise 00's server-side session store was built to solve?
5. Show your offline secret-cracking approach for the weak-HS256 token — what made the secret crackable, and how would you recognize that risk in a code review without cracking it first?

### A.2 — oauthflow0

**Defense questions**

1. Walk me through the full flow live, from the authorization request to the protected resource call, narrating every parameter.
2. Show your redirect_uri exploit — what exact validation logic would have prevented it, and why is prefix-matching still not enough?
3. Show your state-parameter CSRF — trace exactly how the victim ends up authenticated as the attacker, step by step.
4. Why is the implicit grant considered deprecated/dangerous compared to authorization-code-with-PKCE for a browser-based app?
5. What does the access token actually prove to the resource server, and what does it not prove (compare to what a session ID proves in Exercise 00)?

### A.3 — Capstone: authfingerprint

**Defense questions**

1. Point this at a target live and narrate the scheme-detection logic as it runs — what specific evidence tipped it one way or the other?
2. Run the JWT probe module against your Exercise 01 target live — walk through the RS256→HS256 attempt step by step.
3. Show me the clean-target run — why does it correctly report no vulnerabilities, and what specifically was fixed that your probes now correctly fail against?
4. What would your tool report on a target using session cookies for the main app but an OAuth redirect for a "login with Google" button — does it handle a target with two schemes present?
5. Why does detecting the scheme wrong lead directly to false negatives, not just wasted time — give a concrete example.

**Test / edge cases**

- [ ] A JWT stored in a cookie rather than an Authorization header: still correctly detected as JWT scheme, not misclassified as opaque session.
- [ ] A session cookie that happens to be base64-looking but is actually opaque server-side state: not misclassified as a JWT.
- [ ] An OAuth flow using PKCE: redirect_uri probe correctly reports that code interception alone is insufficient without the code_verifier, rather than falsely flagging it as vulnerable.
- [ ] A JWT with a valid `exp` that has already passed: correctly reported as expired, not flagged as a missing-exp vulnerability.
- [ ] A target with no discoverable public key/JWKS endpoint: RS256→HS256 probe explicitly reported as "not attempted, key material unavailable," never silently skipped without a note.
- [ ] Replaying an OAuth authorization code a second time: correctly expected and reported as rejected on a properly implemented target.
- [ ] A completely unrecognized auth scheme (e.g. HTTP Basic auth): reported as "unclassified — no probe set available," not force-fit into one of the three categories.
