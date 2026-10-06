---
title: "The Subject"
description: "You have been using Burp as a proxy for six subjects."
---
# Burp Suite Mastery and the PortSwigger Gauntlet: The Subject

*Subject 6 of 7 — Hands-On Web Security + Code Review · Version 1.0 — September 2026*

> You have been using Burp as a proxy for six subjects. This one makes you fluent in it as an instrument — Repeater, Intruder, match-and-replace, extensions, and Collaborator — while you complete every PortSwigger Web Security Academy lab, including the expert tier, the single highest-signal free credential this entire roadmap recognizes.

## Chapter 00 — Foreword

> *Treating Burp Suite as a magic box that finds bugs is the fastest way to stay a tool operator. Every button in it is a shortcut for something you already know how to do by hand — which is exactly what makes it worth learning properly.*

This subject has an unusual shape: it is partly a tools-mastery exercise and partly a completion gate. The roadmap is explicit that PortSwigger Web Security Academy is the single best free web-security resource in existence and treats full completion — including expert-tier labs — as non-negotiable. This subject builds real Burp fluency first (so the labs go faster and teach more) and then holds you to that completion bar.

## Chapter I — Introduction

You will rebuild a manual multi-step exploit (chosen from earlier subjects) entirely inside Burp using Repeater and Intruder's four attack types correctly matched to the right use case, write a Burp extension that automates a specific check from an earlier subject, and use Collaborator (or a self-hosted equivalent) for out-of-band confirmation the way your own OOB listeners did earlier — professionalized into the tool a real engagement actually uses. The capstone is completing PortSwigger Web Security Academy in full, tracked and proven.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline).** Functions do one thing and are named for what they do. No magic numbers. No block of code you cannot explain, unprompted, line by line, during defense.

**II.3** **Evidence, not assertions.** Every claim of exploitability or of a fix working must be backed by a reproducible request/response, log, or capture in your turn-in.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct.

**II.5** **Scope.** All exploitation targets DVWA, Juice Shop, WebGoat, PortSwigger Academy labs, HackTheBox/lab machines, or an application you wrote — never a third party without written authorization.

## Chapter III — Mandatory Part

### Exercise 00 — burpworkflow0

- **Turn-in dir:** burp_mastery_portswigger/ex00/
- **Files:** WORKFLOW.md, evidence/
- **Allowed:** Burp Suite Community or Professional
- **Forbidden:** none beyond the global list

**Description.** A complete re-execution of one earlier multi-step manual exploit (your choice — the padding oracle, the IDOR enumeration, or the OAuth state-parameter CSRF are all good candidates) entirely within Burp's workflow: Proxy capture, Repeater for manual iteration, and the correct Intruder attack type for the parts that benefit from automation.

!!! success "Mandatory"

    - Capture the full original request chain via Proxy, and use Repeater to manually replay and modify each step, demonstrating the tab-per-request workflow real practitioners use to keep multiple in-flight hypotheses straight.
    - Identify the specific part of your chosen exploit that benefits from Intruder (e.g. the ID-enumeration sweep for an IDOR, or the byte-recovery loop for a padding oracle) and correctly select and configure the matching attack type — Sniper for a single payload position swept through a wordlist, Cluster Bomb for multiple independent positions, Pitchfork for multiple positions advanced in lockstep from paired wordlists — with a written justification for why that specific type fits this specific exploit's shape (not "I used Sniper because it's the default").
    - Configure and use Intruder's response-grep/extraction feature to automatically pull out the specific piece of data your exploit needs from each response (e.g. extracting the padding-oracle's error indicator, or a specific field from an IDOR response) rather than manually reading every response.
    - Use match-and-replace rules to solve one recurring friction point in the exploit chain (e.g. automatically re-inserting a rotating CSRF token or session value on every outgoing request) and demonstrate the chain continuing to work unattended across several requests because of it.
    - A written comparison: what this Burp-driven version got you (speed, response-extraction automation) versus your original hand-rolled script version from the earlier subject, and what the hand-rolled version still teaches that clicking through Burp alone would not have.

!!! failure "Forbidden"

    - Using Intruder's default Sniper attack for a case that actually calls for a different attack type, with no justification.
    - A workflow that doesn't actually reproduce the original exploit's full impact (e.g. stopping at "found the right byte" without completing the chain).

!!! note "Norm"

    WORKFLOW.md documents the Burp configuration (attack type, payload positions, grep/extract rules, match-and-replace rules) precisely enough that someone could reproduce your setup from the document alone.

!!! tip "Bonus"

    Use Burp's session-handling rules to fully automate re-authentication mid-attack for a target whose session expires during a long Intruder run.

### Exercise 01 — burpextension0

- **Turn-in dir:** burp_mastery_portswigger/ex01/
- **Files:** extension/, README.md, evidence/
- **Allowed:** Burp's Montoya/legacy extension API (Java, Python via Jython, or Burp's native scripting)
- **Forbidden:** copying an existing published extension's core logic

**Description.** A working Burp extension that automates one specific, non-trivial check from an earlier subject — e.g. flagging responses missing security headers (HTTP Internals), or flagging a reflected marker's context the way the Client-Side Injection capstone did — integrated as a real Burp tab or passive scan check, not a standalone script.

!!! success "Mandatory"

    - A functioning extension loaded into Burp that registers either a passive scan check (runs automatically on every proxied request/response) or an active custom tab, your choice, justified by which fits your chosen check better.
    - The check itself reuses real logic from an earlier subject's tool (e.g. your `headersec0` header-analysis logic from HTTP Internals, ported into the extension) rather than being trivial/new — the point is integrating prior work into the professional workflow, not writing a check from scratch.
    - Findings surfaced through Burp's native issue-reporting mechanism (so they appear in the standard Issues view alongside Burp's own scanner findings, if using Professional) or a clearly labeled custom results tab if using Community.
    - Demonstrated running live against real traffic generated by browsing/proxying through one of your earlier vulnerable targets, correctly flagging the expected findings automatically as you browse — no manual re-analysis step required.
    - A written note on the extension API's actual capabilities and constraints you learned (e.g. what passive checks can and can't do without blocking the request pipeline) that you wouldn't have known without building one.

!!! failure "Forbidden"

    - Copying an existing published Burp extension's core detection logic — your own earlier tool's logic, ported, is required.
    - A "check" so trivial (e.g. flagging the literal string "password" in a response) that it doesn't demonstrate real integration work.

!!! note "Norm"

    The extension's check logic is factored separately from the Burp-API glue code, so the underlying detection logic remains independently testable outside Burp.

!!! tip "Bonus"

    A second, active-scan-style check that sends an additional probe request (not just passively observing) — e.g. automatically retrying a request with a mutated header to test for a specific misconfiguration.

### Exercise 02 — collaboratorconfirm0

- **Turn-in dir:** burp_mastery_portswigger/ex02/
- **Files:** EXPLOIT.md, evidence/
- **Allowed:** Burp Collaborator (or a self-hosted equivalent if Collaborator's hosted service isn't available to you)
- **Forbidden:** none beyond the global list

**Description.** A blind vulnerability (reusing an XXE, SSRF, or command-injection target from earlier subjects) confirmed via Burp Collaborator instead of your own hand-built OOB listener — professionalizing the OOB-confirmation technique you've now built from scratch twice into the tool a real engagement actually uses.

!!! success "Mandatory"

    - Generate a unique Burp Collaborator payload (a subdomain/URL) and inject it into a blind-vulnerable target from an earlier subject (your choice: the blind XXE from Server-Side Injection, the SSRF target from File Handling, or a blind command injection).
    - Demonstrate the interaction appearing in Burp's Collaborator client, including inspecting the specific interaction type (DNS, HTTP, or SMTP) and what each type's appearance tells you about the vulnerable component's network capabilities (e.g. a DNS-only interaction suggests outbound HTTP may be blocked while DNS resolution isn't — a real, actionable piece of network intelligence, not just a yes/no confirmation).
    - A direct comparison, run side by side on the same target, between your own hand-built OOB listener from an earlier capstone and Collaborator — same finding, both confirming it — with a written note on the practical tradeoffs (Collaborator requires no infrastructure setup and gives richer interaction metadata; a self-hosted listener gives full control and works in fully air-gapped/internal engagements where Collaborator's hosted service can't reach out).
    - A demonstration of Collaborator's polling/async nature specifically: fire the injection, then poll for interactions after a delay (as you would in a real engagement against a target that processes the payload asynchronously, e.g. a background job), rather than assuming confirmation must be instantaneous.

!!! failure "Forbidden"

    - Using Collaborator against any target other than your own.
    - Treating "no interaction yet" as "not vulnerable" without accounting for asynchronous processing delay.

!!! note "Norm"

    EXPLOIT.md documents the injected payload, the Collaborator interaction log entry, and the side-by-side comparison clearly.

!!! tip "Bonus"

    If a self-hosted Collaborator server is feasible in your lab, stand one up and repeat the confirmation using it instead of PortSwigger's hosted service, noting what changes operationally.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** every single vulnerability class covered across this entire roadmap so far, at a breadth and volume no individual subject's three-to-four exercises can match, against Academy's deliberately varied, realistically messy lab implementations — the same vulnerability class implemented five different ways across five different labs, which is exactly the variation real applications present and this roadmap's own hand-built targets, however carefully designed, cannot fully substitute for.

### Capstone — portswigger_academy_complete

- **Turn-in dir:** burp_mastery_portswigger/capstone/
- **Files:** PROGRESS.md, writeups/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** Complete PortSwigger Web Security Academy in full — every topic, every lab, including the expert-tier labs — the roadmap's explicit, non-negotiable exit gate for this stage, with a personal writeup per topic area proving understanding beyond "solved."

!!! success "Mandatory"

    - All Academy topics completed at "Practitioner" or "Expert" level for every lab that offers a tiered difficulty, with no lab skipped — a completion tracker (PROGRESS.md) listing every topic area and every lab within it, checked off with the date completed.
    - For each major topic area (SQL injection, XSS, CSRF, SSRF, XXE, access control, authentication, deserialization, SSTI, request smuggling, GraphQL, and every other area Academy covers, including any not otherwise covered by name in this roadmap), a short writeup (not a walkthrough) per topic area: what pattern unified the labs in that area, which specific lab was hardest and why, and how it connects to something you built or exploited elsewhere in this roadmap.
    - At least 5 of the expert-tier labs specifically flagged in your writeups with a deeper note: expert labs are designed to require chaining multiple bug classes or unusual reasoning, and the note should show that reasoning, not just the final payload.
    - A final reflection tying the whole roadmap so far together: which Academy topic most changed how you'd approach black-box testing in the future, and why.
    - Evidence: for at least 10 labs of your choosing spanning different topic areas, a screenshot or exported proof of the "Congratulations, you solved this lab" confirmation alongside your writeup for that lab.

!!! failure "Forbidden"

    - Using a published walkthrough/solution for any lab — solve every lab yourself; reading a hint after genuine attempt is fine, copying a solution is not.
    - Marking a lab complete in the tracker without actually having solved it.
    - A writeup that's a step-by-step walkthrough instead of a synthesis of what the topic area taught.

!!! note "Norm"

    PROGRESS.md and the writeups directory are organized by Academy's own topic taxonomy, for easy cross-reference against Academy's own site structure.

!!! tip "Bonus (§II.7)"

    Publish your topic-area writeups (not solutions/walkthroughs — synthesis and reasoning only, respecting Academy's own request not to publish solutions) as a public blog series, an early contribution toward the roadmap's later portfolio-building goals.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
burp_mastery_portswigger/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Exercises 00-02 are defended live inside Burp itself. The capstone is verified against your completion tracker and a live, unrehearsed walkthrough of at least two labs the evaluator selects from your writeups, solved again from scratch if the evaluator asks.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — burpworkflow0

**Defense questions**

1. Run this live in Burp, narrating your attack-type choice and configuration as you go.
2. Why is Cluster Bomb wrong (or right) for this specific exploit, compared to Pitchfork — walk through what each would actually do differently here.
3. Show your grep/extract configuration and explain what it's pulling from each response and why.
4. What did the original hand-rolled script version teach you that using Burp alone, from the start, would not have?

### A.1 — burpextension0

**Defense questions**

1. Load and demonstrate the extension live, browsing your target and showing findings appear automatically.
2. Walk through the extension API call that hooks into Burp's request/response pipeline — what exactly triggers your check?
3. Why did you choose a passive check versus an active/custom-tab approach for this specific detection logic?
4. What extension-API limitation did you run into, and how did you work around it (or document it as a limitation)?

### A.2 — collaboratorconfirm0

**Defense questions**

1. Fire the injection live and show the Collaborator interaction arriving.
2. Explain what a DNS-only interaction (versus an HTTP interaction) tells you about the target's outbound network restrictions.
3. Compare this to your own hand-built listener from an earlier subject — when would you actually prefer each, in a real engagement?
4. Why does asynchronous processing matter for how you interpret "no interaction yet" during a real test?

### A.3 — Capstone: portswigger_academy_complete

**Defense questions**

1. Pick three topic areas at random — walk through the unifying pattern you identified and the hardest lab in each, live, without notes.
2. Pick one expert-tier lab and walk through the full chained reasoning that solved it.
3. What Academy topic most changed your approach to testing, and give a concrete before/after example from your own work in this roadmap.
4. Show me your completion tracker and account for its state — anything not yet complete, and why.

**Test / edge cases**
