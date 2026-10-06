---
title: "The Subject"
description: "The closing Stage 2 subject, and the one hardest to find with any scanner: bugs that exist only in the gap between two requests arriving close together, o…"
---
# Race Conditions and Business Logic Abuse: The Subject

*Subject 7 of 7 — Hands-On Web Security + Code Review · Version 1.0 — September 2026*

> The closing Stage 2 subject, and the one hardest to find with any scanner: bugs that exist only in the gap between two requests arriving close together, or in a workflow an attacker can reorder, skip a step of, or repeat — nothing here is a malformed payload, every request is individually well-formed.

## Chapter 00 — Foreword

> *A race condition isn't an attacker breaking your code. It's an attacker arriving at the one moment your code assumed no one else would.*

Every vulnerability class before this one had a payload — a string, a header, a crafted object — that a scanner could plausibly generate and a WAF could plausibly block. Race conditions and business-logic abuse have neither. The requests are perfectly valid; the vulnerability is in the sequencing and the assumptions, which is exactly why these bugs survive in mature, well-tested applications long after the "easy" classes have been scanned away, and why they command outsized bug bounty payouts.

## Chapter I — Introduction

You will exploit a classic TOCTOU race condition to redeem a limited-use discount code more than once through concurrent requests, abuse a multi-step checkout/workflow by skipping or reordering steps to reach a state the application never validated directly, and exploit a single-use-token race (the same coupon-redemption idea applied to password reset or email verification, where winning the race has account-takeover consequences instead of financial ones). The capstone builds a concurrency-fuzzing harness that finds race windows automatically.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of exploitability or of a fix working must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation targets DVWA, Juice Shop, WebGoat, PortSwigger Academy labs, HackTheBox/lab machines, or an application you wrote — never a third party without written authorization.

## Chapter III — Mandatory Part

### Exercise 00 — couponrace0

- **Turn-in dir:** race_conditions_business_logic/ex00/
- **Files:** vuln_app.py, EXPLOIT.md, evidence/
- **Allowed:** Python (threading/asyncio for concurrent requests), Burp's "Send group in parallel"
- **Forbidden:** any prebuilt race-condition exploitation tool

**Description.** A deliberately vulnerable single-use discount-code redemption endpoint, exploited via a classic TOCTOU (time-of-check-to-time-of-use) race: fire many redemption requests for the same code at once and redeem it far more than once.

!!! success "Mandatory"

    - A vulnerable endpoint implementing "check if code is unused, then mark it used, then apply the discount" as separate, non-atomic steps (e.g. a read-then-write pattern with no locking/transaction) — the deliberate, realistic bug (this exact pattern is extremely common in real code).
    - Fire a genuinely concurrent burst of requests (not sequential-but-fast — actual simultaneous dispatch, using threading/asyncio or Burp's parallel-send feature) redeeming the same single-use code, and demonstrate the code being successfully applied more than once, with the exact count of successful redemptions captured as evidence.
    - A written explanation of the race window precisely: between the "check" and the "use" steps, multiple requests can all pass the check before any of them completes the use step — with your own request timing/ordering evidence (not just the final "it redeemed twice" result) showing the interleaving actually happened.
    - A demonstration that the race becomes measurably harder to win (lower success rate) as request concurrency decreases, and easier as it increases — proving you understand the race's mechanics quantitatively, not just qualitatively.
    - The correct fix applied and verified: make the check-and-use atomic (a database transaction with appropriate isolation level, or a single atomic `UPDATE ... WHERE used=false` statement whose affected-row-count tells you definitively whether you won the race), with your concurrent-burst attack re-run and shown succeeding only once no matter the concurrency level.

!!! failure "Forbidden"

    - Any prebuilt race-condition tool.
    - A "concurrent" attack that's actually sequential requests fired quickly — genuine simultaneous dispatch is required and must be evidenced.
    - A fix that just adds a delay/sleep instead of actual atomicity — this doesn't fix the race, it only narrows the window.

!!! note "Norm"

    See §II.2, plus: the vulnerable check-then-use logic and the concurrent-request dispatcher each isolated.

!!! tip "Bonus"

    Exploit the same race via HTTP/2 request multiplexing (single connection, multiplexed streams) instead of multiple TCP connections, and note any difference in reliability.

### Exercise 01 — workflowbypass0

- **Turn-in dir:** race_conditions_business_logic/ex01/
- **Files:** vuln_app.py, EXPLOIT.md, evidence/
- **Allowed:** Burp, a multi-step workflow app you build (e.g. checkout: cart → shipping → payment → confirm)
- **Forbidden:** none beyond the global list

**Description.** A multi-step business workflow (e.g. a checkout process) where server-side state is only checked at the final step, exploited by skipping or reordering steps to reach a favorable end state the application never actually validated the path to.

!!! success "Mandatory"

    - A vulnerable multi-step workflow (e.g. cart → apply-discount → shipping-address → payment → confirm) where each step is its own endpoint, and the final confirm step trusts client-supplied state (e.g. a total price passed from the client) rather than recomputing it server-side from the actual cart/discount/shipping state.
    - A step-skipping exploit: call the confirm endpoint directly, skipping the payment step entirely, and demonstrate the order completing without payment ever having been processed.
    - A parameter-tampering-across-steps exploit: manipulate a value passed between steps (e.g. the price or an item quantity) that the final step trusts instead of recomputing, and demonstrate an order completing at an attacker-favorable price.
    - A step-repetition exploit: replay an early step (e.g. "apply discount") multiple times to see whether the discount stacks when it shouldn't (e.g. applying a 10%-off code three times for 30% off, or applying a single-use code across multiple orders because the workflow never marked it consumed at the right point).
    - The correct fix applied and verified: the server recomputes and re-validates all critical state (price, discount validity, item availability) at the final confirm step from its own source of truth, ignoring client-supplied values for anything security/financially relevant — with all three exploits re-run and shown failing.

!!! failure "Forbidden"

    - A workflow where the final step already recomputes everything server-side from the start — the vulnerability (trusting client state at the final step) must be real and demonstrated first.
    - Claiming a bypass without showing the actual completed end state (e.g. a confirmed order) as evidence, not just an unusual intermediate response.

!!! note "Norm"

    See §II.2, plus: each workflow step as its own clearly-labeled endpoint/function, so the eventual fix (recompute at the end) is a clean, auditable change.

!!! tip "Bonus"

    Combine this with Exercise 00: a workflow-bypass exploit that also races the discount-code redemption step for a compounded price manipulation.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** the genuine-concurrency dispatch mechanics and statistical race-detection reasoning from Exercise 00 (the same underlying skill as Applied Cryptographic Attacks' timing statistics — deciding whether an observed outcome distribution is consistent with "no race" or indicates a real window — but applied to concurrency outcomes instead of timing measurements), plus the business-logic-state awareness from Exercise 01 (a race-fuzzer that fires bursts at random endpoints with no understanding of which ones represent a limited/single-use resource will waste enormous effort on endpoints that can't meaningfully race). Someone who can fire concurrent requests but doesn't know which endpoints are worth targeting produces noise; someone who understands business logic but can't reliably achieve true concurrent dispatch never actually triggers the race window to observe it.

### Capstone — racefuzz

- **Turn-in dir:** race_conditions_business_logic/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A concurrency-fuzzing harness: given a set of candidate endpoints (especially ones involving limited resources — codes, tokens, inventory counts, single-use actions), automatically fires calibrated concurrent bursts at each and statistically detects race-condition windows by comparing observed outcomes (e.g. redemption count) against the expected single-winner outcome — turning the manual "fire a burst and count" technique from Exercise 00 into a repeatable scanner.

!!! success "Mandatory"

    - Candidate identification: given a list of endpoints (from a captured HAR/spec, reusing your API Authorization capstone's spec-ingestion approach if convenient), flags likely race-condition candidates by heuristic — endpoints whose naming/behavior suggests a limited resource or single-use action (redeem, claim, apply, use-once, transfer, withdraw) — rather than blindly firing bursts at every endpoint.
    - Calibrated concurrent dispatch: for each candidate, fires a genuinely concurrent burst (reusing Exercise 00's dispatch mechanics) at multiple concurrency levels (e.g. 5, 20, 50 simultaneous requests), recording the outcome distribution at each level.
    - Statistical race detection: compares the observed "successful" outcome count against the expected count under a no-race assumption (normally 1, for a single-use resource) at each concurrency level, and reports a race-condition finding only when the deviation is consistent and reproducible across multiple runs — not a one-off fluke — with the actual run-to-run data shown as evidence.
    - A confirmation replay: for every detected race, re-runs the exact same burst configuration at least 3 additional times and reports the reproduction rate, since race-condition findings in a real report need reliability data, not a single lucky hit.
    - One consolidated report: candidate endpoints tested, concurrency levels used, outcome distributions, and confirmed findings with reproduction rates and suggested fix pattern (atomic check-and-use, matching Exercise 00's fix).
    - Demonstrated end to end against your Exercise 00 vulnerable and fixed coupon endpoints, correctly detecting the race in the vulnerable version with a high reproduction rate and correctly reporting zero race findings (single successful redemption every time) against the fixed version across repeated runs.

!!! failure "Forbidden"

    - Any existing race-condition testing tool doing the detection for you.
    - Firing bursts at every endpoint indiscriminately with no candidate-prioritization heuristic — wastes an engagement's time budget and this is graded against.
    - Reporting a race-condition finding from a single run with no reproduction-rate evidence.

!!! note "Norm"

    See §II.2, plus: candidate-identification, concurrent-dispatch, and statistical-detection each in their own module, sharing one underlying HTTP-burst-firing layer.

!!! tip "Bonus (§II.7)"

    Extend candidate identification to also flag Exercise 01-style multi-step workflows (a sequence of related endpoints) as candidates for step-skipping/reordering testing, in addition to single-endpoint race testing.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
race_conditions_business_logic/
├── ex00/
├── ex01/
└── capstone/
```

Each exercise is defended live, with the concurrent-burst evidence reproduced on demand — a "trust me, it raced once" is not acceptable evidence. The capstone is run live against a target set the evaluator selects, including at least one repeated run during the defense itself to demonstrate the reproduction-rate discipline in real time.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — couponrace0

**Defense questions**

1. Run the concurrent burst live and show the redemption count exceeding one.
2. Explain the exact non-atomic check-then-use pattern and why a database transaction with the right isolation level (or an atomic conditional update) closes it completely.
3. Why does a `time.sleep()`-based "fix" not actually solve this, even if it makes the race much harder to win in practice?
4. Show your concurrency-vs-success-rate data and explain what it demonstrates about the race window's actual width.

### A.1 — workflowbypass0

**Defense questions**

1. Walk through all three exploits live against the vulnerable workflow, then show all three failing against the fixed version.
2. Why does trusting client-supplied state at the final step recreate exactly the mistake IDOR/broken-access-control findings make, just applied to workflow state instead of object ownership?
3. What's the general principle for multi-step workflows that this fix embodies — "never trust the client for anything the server can independently derive"?
4. Give a real-world example (outside your own app) where you'd expect this exact bug class to show up.

### A.2 — Capstone: racefuzz

**Defense questions**

1. Run this against your Exercise 00 vulnerable endpoint live, across multiple concurrency levels, and narrate the outcome distribution as it's gathered.
2. Run it against the fixed endpoint and show the reproduction-rate evidence supporting a "not vulnerable" conclusion.
3. Walk through your candidate-identification heuristic — what would it flag, and what would it correctly skip, from a list of ten made-up endpoint names?
4. Why does reproduction-rate matter for a race-condition finding specifically, more than it did for, say, a straightforward IDOR finding?
5. What's the relationship between concurrency level and detection reliability in your own data — does higher concurrency always mean a clearer signal?

**Test / edge cases**

- [ ] A resource that's meant to be usable exactly N times (not strictly 1), e.g. "redeem up to 3 times": detection logic correctly compares against the expected-N outcome, not a hardcoded expectation of exactly 1.
- [ ] A candidate endpoint that turns out to already be correctly atomic: repeated runs consistently show single-winner outcomes, and the tool correctly does not report a finding despite the endpoint matching the naming heuristic.
- [ ] Network-level request reordering/jitter causing an inconsistent single run: the multi-run reproduction-rate requirement specifically guards against reporting this as a false finding.
- [ ] A race window so narrow it only triggers at very high concurrency levels your default configuration doesn't reach: documented as a known limitation with a configurable concurrency ceiling, rather than a silent false negative presented as a clean result.
- [ ] Two different candidate endpoints that share the same underlying resource (e.g. one to "preview" and one to "apply" a coupon): tool's handling of this relationship (tested independently, or flagged as related) is documented.
