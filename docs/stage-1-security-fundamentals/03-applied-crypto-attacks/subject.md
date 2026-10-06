---
title: "The Subject"
description: "Four attacks that show up repeatedly in real CVEs and bug bounty reports, executed for real against your own vulnerable targets: the padding oracle, hash-…"
---
# Applied Cryptographic Attacks: The Subject

*Subject 3 of 7 — Security Fundamentals · Version 1.0 — September 2026*

> Four attacks that show up repeatedly in real CVEs and bug bounty reports, executed for real against your own vulnerable targets: the padding oracle, hash-length-extension, a timing side-channel, and weak-RNG token prediction.

## Chapter 00 — Foreword

> *A cryptographic system doesn't fail because the math was wrong. It fails because the implementation answered a question — even a very quiet one, like "how long did that take?" — that it should never have answered at all.*

Cryptography Fundamentals taught you to recognize misuse in source code. This subject executes four of the most consequential misuse patterns as full attacks against targets you build, because recognizing "this looks risky" and actually extracting a plaintext or forging an authenticated message are different skills, and the second one is what makes the first one credible in a report.

## Chapter I — Introduction

You will decrypt a full CBC-mode ciphertext byte by byte using only a padding-error oracle, forge a valid MAC over an extended message without ever seeing the secret key via hash-length-extension, statistically extract a secret through response-timing differences, and predict session tokens generated from a weak PRNG seed. The capstone chains a timing side-channel into a full authentication bypass.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of the form "this is exploitable" or "this fix works" must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation in this subject targets DVWA, Juice Shop, WebGoat, or an application you wrote — running locally or on a VPS you own. Never a third party without written authorization.

**II.6** **No hand-rolled primitives.** As in Cryptography Fundamentals — you attack real, correctly-implemented-except-for-one-flaw targets using real library primitives; you never reimplement AES/SHA yourself.

## Chapter III — Mandatory Part

### Exercise 00 — paddingoracle0

- **Turn-in dir:** applied_crypto_attacks/ex00/
- **Files:** paddingoracle0.py, EXPLOIT.md, evidence/
- **Allowed:** requests/sockets against your own CBC+verbose-padding-error target
- **Forbidden:** PadBuster or any existing padding-oracle tool

**Description.** A full padding-oracle attack against a deliberately vulnerable CBC-mode endpoint that leaks padding-validity through distinguishable error responses — decrypting an entire ciphertext block by block without ever knowing the key.

!!! success "Mandatory"

    - A target endpoint (you build it) that decrypts an attacker-supplied CBC-mode ciphertext and returns a distinguishable response for "padding valid" versus "padding invalid" (an explicit error message, a different status code, or even just a timing difference — your primary implementation should use an explicit oracle, with timing as the bonus path).
    - Implement the byte-at-a-time padding-oracle algorithm yourself: manipulate the previous ciphertext block's bytes to produce each possible padding value, use the oracle's valid/invalid signal to recover one intermediate-state byte at a time, and XOR against the real previous-block ciphertext to recover plaintext — for a full multi-block ciphertext, not a single block toy case.
    - A written, precise explanation of *why* this works: what CBC decryption's XOR-with-previous-ciphertext-block structure has to do with the ability to manipulate plaintext bytes by manipulating ciphertext bytes, and why the oracle only needs to say yes/no about padding to leak the entire plaintext.
    - Demonstrate the attack fully recovering a multi-block secret (e.g. a session token or a short message) end to end, verified against the known plaintext you planted.
    - A written fix: what specifically closes this (authenticated encryption / constant-time, uniform error responses) and why "just make the error messages identical" is necessary but insufficient without also addressing timing.

!!! failure "Forbidden"

    - PadBuster or any existing padding-oracle exploitation tool.
    - A target with a real oracle that you happen to already know the plaintext for, with no actual byte-recovery algorithm implemented.
    - Claiming the attack works without showing full recovery of a plaintext you didn't already know going in (blind to your own exploit code, verified only against the planted secret afterward).

!!! note "Norm"

    See §II.2, plus: oracle-query, single-byte-recovery, and full-block/full-message orchestration each in their own function.

!!! tip "Bonus"

    Extend the same algorithm to also *forge* a valid ciphertext for an attacker-chosen plaintext (full CBC-mode plaintext-and-ciphertext control via padding oracle, not just decryption).

### Exercise 01 — lengthextend0

- **Turn-in dir:** applied_crypto_attacks/ex01/
- **Files:** lengthextend0.py, EXPLOIT.md
- **Allowed:** hashlib for the underlying hash only; you implement the extension logic
- **Forbidden:** hashpumpy or any existing length-extension tool as your core logic (comparing against it afterward is fine)

**Description.** A hash-length-extension attack against a naive `MAC = SHA256(secret || message)` authentication scheme: forge a valid MAC over an attacker-extended message without ever learning the secret, by exploiting the Merlin-Damgård construction directly.

!!! success "Mandatory"

    - A target (you build it) that authenticates messages using `SHA256(secret || message)` as a MAC, where `secret` is fixed and unknown to your attack code, and accepts a `(message, mac)` pair as valid only if the MAC matches.
    - Implement Merkle–Damgård length-extension yourself: given one valid `(message, mac)` pair and the secret's *length* (a realistic real-world assumption — often guessable or discoverable), compute the correct glue padding and derive a valid MAC for `message || glue_padding || attacker_suffix` for an attacker-chosen suffix — without ever learning the secret value itself.
    - A written, precise explanation of exactly why this works: SHA-256's internal state after processing `secret || message || padding` is a complete, resumable starting point for hashing further data, because the Merkle–Damgård construction has no distinct "finalization" step that scrambles the final state irreversibly.
    - Demonstrate a real consequence: the target application treats the extended message as authentic (e.g. a URL with `&admin=true` appended past the original authenticated message), and your forged MAC is accepted, granting the extended privilege.
    - A written fix: why `HMAC(secret, message)` (not `SHA256(secret || message)`) closes this specific attack, tying back to HMAC's actual construction (the nested inner/outer hash) rather than just asserting "HMAC is safer."

!!! failure "Forbidden"

    - hashpumpy or any existing length-extension library as your forging logic.
    - A target using HMAC correctly from the start — the vulnerable construction must be the naive `secret || message` concatenation.
    - Skipping the glue-padding derivation and hardcoding it for one specific secret length "because you already knew it."

!!! note "Norm"

    See §II.2, plus: MD-padding calculation, internal-state resumption, and forged-MAC construction each in their own function.

!!! tip "Bonus"

    Demonstrate the same attack against SHA-1 or MD5 for comparison and note which underlying property (shared by all Merkle–Damgård hashes) makes this attack independent of which specific hash function is used.

### Exercise 02 — timingleak0

- **Turn-in dir:** applied_crypto_attacks/ex02/
- **Files:** timingleak0.py, ANALYSIS.md, evidence/
- **Allowed:** requests/sockets, statistics module
- **Forbidden:** none beyond the global list

**Description.** A statistical timing side-channel attack that extracts a secret token character by character purely from measured response-time differences of a non-constant-time string comparison — proving the attack with real measurements and real statistics, not a theoretical description.

!!! success "Mandatory"

    - A target (you build it) that compares an attacker-supplied token against a secret using a naive, non-constant-time comparison (e.g. Python's `==` on strings, which short-circuits on the first mismatched byte) rather than `hmac.compare_digest` or equivalent.
    - Implement a character-by-character extraction: for each position, send enough requests with each candidate byte in that position (holding prior recovered bytes correct) to measure a statistically significant timing difference between a correct-so-far prefix and an incorrect one, using proper statistics (mean/median with enough samples to beat network jitter — not a single request per guess).
    - A written explanation of your statistical methodology: how many samples per guess, how you handled outliers/jitter, and what confidence threshold you used to accept a byte as correct before moving to the next position — with a plot or table of the actual timing distributions you measured.
    - Demonstrate full recovery of a secret token of realistic length (8+ characters) purely from timing, verified against the known planted value.
    - A demonstration that the same attack fails (or becomes statistically indistinguishable from noise within a reasonable request budget) against the same target once the comparison is switched to `hmac.compare_digest`, run head to head as a real before/after.

!!! failure "Forbidden"

    - Reporting success without the underlying timing-distribution evidence (raw measurements or a summary statistic table) in ANALYSIS.md.
    - A single-sample-per-guess implementation that "happens to work" once due to noise — the exercise requires demonstrating statistical rigor.
    - Running this against any target you do not control, on a network you do not control (local loopback or your own lab network only — real timing attacks are extremely sensitive to network jitter, and this must be reproducible).

!!! note "Norm"

    See §II.2, plus: measurement, statistical-comparison, and byte-recovery-orchestration each in their own function.

!!! tip "Bonus"

    Repeat the extraction over a simulated higher-jitter network path (e.g. artificial random delay injected server-side) and show how many more samples per guess were needed to still succeed.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** the statistical extraction methodology from Exercise 02 and the forgery mechanics from Exercises 00-01 (constructing a valid credential once you have the secret material), applied end to end against one coherent target rather than three separate toy demonstrations. A timing leak that only proves "I can tell characters apart statistically" is a research curiosity; chaining it into an actual forged, accepted request is what makes it a finding a report can rate as Critical rather than Informational — the gap between "theoretically exploitable" and "here is the authenticated request I should not have been able to make" is exactly what separates a real vulnerability report from a false-positive scanner alert.

### Capstone — timingbypass

- **Turn-in dir:** applied_crypto_attacks/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A full authentication-bypass chain: use the timing side-channel technique from Exercise 02 to extract a valid API key or session-signing secret from a target application byte by byte, then use that recovered secret to forge a valid authenticated request — proving a timing leak is not an academic curiosity but a direct path to full compromise.

!!! success "Mandatory"

    - A target application (you build it) protecting an admin action behind either an API-key comparison or a signed-token check, implemented with a non-constant-time comparison as the vulnerable point.
    - Full statistical timing extraction of the complete secret (API key or signing key), reusing and extending your Exercise 02 methodology, including a documented sample-size/confidence strategy and the full timing-distribution evidence for at least three recovered byte positions.
    - Using the fully recovered secret, construct a valid, accepted request to the protected admin action — either directly (recovered API key) or by using the recovered signing secret to forge a valid signature/MAC over an attacker-chosen payload (reusing Exercise 01's forgery mechanics if the target uses a MAC construction, or straightforward key reuse if it's a plain API key).
    - A complete, reproducible attack script that runs unattended from "no knowledge of the secret" to "successful forged admin request," with progress logged at each stage.
    - A written incident-style report: what was recovered, how, how long it took (wall-clock and request count), and — critically — the actual fix (constant-time comparison, and why timing-safe comparison is a specific, learnable code-review pattern rather than a vague "use better crypto" gesture).

!!! failure "Forbidden"

    - Skipping straight to using a pre-known secret for the forgery step — the secret must be genuinely recovered by your own timing attack in this run.
    - A "recovery" that is actually brute force unrelated to timing (e.g. guessing a short key by exhaustive search) — the exercise specifically requires the timing side-channel to be the extraction mechanism.
    - Claiming success without the full distribution evidence proving the extraction was statistically sound, not lucky.

!!! note "Norm"

    See §II.2, plus: extraction and forgery remain separable, independently-runnable stages with a clean handoff (recovered secret as a single artifact passed between them).

!!! tip "Bonus (§II.7)"

    Add a rate-limiter to the target and demonstrate/discuss how a realistic rate limit changes the attack's practical wall-clock feasibility, including any evasion or patience-based adaptation you attempt.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
applied_crypto_attacks/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live against your own reproducible target, re-run from a fresh process so timing and oracle behavior are not artifacts of a warmed-up cache from your development runs. The capstone's full chain is run live, unattended, start to finish, during the defense.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — paddingoracle0

**Defense questions**

1. Walk me through recovering one plaintext byte, live, narrating each padding-guess and what the oracle's response told you.
2. Why does this attack need zero knowledge of the encryption key at any point — what is it actually exploiting?
3. What happens to your attack if the error responses are made identical text but the invalid-padding path takes measurably longer to compute — is your implementation resilient to that, or is that explicitly out of scope for the mandatory part?
4. Why is switching to an AEAD mode (like GCM) a complete fix rather than a mitigation — what disappears from the attack surface entirely?

### A.1 — lengthextend0

**Defense questions**

1. Walk through your glue-padding calculation live for a specific secret length — derive it, don't recite it.
2. Explain, at the level of SHA-256's internal compression function, why resuming from a known digest is possible at all.
3. Why does HMAC's inner/outer double-hash structure specifically prevent this, when HMAC is still "just SHA-256 underneath"?
4. What real-world assumption does this attack depend on (secret length known or guessable) and how realistic is that assumption in practice — give a concrete scenario where an attacker would know or could brute-force-guess it.

### A.2 — timingleak0

**Defense questions**

1. Show me your raw timing measurements for one byte position — walk through how you decided which candidate was actually correct.
2. Why does Python's default `==` on strings leak timing information at all — what's happening at the byte-comparison level?
3. What does `hmac.compare_digest` do differently, mechanically, that defeats this?
4. Why is this attack dramatically harder over a real internet path than over loopback, and what does that imply about its practical exploitability against a real remote target versus a same-datacenter attacker?

### A.3 — Capstone: timingbypass

**Defense questions**

1. Run the full chain live, start to finish, narrating each stage.
2. Show me the timing-distribution evidence for the hardest-to-distinguish byte position you recovered — what made it hard, and how did you resolve the ambiguity?
3. Walk through exactly how the recovered secret becomes a forged, accepted request — what does the target actually check, and why does your forged value pass that check?
4. What single code change closes this entire chain, and why does it need to happen at the comparison, not anywhere else in the flow?
5. How would a rate limit change your approach, and is a rate limit alone a sufficient fix on its own?

**Test / edge cases**

- [ ] A byte position where two candidates produce statistically indistinguishable timing (a genuine tie within your measurement precision): your tool's behavior on this (more samples, flagged as ambiguous, or explicit failure) is documented and justified.
- [ ] Network jitter spike during extraction (simulated): does not silently corrupt a recovered byte — outlier handling is visible in your methodology.
- [ ] The forged request accepted but for the wrong recovered secret (an off-by-one in your extraction): your validation step catches this before declaring success, rather than reporting a false "compromise."
- [ ] Target restarts mid-extraction and secret rotates: extraction correctly fails/restarts rather than silently mixing partial data from two different secrets.
- [ ] A secret containing repeated/adjacent similar bytes: extraction still correctly distinguishes them, not just the "easy" high-timing-delta cases.
