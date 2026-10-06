---
title: "The Subject"
description: "Not implementing your own crypto — using real primitives correctly, and knowing exactly where a system's security actually lives: not in the algorithm nam…"
---
# Cryptography Fundamentals for AppSec: The Subject

*Subject 2 of 7 — Security Fundamentals · Version 1.0 — September 2026*

> Not implementing your own crypto — using real primitives correctly, and knowing exactly where a system's security actually lives: not in the algorithm name, but in key management, mode of operation, and the trust chain that tells you whose key you're even looking at.

## Chapter 00 — Foreword

> *AES-256" tells you almost nothing about whether a system is secure. The mode, the key management, and the seventeen ways a correct algorithm gets used incorrectly are where the real system lives.*

AppSec engineers are not cryptographers, and this subject does not pretend otherwise — you will use vetted libraries throughout, never hand-roll a cipher. What you need is the ability to read a system's use of crypto and know immediately whether it's sound: is this mode authenticated, is this hash used for the right purpose, does this PKI chain actually terminate somewhere trustworthy. That reading ability is the actual skill.

## Chapter I — Introduction

You will implement correct symmetric encryption (authenticated, with correct nonce handling) and observe what happens when each safeguard is removed one at a time, build a password-hashing comparison demonstrating why fast hashes are wrong for passwords, and walk a full X.509 certificate chain by hand extending your TLS work from Networking Depth into signature verification specifically. The capstone is a static crypto-usage auditor that scans source code for exactly the misuse patterns you'll have spent the whole subject learning to recognize.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of the form "this is exploitable" or "this fix works" must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation in this subject targets DVWA, Juice Shop, WebGoat, or an application you wrote — running locally or on a VPS you own. Never a third party without written authorization.

**II.6** **No hand-rolled primitives.** Every cipher, hash, and signature operation in this subject uses a vetted library (`cryptography`, `PyNaCl`, or your language's standard crypto module). You are studying correct *usage*, never implementing AES or SHA yourself.

## Chapter III — Mandatory Part

### Exercise 00 — aeadmatters

- **Turn-in dir:** crypto_fundamentals/ex00/
- **Files:** aeadmatters.py, REPORT.md, evidence/
- **Allowed:** python cryptography library
- **Forbidden:** any hand-rolled cipher implementation

**Description.** A file-encryption tool built correctly first (AES-GCM, random nonce per message, authenticated), then deliberately broken one safeguard at a time — nonce reuse, no authentication tag check, ECB mode — with each break demonstrated as a real, working attack, not just described.

!!! success "Mandatory"

    - Correct baseline: AES-256-GCM with a freshly random 96-bit nonce per encryption, the auth tag verified on decrypt, key derived from a passphrase via a proper KDF (e.g. Scrypt/Argon2, not a bare hash).
    - Nonce-reuse attack: encrypt two different plaintexts under the same key and the same (reused) nonce, and demonstrate recovering the XOR of the two plaintexts from the two ciphertexts — the textbook stream-cipher-keystream-reuse break, executed for real against your own output, not described in the abstract.
    - Missing-authentication attack: given a mode without a tag check (or GCM with tag verification deliberately skipped), demonstrate a bit-flipping attack — modify specific ciphertext bytes and show a predictable, attacker-chosen change appears in the decrypted plaintext with no error raised.
    - ECB-mode demonstration: encrypt an image or another block-structured input under ECB and ordinary CBC/GCM side by side, and show the ECB output still visibly reveals structure ("the ECB penguin") while CBC/GCM does not.
    - A written summary table: attack → what safeguard's absence enabled it → what the correct implementation does differently.

!!! failure "Forbidden"

    - Implementing AES, GCM, or any primitive yourself — use the library's tested implementation throughout.
    - A "correct baseline" that reuses a nonce across runs due to a seeding bug — verified by explicitly checking nonce uniqueness across N encryptions.
    - Deriving the key directly from a passphrase via a bare hash instead of a proper password-based KDF.

!!! note "Norm"

    See §II.2, plus: key derivation, encryption, decryption/verification, and each attack demonstration in their own function.

!!! tip "Bonus"

    Demonstrate a padding-oracle-style attack against a CBC-mode implementation with verbose padding-error responses (a preview of Applied Cryptographic Attacks).

### Exercise 01 — hashpurpose0

- **Turn-in dir:** crypto_fundamentals/ex01/
- **Files:** hashpurpose0.py, REPORT.md
- **Allowed:** hashlib, bcrypt/argon2 library
- **Forbidden:** none beyond the global list

**Description.** A password-storage comparison tool that hashes the same wordlist under a fast general-purpose hash (SHA-256) versus a purpose-built password hash (bcrypt/Argon2), measures and demonstrates the real-world cracking-speed gap, and produces a written explanation of exactly why "hashing" is not one undifferentiated concept.

!!! success "Mandatory"

    - Hash a shared wordlist of at least 5,000 candidate passwords under raw SHA-256 (with a per-user salt) and separately under bcrypt/Argon2 (correctly configured cost parameters, justified in writing).
    - Measure and report actual hashing throughput (hashes/second on your hardware) for both, and extrapolate to realistic offline cracking time for a leaked database of, say, 10,000 SHA-256 hashes versus 10,000 bcrypt/Argon2 hashes at that measured rate.
    - Demonstrate cracking a deliberately weak password from each hash set using a dictionary attack you implement (not a prebuilt cracker), and show the wall-clock time difference directly, not just the extrapolated math.
    - A written explanation distinguishing three purposes commonly (and wrongly) conflated under "hashing": general-purpose integrity hashing (fast is fine, e.g. checking a file wasn't corrupted), cryptographic hashing for signatures/HMAC (fast, but must be collision- and preimage-resistant), and password hashing (must be deliberately slow and memory-hard) — with a concrete real-world consequence of using the wrong one for each purpose.
    - A demonstration of salting's specific benefit: precompute a rainbow-table-style lookup for a small unsalted hash set, then show the same lookup fails against a salted set — real precomputed tables, not just an assertion.

!!! failure "Forbidden"

    - A prebuilt password cracker (John/Hashcat) as your cracking engine — build your own dictionary-attack loop; comparing your result against Hashcat afterward is fine.
    - Configuring bcrypt/Argon2 with cost parameters so low they defeat the point of the comparison, without justifying the choice.
    - Conflating "hashing" as one undifferentiated concept anywhere in your written explanation.

!!! note "Norm"

    See §II.2, plus: hashing, throughput measurement, dictionary-attack, and rainbow-table-demo each isolated.

!!! tip "Bonus"

    Demonstrate a real-world consequence of hash-length-extension on a naive `SHA256(secret || message)` MAC construction, previewing why HMAC exists (full exploitation is Applied Cryptographic Attacks' subject).

### Exercise 02 — chaininspect

- **Turn-in dir:** crypto_fundamentals/ex02/
- **Files:** chaininspect.py, README.md
- **Allowed:** cryptography library (x509 module), ssl for connection setup
- **Forbidden:** reusing tlsinspect.py verbatim from Networking Depth — this exercise goes deeper into signature verification specifically

**Description.** Extends the TLS chain work from Networking Depth into full manual signature verification: for a real certificate chain, verify each certificate's signature against its issuer's public key using raw cryptographic operations, and demonstrate what breaks when a chain doesn't actually terminate in a trusted root.

!!! success "Mandatory"

    - Retrieve a real certificate chain (leaf, intermediate(s), root) for a target you choose, and for each non-root certificate, extract the issuer's public key and verify the certificate's signature over its own TBSCertificate bytes using the correct algorithm (RSA-PSS/PKCS1v15 or ECDSA depending on the cert) — a genuine signature-verification call, not a bundled "is this valid" boolean from a higher-level API.
    - Demonstrate the chain terminating in a certificate present in a real trust store (e.g. the system CA bundle), and explain in writing what "trusted root" actually means operationally — a root CA's certificate is self-signed, so its own "signature verification" only proves internal consistency, and trust is actually a policy decision (is this root in the store you've chosen to trust) not a cryptographic one.
    - Construct and verify a chain that does *not* terminate in a trusted root (e.g. a self-signed leaf, or a real intermediate with a fabricated/self-signed replacement for the root), and show your verification logic correctly rejecting it — with the exact point of failure identified (signature mismatch vs. untrusted anchor).
    - A written explanation of the asymmetric-crypto mechanics underneath this: why the issuer signing with their private key and everyone verifying with the public key is what makes forging a certificate infeasible without the issuer's private key, tied back to RSA/ECDSA fundamentals.
    - A demonstration of certificate pinning's specific benefit: show a scenario (simulated, e.g. a MITM proxy you run against your own test client) where a normally-valid-but-substituted certificate is accepted by standard chain validation but rejected once pinning to the expected public key/certificate is added.

!!! failure "Forbidden"

    - Calling a single library "verify chain" function and treating its boolean result as your own verification logic.
    - Skipping intermediate certificates and only verifying the leaf against the root directly.
    - Asserting the broken-chain case is rejected without showing the specific verification step that fails.

!!! note "Norm"

    See §II.2, plus: chain retrieval, per-certificate signature verification, trust-anchor checking, and the pinning demo each in their own function.

!!! tip "Bonus"

    Certificate Transparency: fetch and display the CT log inclusion for a real certificate, and explain what CT specifically defends against (mis-issuance detection) that chain validation alone does not.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** every failure mode from all three exercises simultaneously, recognized from source code rather than from a live attack you already know is there — ECB/nonce-reuse patterns from Exercise 00, password-hashing misuse from Exercise 01, and disabled/incomplete certificate validation from Exercise 02, plus enough real understanding of each primitive's correct use to avoid flooding a report with false positives on code that is actually fine. A pattern-matcher with no underlying model of \*why\* each pattern is dangerous cannot tell "AES.MODE_ECB used for a non-repeating single block" (low risk) from "AES.MODE_ECB used to encrypt a multi-block image" (textbook broken) — this capstone has to make that distinction.

### Capstone — cryptoreview

- **Turn-in dir:** crypto_fundamentals/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A static analysis tool that scans a codebase for the crypto-misuse patterns this subject covers — ECB mode, hardcoded keys/IVs, fast hashes used for passwords, missing authentication, weak/no salt, disabled certificate verification — and produces a reviewer-grade report with the exact line, the specific risk, and the correct fix.

!!! success "Mandatory"

    - Static rule for symmetric-cipher misuse: flags ECB mode usage, flags any hardcoded IV/nonce literal in source, and flags any cipher-mode usage without a paired authentication mechanism (bare CBC/CTR with no HMAC and no AEAD mode) — using an AST-based or robust regex-based scanner across at least Python and one other language (e.g. JavaScript or Java) of your choice.
    - Static rule for password-hashing misuse: flags direct use of MD5/SHA-1/SHA-256/SHA-512 where the surrounding context (variable/field names like `password`, `passwd`, function names like `hash_password`) indicates password storage, and confirms — rather than flags as clean — correct use of bcrypt/Argon2/scrypt/PBKDF2.
    - Static rule for hardcoded secrets: flags hardcoded API keys, encryption keys, and JWT signing secrets assigned as string literals in source (building on and reusable from a simple entropy/pattern heuristic, not just a fixed keyword list).
    - Static rule for TLS/certificate-validation bypass: flags `verify=False`/`CERT_NONE`/equivalent disabled-verification patterns across your target languages' common HTTP/TLS libraries.
    - Every finding reported with file, line, the exact risky code, a plain-language explanation of the specific failure mode (not a generic "insecure crypto" message), and a concrete suggested fix.
    - Demonstrated against a test corpus of at least 15 deliberately-planted findings across the four rule categories plus at least 10 deliberately-clean examples of correct usage (e.g. properly-configured AES-GCM, properly-used bcrypt, a legitimate non-password SHA-256 integrity check) — and achieves zero false positives on the clean set, with every planted finding caught.

!!! failure "Forbidden"

    - Semgrep, Bandit, or any existing SAST tool doing the detection for you — you are building the rule logic yourself (a preview of what Stage 3's SAST Engineering subject formalizes).
    - A keyword-only scanner that flags every occurrence of "MD5" regardless of context, producing false positives on legitimate non-password integrity uses.
    - Any false positive on the clean-code test set — an AppSec tool that cries wolf gets disabled by the engineering team it's meant to help, and this capstone is graded on that standard.

!!! note "Norm"

    See §II.2, plus: one rule module per finding category with a shared file-walking/AST-parsing layer; each rule independently testable against its own fixture files.

!!! tip "Bonus (§II.7)"

    A fifth rule detecting insufficiently random key/token generation (e.g. Python's `random` module used for a security-sensitive token instead of `secrets`).

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
crypto_fundamentals/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live with your own captures reproduced on demand. For the capstone, the evaluator supplies a modified corpus (new planted findings, new clean examples) immediately before the defense and expects the same zero-false-positive, full-catch standard.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — aeadmatters

**Defense questions**

1. Show your nonce-reuse attack live — derive the XOR-of-plaintexts result and explain exactly why stream-cipher-style constructions make this possible.
2. Why does GCM's authentication tag specifically prevent the bit-flipping attack that a bare CTR/CBC-without-HMAC construction would not?
3. What in the ECB output makes structure visible, at the byte level — why does one identical plaintext block always produce the same ciphertext block?
4. Why is Argon2/Scrypt correct for password-based key derivation where a single SHA-256 call is wrong — tie this forward to Cryptography's "password hashing" distinction from general-purpose hashing.

### A.1 — hashpurpose0

**Defense questions**

1. Show your measured hashes/second for both algorithms live and walk through the extrapolated cracking-time math for a real breach scenario.
2. Why is "slow" a security property for password hashing but a liability everywhere else you use hashing?
3. What does Argon2's memory-hardness specifically defend against that a purely CPU-slow hash does not?
4. Show your salted-vs-unsalted rainbow-table demo — why does a unique salt per user defeat a precomputed table even if the table is enormous?

### A.2 — chaininspect

**Defense questions**

1. Walk me through verifying one intermediate certificate's signature, live, byte-level, against its issuer's public key.
2. Why is a self-signed root's "valid signature" not actually proof of trustworthiness — what makes a root trustworthy, if not cryptography?
3. Show your rejected-chain case — exactly which check failed, and how does your code distinguish "signature invalid" from "signer not trusted"?
4. Explain your pinning demo's MITM scenario — what would a real attacker need to pull this off against a non-pinned client, and why does pinning close it?

### A.3 — Capstone: cryptoreview

**Defense questions**

1. Run this against a codebase I hand you live — walk through the findings as they come out.
2. Show me one of your clean-code fixtures and explain exactly what makes your scanner correctly recognize it as safe rather than flagging the mere presence of "SHA256" or "AES".
3. Why does distinguishing password-hashing context from general-purpose hashing context require more than a keyword match — what did you actually check?
4. What would a real false positive on a large real-world codebase look like for your ECB-detection rule, and how would you tune it down without missing real cases?
5. Why is this capstone specifically about \*recognizing\* the failure modes from source rather than exploiting them live — what's the practical AppSec-engineering value of that shift?

**Test / edge cases**

- [ ] ECB mode used deliberately and safely for a single, non-repeating 16-byte block (rare but real): not flagged, or flagged at clearly lower severity with the reasoning shown.
- [ ] A hardcoded IV that is actually a public, non-secret constant used correctly in a context where IV secrecy isn't the security property (documented exception): reviewer can see why it was or wasn't flagged.
- [ ] bcrypt/Argon2 used with a dangerously low cost factor: flagged as a separate, lower-severity finding — "correct primitive, weak configuration" — not treated identically to using no password hash at all.
- [ ] A hardcoded value that looks like a secret but is a public constant (e.g. a well-known test key from a library's own documentation): either correctly excluded or flagged with appropriately hedged confidence.
- [ ] Disabled certificate verification only in code clearly marked as a test/mock file: still flagged, since test-only code has a way of reaching production — but the report may note the file's apparent purpose.
- [ ] A file the scanner cannot parse (syntax error, unsupported language dialect): reported as unscanned, never silently skipped from the final report.
- [ ] The same finding appearing in a vendored/third-party directory versus first-party code: both reported, optionally distinguished, never silently excluded without the user opting into that.
