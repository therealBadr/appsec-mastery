---
title: "The Subject"
description: "The tooling layer underneath everything else in this roadmap — concurrent sockets, binary packing, subprocess handling that doesn't open a second vulnerab…"
---
# Bash and Python for Security: The Subject

*Subject 6 of 6 — Foundations Reset · Version 1.0 — September 2026*

> The tooling layer underneath everything else in this roadmap — concurrent sockets, binary packing, subprocess handling that doesn't open a second vulnerability while closing the first, and the Burp-adjacent HTTP fuzzing primitives you will otherwise depend on a GUI for forever.

## Chapter 00 — Foreword

> *Every security tool you will ever use started as someone's script that got popular. Write the script first and you will never mistake the tool for magic again.*

This is the last Stage 0 subject on purpose: it assumes the networking, HTTP, OS, and SQL depth from the rest of the stage and turns it into reusable tooling instinct. The four builds here are not toy exercises — a subdomain enumerator, a banner grabber, and a hand-built HTTP fuzzer are the actual internals of tools like `amass`, `masscan`, and Burp Intruder, at a scale you can still read top to bottom.

## Chapter I — Introduction

You will build a concurrent subdomain enumerator, a CIDR-range banner grabber, and a stripped-down HTTP fuzzer that flags anomalous responses the way Burp Intruder's response-diffing does — then combine all three into a single recon pipeline that takes a domain and produces a structured attack-surface report with zero manual steps in between.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input, an unreachable host, or unexpected data. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline), applies to every exercise.** Functions do one thing and are named for what they do. No magic numbers — ports, offsets, thresholds, and protocol constants are named constants, never bare literals. No block of code you cannot explain, unprompted, line by line, during defense. Every non-obvious line carries a comment explaining why, not what.

**II.3** **Evidence, not assertions.** Every claim of the form "this detects X" or "this parses Y correctly" must be backed by a reproducible capture, transcript, or log — captured in your turn-in. Assertions without evidence are treated as unmet requirements during defense.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct. A single mandatory-part flaw — even a minor one — zeroes the bonus evaluation for that exercise, no exceptions.

**II.5** **Scope.** Exercises target domains/hosts you own or a lab environment (e.g. your own VPS, a deliberately vulnerable app you run locally). Subdomain enumeration and fuzzing against third-party infrastructure without written authorization is out of scope for this subject, full stop.

**II.6** **Global forbidden list.** No `subfinder`/`amass`/`ffuf`/`gobuster`/`masscan` — you are building minimal versions of exactly these tools. `shell=True` in `subprocess` calls is forbidden anywhere in this subject unless the exercise explicitly requires demonstrating why it's dangerous.

## Chapter III — Mandatory Part

### Exercise 00 — subenum0

- **Turn-in dir:** bash_python_security/ex00/
- **Files:** subenum0.py, README.md
- **Allowed:** socket, concurrent.futures/asyncio/threading, standard library only
- **Forbidden:** subfinder, amass, dnspython for the core resolution logic

**Description.** A concurrent subdomain enumerator: given a domain and a wordlist, resolves each candidate subdomain and reports which exist, with real concurrency and real rate control — not a naive serial loop with a library doing the DNS work for you.

!!! success "Mandatory"

    - Constructs and sends DNS A-record queries for each candidate subdomain using raw `socket` (UDP to a configurable resolver) — reusing/extending your `dnsresolve0` logic from Networking Depth is expected, not discouraged.
    - Runs lookups concurrently (thread pool, process pool, or asyncio — your choice, justified) with a configurable concurrency limit, and measurably faster than a serial baseline you also implement and benchmark against.
    - Implements basic rate limiting/backoff so the tool does not flood the resolver into dropping responses — demonstrated by comparing result completeness at an unthrottled vs. throttled concurrency level against your own test resolver.
    - Correctly handles wildcard DNS (a domain that resolves \*every\* subdomain to the same IP, which would otherwise produce 100% false positives) by detecting the wildcard pattern first and filtering it out.
    - Outputs discovered subdomains with their resolved IP(s), and a summary of query count, success rate, and elapsed time.

!!! failure "Forbidden"

    - dnspython or any DNS library doing the packet construction/parsing for you.
    - A tool with no concurrency limit that can be trivially turned into a denial-of-service against the target's DNS infrastructure.
    - Silently returning wrong results on a wildcard domain instead of detecting and handling it.

!!! note "Norm"

    See §II.2, plus: resolution, concurrency orchestration, wildcard detection, and reporting each in their own function; concurrency limit and timeout as named config values.

!!! tip "Bonus"

    Passive enumeration via Certificate Transparency logs (crt.sh) as an additional, clearly-labeled data source alongside your active brute-force results.

### Exercise 01 — bannergrab0

- **Turn-in dir:** bash_python_security/ex01/
- **Files:** bannergrab0.py, README.md
- **Allowed:** socket, ssl, concurrent.futures/asyncio, ipaddress standard module
- **Forbidden:** masscan, nmap, python-nmap

**Description.** A tool that scans a CIDR range for a set of common ports, grabs service banners (including a TLS-wrapped banner where relevant), and identifies services from the banner text into a structured report — the connect-and-read pattern underneath every recon tool's "service detection" feature.

!!! success "Mandatory"

    - Given a CIDR (using the `ipaddress` module to enumerate hosts) and a port list, connects to each host:port concurrently with a sane timeout, and reads the first response bytes (or, for ports needing a prompt like HTTP, sends a minimal valid request first).
    - Correctly handles at least one TLS-wrapped service (e.g. HTTPS on 443) by wrapping the socket with `ssl` before reading the banner, and reports the negotiated TLS version alongside the banner.
    - Identifies service/product from the banner text against a small signature table you build (e.g. recognizing `SSH-2.0-OpenSSH_X.Y`, an `HTTP/1.1` status line with a `Server:` header, etc.), reporting "unidentified" honestly when no signature matches rather than guessing.
    - Structured output per host: open ports, raw banner, identified service/version where possible, and a timestamp.
    - A written note on why banner-based version identification is inherently unreliable (banners can be spoofed, stripped, or genuinely ambiguous) and what that means for trusting this tool's output at face value.

!!! failure "Forbidden"

    - nmap/masscan/python-nmap doing the scanning or the service identification for you.
    - A synchronous, unbounded-timeout scanner that takes hours on a /24 with no way to configure concurrency.
    - Claiming a confident service identification from an ambiguous or generic banner.

!!! note "Norm"

    See §II.2, plus: CIDR expansion, connection/banner-grab, TLS handling, and signature matching each in their own function.

!!! tip "Bonus"

    Add UDP banner grabbing for at least one UDP service (e.g. DNS version query) with the inherent unreliability of UDP handled (retries, explicit "no response" vs "closed" distinction from Networking Depth carried over here).

### Exercise 02 — httpfuzz0

- **Turn-in dir:** bash_python_security/ex02/
- **Files:** httpfuzz0.py, README.md
- **Allowed:** requests or raw sockets, concurrent.futures/asyncio
- **Forbidden:** Burp Intruder, ffuf, wfuzz, any existing fuzzing tool

**Description.** A stripped-down HTTP fuzzer: takes a request template with a marked injection point and a payload wordlist, sends every payload, and flags responses that differ meaningfully from a measured baseline — by status, length, and timing — the exact mechanism behind Burp Intruder's "Grep/Extract" and response-diffing.

!!! success "Mandatory"

    - Accepts a request template (method, URL, headers, body) with a placeholder marker (e.g. `FUZZ`) and a wordlist file, and substitutes each payload into the marked position — URL, a query parameter, a header value, or the body, your choice of which positions to support, at least two of the four.
    - Sends a baseline request first (with an inert placeholder value) and records its status code, response length, and response time as the comparison point.
    - For every payload, records status/length/time and flags a response as anomalous if it differs from baseline by more than a configurable threshold in any dimension — not just exact-match filtering.
    - Runs concurrently with a configurable worker count and a rate limit, and includes basic retry/backoff on transient connection errors rather than treating a dropped connection as a legitimate response.
    - Outputs a sorted, scannable report: payload, status, length, time-delta-from-baseline, and an anomaly flag — the same shape as Burp Intruder's results grid.

!!! failure "Forbidden"

    - Burp Intruder, ffuf, wfuzz, or any existing fuzzer wrapped and relabeled.
    - Flagging every non-200 response as anomalous with no actual baseline comparison.
    - A concurrency model with no rate limit that can trivially become a denial-of-service against the target.

!!! note "Norm"

    See §II.2, plus: template-substitution, baseline measurement, request execution, and anomaly-detection each in their own function.

!!! tip "Bonus"

    Add a second, independent anomaly signal: response-body similarity (e.g. a simple diff ratio) instead of just length, to catch same-length-but-different-content responses.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** concurrent DNS resolution, raw socket/TLS service interaction, and HTTP request construction/anomaly-detection, chained so each stage's output correctly becomes the next stage's input — discovered subdomains feed the port scanner, discovered open HTTP(S) ports feed the fuzzer — with concurrency and rate-limiting reasoned about at the pipeline level, not just per-stage, since three separately-well-behaved tools run back to back can still add up to an unintentional denial-of-service against the target. No single exercise above has to reason about that compounding effect; the capstone does, by construction.

### Capstone — reconpipe

- **Turn-in dir:** bash_python_security/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A single pipeline that takes one domain and, unattended, runs subdomain enumeration, then banner-grabs every discovered live host, then fuzzes any discovered HTTP endpoints with a small default payload set for anomalies — producing one structured, prioritized attack-surface report with zero manual steps between stages.

!!! success "Mandatory"

    - Stage 1: runs your `subenum0` logic against the target domain and a wordlist, producing a list of live subdomains with resolved IPs.
    - Stage 2: runs your `bannergrab0` logic against every discovered IP on a default port list (at minimum 22, 80, 443, 8080), producing service/banner data per host, and specifically identifying which hosts are serving HTTP/HTTPS.
    - Stage 3: for every discovered HTTP(S) endpoint, runs your `httpfuzz0` logic with a small default wordlist (e.g. common path segments) against the URL path, flagging anomalous responses (candidate hidden endpoints) per host.
    - Pipeline-level concurrency/rate governance: a single global rate-limit/concurrency budget that stages 1–3 share or respect in sequence, with written reasoning for why per-stage limits alone are not sufficient to bound total request volume against one target.
    - One final consolidated report combining all three stages: for each live host, its open ports/services and any flagged anomalous paths, ranked by a simple priority heuristic you define and justify (e.g. non-standard open ports and flagged anomalies rank above a clean, fully-expected HTTP/HTTPS-only host).
    - Demonstrated end to end against your own VPS/lab domain with at least one intentionally-hidden path seeded for the fuzz stage to find, proving the full chain works without manual intervention between stages.

!!! failure "Forbidden"

    - Any of the forbidden tools from Exercises 00–02, anywhere in the pipeline.
    - Running any stage against a target outside your own lab/domain.
    - A pipeline with no global rate governance, where each stage independently maxes out concurrency regardless of what the other stages already sent.
    - Silently dropping a stage's failure (e.g. DNS resolver unreachable) instead of reporting it and degrading gracefully.

!!! note "Norm"

    See §II.2, plus: each stage remains an independently callable/testable module (reusing Exercises 00–02's code, not reimplementing), with a single orchestrator that sequences them and owns the shared rate/concurrency budget.

!!! tip "Bonus (§II.7)"

    A resumable run — if the pipeline is interrupted after Stage 1, a re-run picks up from Stage 2 using cached Stage 1 output instead of re-enumerating from scratch.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
bash_python_security/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live against your own lab environment, which the evaluator may reseed with different hosts/wordlist entries beforehand. For the capstone, the evaluator may add a new hidden path or a new listening service to your lab domain immediately before the defense and expects the pipeline to surface it without any code changes.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — subenum0

**Defense questions**

1. Show me your wildcard-detection logic running live against a domain configured with a wildcard record — walk through exactly how it avoids the false-positive flood.
2. Why does an unthrottled concurrent resolver risk becoming a denial-of-service tool against the target's own DNS infrastructure, and what specifically did you do about it?
3. What is your concurrency model (threads/processes/asyncio) and why did you pick it for this specific workload (I/O-bound DNS lookups)?
4. Show your serial-vs-concurrent benchmark — what was the actual speedup, and where does the benefit taper off as you increase concurrency further?

### A.1 — bannergrab0

**Defense questions**

1. Show me your CIDR expansion on a real range — how many hosts, and how does your concurrency limit keep this from being effectively a denial-of-service scan?
2. Walk through your TLS-wrapped banner grab live — where exactly does the TLS handshake happen relative to reading the banner?
3. Give me an example banner your signature table correctly identifies, and one it correctly refuses to guess on — why the difference?
4. What stops this tool from being indistinguishable, from the target's perspective, from the reconnaissance phase of a real attack — and why does that mean scope authorization matters here specifically?

### A.2 — httpfuzz0

**Defense questions**

1. Run this live against your own Exercise 02 login endpoint from SQL and Database Internals with a small SQLi payload wordlist — walk me through which result gets flagged and why.
2. Why is length-only anomaly detection insufficient on its own — give a concrete case where it would miss something a length-plus-timing check would catch.
3. Show your baseline measurement — why does it matter that you measure baseline timing more than once, if you do?
4. What specifically makes this dangerous to run against a target without authorization, distinct from just "sending some HTTP requests"?

### A.3 — Capstone: reconpipe

**Defense questions**

1. Run the full pipeline live against your lab domain — narrate what's happening as each stage hands off to the next.
2. Why can three individually-rate-limited stages still overwhelm a target if you don't reason about the pipeline as a whole — give me the concrete math for your own configured limits.
3. Show me the intentionally-hidden path you seeded — walk through exactly how the fuzz stage's anomaly detection caught it.
4. What happens if Stage 1 finds zero subdomains — does the pipeline degrade gracefully or does it crash trying to feed an empty list into Stage 2?
5. Justify your priority-ranking heuristic in the final report with a concrete example from your own run.
6. If I ask you to point this at a domain you don't own right now, what do you say, and why?

**Test / edge cases**

- [ ] Zero subdomains discovered: pipeline reports this clearly and exits cleanly rather than crashing on empty input to Stage 2.
- [ ] A discovered host with no open ports from the default list: reported as scanned-but-closed, not omitted from the report entirely.
- [ ] A discovered HTTP(S) endpoint that returns identical responses for every fuzzed payload (a catch-all 200 page): correctly reported as zero anomalies, not a false positive flood.
- [ ] DNS resolver becomes unreachable mid-Stage-1: pipeline reports a partial result and a clear error, does not hang indefinitely.
- [ ] A host that responds to banner-grab but drops the connection during the HTTP fuzz stage: reported as a connectivity anomaly for that host, not silently skipped.
- [ ] The same host appearing under two different discovered subdomains (duplicate IP): fuzzed once, not redundantly, or explicitly documented if you chose to fuzz per-hostname instead of per-IP.
- [ ] Pipeline interrupted (Ctrl-C) mid-run: partial results already gathered are not lost/discarded silently.
