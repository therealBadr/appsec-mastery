---
title: "The Subject"
description: "Everything in this roadmap so far has been black-box: you found the bug by attacking it."
---
# Secure Code Review Methodology: The Subject

*Subject 5 of 7 — Hands-On Web Security + Code Review · Version 1.0 — September 2026*

> Everything in this roadmap so far has been black-box: you found the bug by attacking it. This subject flips the vantage point — given the source, find the same bug classes faster, more completely, and with a fix you can propose in the same pull request.

## Chapter 00 — Foreword

> *A black-box tester finds the vulnerabilities that happen to be reachable and happen to be tried. A code reviewer with a method finds the ones that are merely present.*

Every vulnerability class in Stage 1 and the rest of Stage 2 has a source-code signature, and a systematic reviewer doesn't wait for an exploit to prove a bug exists — they read data flow from every entry point (a request parameter, a file, a queue message) to every sink (a query, a shell call, a template render, an HTML write) and check whether anything sanitizes the path between them. This subject builds that method deliberately, then proves it against a real, sizable open-source codebase.

## Chapter I — Introduction

You will build a personal code-review checklist mapped to every vulnerability class this roadmap has covered so far, apply it manually to trace one specific data flow through a real multi-file application, then perform a full line-numbered audit of a deliberately vulnerable open-source app (WebGoat or Juice Shop's source). The capstone is a differential reviewer that re-audits a codebase after a diff and reports only what the diff introduced or fixed.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of exploitability or of a fix working must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation targets DVWA, Juice Shop, WebGoat, PortSwigger Academy labs, HackTheBox/lab machines, or an application you wrote — never a third party without written authorization.

## Chapter III — Mandatory Part

### Exercise 00 — reviewchecklist0

- **Turn-in dir:** secure_code_review/ex00/
- **Files:** CHECKLIST.md
- **Allowed:** your own accumulated knowledge from this roadmap
- **Forbidden:** copying a published checklist verbatim without adapting it in your own words

**Description.** A personal, source-mapped code-review checklist: for every vulnerability class covered in Stages 0-2 so far, the exact source-code pattern that indicates risk, in the language(s) you review most.

!!! success "Mandatory"

    - One entry per vulnerability class covered so far (at minimum: SQLi, command injection, XXE, SSRF, XSS, CSRF, insecure deserialization, SSTI, path traversal/LFI, broken access control/BOLA, mass assignment, weak crypto/hashing usage, hardcoded secrets, disabled TLS verification) — not copied from Cryptography Fundamentals' capstone rules wholesale, but written in your own words with your own example snippet per entry.
    - For each entry: the vulnerable pattern (a real code snippet you write, not lifted from a tutorial), the safe pattern it should be replaced with, and one sentence on how to distinguish a true positive from a false positive when you see the pattern in a real codebase (reusing the false-positive discipline from earlier capstones).
    - A "trust boundary" section: a written definition, in your own words, of what a trust boundary is in source-code terms (the exact line where data stops being "whatever the caller/environment provided" and starts being treated as safe), since every entry above is really a variant of "something crossed a trust boundary without being checked."
    - A prioritization scheme: given limited review time, which categories you'd check first in an unfamiliar codebase and why (e.g. authentication/authorization code first, since a flaw there undermines every other control).

!!! failure "Forbidden"

    - Copy-pasting the OWASP Code Review Guide or any published checklist without rewriting it in your own words and your own examples.
    - A checklist entry with no concrete code example.

!!! note "Norm"

    One consistent entry format applied to every vulnerability class, so the checklist is actually usable as a working tool, not a essay.

!!! tip "Bonus"

    A second checklist pass specific to a language/framework you haven't emphasized yet (e.g. Java/Spring or Node/Express) translating the same vulnerability classes into that ecosystem's idioms.

### Exercise 01 — dataflowtrace0

- **Turn-in dir:** secure_code_review/ex01/
- **Files:** TRACE.md
- **Allowed:** a real multi-file application (WebGoat, Juice Shop, or another open-source app of comparable size)
- **Forbidden:** an automated static analyzer as your primary method for this exercise — you are building the manual skill the capstone later automates

**Description.** A single, complete, hand-traced data flow through a real multi-file application: from the exact line where user input enters, through every function it passes through, to the exact sink where it's used — with every intermediate transformation and every missed (or present) sanitization step documented.

!!! success "Mandatory"

    - Select one real endpoint in a real application whose vulnerability status you do not already know going in, and trace its input from the HTTP-request-parsing entry point through every intervening function call to its eventual sink (a query, a file operation, a template render, a shell call, or an HTTP write) — every hop in the call chain documented with file and line number.
    - At each hop, explicitly note whether any transformation or check occurs (type coercion, validation, encoding, or none), and whether that check would actually stop a malicious payload for the sink type it eventually reaches.
    - A final verdict: vulnerable or not, with the reasoning laid out as the trace itself — the verdict should be a direct, visible consequence of the documented trace, not a separate assertion tacked onto the end.
    - If vulnerable: a working exploit proving the trace was right (closing the loop back to black-box confirmation — code review finds the candidate, exploitation proves it). If not vulnerable: a precise identification of exactly which hop's check is the one that stops it, and what would have to change for it to become vulnerable.
    - A written reflection: how long manual tracing took for this one flow, and what that implies about the scale problem real code review faces on a codebase with thousands of endpoints — setting up the motivation for this subject's capstone and for Stage 3's SAST subject.

!!! failure "Forbidden"

    - An automated static analyzer as the primary method — this exercise is specifically about the manual skill.
    - Picking a flow you already know the answer to from earlier black-box testing — the point is code review finding something new, or confirming absence with real rigor.
    - A verdict with no visible trace supporting it.

!!! note "Norm"

    TRACE.md structured as an ordered hop list (file:line → what happens → what's checked), ending in the verdict and evidence.

!!! tip "Bonus"

    Trace a second flow through the same application that turns out to have the opposite verdict from the first (one vulnerable, one safe), to demonstrate the method isn't biased toward finding (or not finding) bugs.

### Exercise 02 — fullaudit0

- **Turn-in dir:** secure_code_review/ex02/
- **Files:** AUDIT_REPORT.md
- **Allowed:** WebGoat or Juice Shop source, your Exercise 00 checklist
- **Forbidden:** an automated SAST tool as your primary finding source — cross-checking your manual findings against one afterward is encouraged, not required

**Description.** A full, line-numbered, checklist-driven manual audit of a real deliberately-vulnerable open-source application's source, producing a professional vulnerability report with every finding's exact location, root cause, and fix.

!!! success "Mandatory"

    - A systematic pass through the target application's source using your Exercise 00 checklist as the driving method, covering at minimum the application's authentication, authorization, and input-handling code (the highest-priority areas per your own prioritization scheme).
    - At least 8 distinct findings, each with: file and line number, the vulnerability class, a code-level root-cause explanation (why this specific code is wrong, not a generic description), a proposed fix as an actual code diff, and a severity rating with justification.
    - For at least 3 of the 8 findings, a working exploit confirming the manual finding was correct — reusing the black-box techniques from Stage 1/Stage 2 to close the loop, as in Exercise 01.
    - A findings summary table at the top of the report (severity-sorted) suitable for an engineering team's triage meeting, followed by the detailed per-finding sections.
    - A written note on any finding you suspected but could not confirm (either because exploitation was impractical in the time available or because the code path was ambiguous) — reported honestly as "suspected, unconfirmed" rather than omitted or overstated.

!!! failure "Forbidden"

    - An automated SAST tool as the primary source of findings for the mandatory part.
    - A finding with no file/line reference.
    - A proposed fix that isn't an actual code diff you could hand to a developer.

!!! note "Norm"

    AUDIT_REPORT.md follows the same professional report structure as Secure Coding and TLS Configuration's TLS audit and DVWA capstone — this is intentional, since a code-review report and a pentest report ultimately serve the same reader.

!!! tip "Bonus"

    Submit at least one of your findings as a real issue/pull request to the target project's public repository (if it is genuinely unreported and the project accepts external reports) — an authentic step toward the roadmap's "found and reported a real vulnerability in an open-source project" Stage 2/4 exit-gate criterion.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** the checklist patterns from Exercise 00, the hop-by-hop data-flow tracing discipline from Exercise 01 (a diff-aware reviewer still has to trace a changed line's data flow forward to its sink and backward to its source, even when the sink or source is outside the diff itself, in unchanged code), and the report structure and severity/confidence discipline from Exercise 02 — applied under the real-world constraint that a full-codebase audit doesn't scale to every pull request, which is exactly the scale problem Exercise 01's closing reflection was building toward.

### Capstone — diffreview

- **Turn-in dir:** secure_code_review/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A differential code reviewer: given a git diff (a pull request), applies your Exercise 00 checklist patterns specifically to the changed lines and their immediate data-flow neighborhood, reporting only what the diff newly introduces or newly fixes — the actual shape of code review inside a real engineering team, where nobody re-audits the whole codebase on every commit.

!!! success "Mandatory"

    - Given a git diff (a set of changed files with added/removed lines), for every added line, checks it against your Exercise 00 checklist patterns directly.
    - For every added line that touches a checklist pattern's sink or source, traces the data flow at least one hop forward and one hop backward into the *surrounding unchanged code* (not just the diff's own lines) to determine whether the change actually introduces or fixes a vulnerability, or is a no-op with respect to security — reusing Exercise 01's tracing method but scoped to start from the diff.
    - Classifies each flagged line as newly-introduced-risk, newly-fixed-risk (the diff removed a vulnerable pattern or added a missing check), or flagged-but-inconclusive-without-deeper-trace (explicitly, rather than guessing).
    - Produces a PR-review-style report: comments anchored to specific added lines (as a real PR review tool would), each with the same root-cause/fix/severity structure as Exercise 02's findings, kept short enough to actually be read in a PR review (a paragraph, not a full audit report per line).
    - Demonstrated against at least two real diffs you construct: one that introduces a genuine vulnerability from your checklist (e.g. a diff that changes a parameterized query back to string concatenation) and one that fixes one (the reverse), correctly classifying each — plus a third, security-irrelevant diff (e.g. a CSS/formatting change) correctly producing zero findings.

!!! failure "Forbidden"

    - A full-codebase re-scan disguised as "diff review" — the tool must demonstrably scope its analysis to the diff and its immediate data-flow neighborhood, not silently re-audit everything.
    - Any existing SAST/PR-review-bot product doing the analysis for you.
    - A false positive on the security-irrelevant diff.

!!! note "Norm"

    See §II.2, plus: diff-parsing, checklist-matching, neighborhood-tracing, and report-formatting each in their own module.

!!! tip "Bonus (§II.7)"

    GitHub Actions integration: the tool runs automatically on a pull request in a test repository and posts its findings as real PR review comments via the GitHub API.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
secure_code_review/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Exercises 00-02 are defended live with the source open in front of you, findings reproduced on demand. The capstone is run live against a diff the evaluator constructs on the spot from your Exercise 02 target application, and must classify it correctly with a visible trace, not a pattern-match guess.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — reviewchecklist0

**Defense questions**

1. Pick three entries at random — explain the vulnerable pattern, the safe pattern, and the false-positive discrimination, without your notes.
2. Defend your prioritization scheme — why review authentication code before, say, a logging utility?
3. What's your own definition of a trust boundary, in your own words, applied to a concrete example from this roadmap?
4. What would you add to this checklist that isn't on it yet, based on something you learned in this roadmap that surprised you?

### A.1 — dataflowtrace0

**Defense questions**

1. Walk the trace live, hop by hop, from the source file open in front of you.
2. At the hop where a check exists (or is missing), explain precisely why it would or wouldn't stop the specific attack class this sink is vulnerable to.
3. How confident are you in the verdict, and what would change your mind?
4. How long did this take you, and what does that tell you about doing this at the scale of a real codebase?

### A.2 — fullaudit0

**Defense questions**

1. Pick two findings at random and walk through the code, the root cause, and the fix, live, from the open source file.
2. Show me one of your three confirmed exploits working against the actual application.
3. Walk through your "suspected, unconfirmed" note — what would you need to do to resolve the ambiguity?
4. Defend your severity ratings for two findings — why is one higher than the other?

### A.3 — Capstone: diffreview

**Defense questions**

1. Run this against your vulnerability-introducing diff live and walk through how it traced beyond the diff's own lines to reach its conclusion.
2. Run it against your vulnerability-fixing diff and explain how it correctly recognized a fix rather than flagging the removed line as if it were still risky.
3. Run it against your irrelevant diff and confirm zero findings.
4. Why does diff-scoped review need to look at unchanged surrounding code at all — give a concrete example where ignoring it would cause a wrong classification.
5. How would this tool behave differently from — and better than — commenting on every line that merely matches a checklist pattern with no data-flow tracing at all?

**Test / edge cases**

- [ ] A diff that moves a vulnerable pattern from one file to another without changing its behavior (a refactor): correctly classified as neither newly-introduced nor newly-fixed risk, since the vulnerability existed before and after.
- [ ] A diff that changes a parameterized query's table name only (no security-relevant change): correctly produces no finding despite touching a "SQL" line.
- [ ] A diff where the fix is in a different file from the original vulnerable line (e.g. a shared validation helper is fixed, affecting call sites not in this diff): tool's scoping decision here (flag the helper's diff only, or attempt to also assess call sites) is documented and justified.
- [ ] A diff too large to trace every added line's full neighborhood in reasonable time: tool has a documented, sensible prioritization (e.g. auth/input-handling files first, matching Exercise 00's prioritization scheme) rather than silently truncating arbitrarily.
- [ ] A diff that adds a new checklist-pattern match but the surrounding trace shows the sink is entirely unreachable with attacker-controlled data (e.g. a hardcoded, non-user-controlled argument): correctly not flagged, avoiding a pattern-only false positive.
