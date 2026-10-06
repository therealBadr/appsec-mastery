---
title: "The Subject"
description: "Harden, instrument, and defend a real Linux host from first principles — filesystem, permissions, processes, systemd, packet filtering, capabilities, and …"
---
# Linux Administration Depth: The Subject

*Subject 1 of Stage 0 — Foundations Reset · Version 1.0 — August 2026*

> Harden, instrument, and defend a real Linux host from first principles — filesystem, permissions, processes, systemd, packet filtering, capabilities, and logs — with nothing you cannot personally explain, line by line, while someone is watching.

## Chapter 00 — Foreword

> *Root is not a permission. It is the absence of a decision.*

A system is not hardened because you ran a script that says so. It is hardened because you can put it in front of a live attacker, watch, and explain afterward exactly why it held — or exactly why it didn't.

## Chapter I — Introduction

This subject closes the gap between "I used the terminal" and "I understand what the terminal is talking to." You will provision a real host, harden it, instrument it, and finally build a daemon that defends it autonomously. Every exercise below stands alone and is turned in separately, but they share one box: your own VPS. By the end of Chapter IV that box will be running code you wrote to detect and respond to a live attack, unsupervised.

## Chapter II — General Instructions

**II.1** **Evaluation environment.** Every exercise is evaluated on a real, disposable Linux VPS you provision yourself (Debian or Ubuntu, minimal image), administered entirely over SSH. No GUI, no desktop environment, no cloud-console point-and-click substitutes for a command you were supposed to run yourself.

**II.2** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input, missing permissions, or unexpected system state. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.3** **Norm (code-quality baseline), applies to every exercise.** Functions do one thing and are named for what they do. No magic numbers — thresholds, ports, paths, and time windows are named constants or config values. No block of code you cannot explain, unprompted, line by line, during defense. Scripts are modular: one function per pipeline stage, not one monolith. Every non-obvious line carries a comment explaining why, not what.

**II.4** **Global forbidden list.** Unless an exercise explicitly says otherwise: no `nmap`, `scapy`, `lsof`, `netstat`, `ss`, `fail2ban`, `OSSEC`, `Wazuh`, `auditd`, `ufw`, `SQLMap`, `dnspython`, or any library/tool that performs the exercise's core mechanism for you. Reading their source for ideas is allowed. Depending on them at runtime is not.

**II.5** **Evidence, not assertions.** Every claim of the form "this control works" must be backed by a reproducible demonstration — a command, a log line, a failed attack attempt — captured in your turn-in. Assertions without evidence are treated as unmet requirements during defense.

**II.6** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct. A single mandatory-part flaw — even a minor one — zeroes the bonus evaluation for that exercise, no exceptions.

## Chapter III — Mandatory Part

### Exercise 00 — bastion0

- **Turn-in dir:** linux_admin_depth/ex00/
- **Files:** harden.sh, README.md, evidence/
- **Allowed:** ssh, nftables, fail2ban, systemd, unattended-upgrades
- **Forbidden:** ufw (as final artifact), ansible/puppet/chef, any hardening script you did not write

**Description.** Provision a fresh VPS and convert it into a defensible bastion host via a single idempotent script, with every control verified by a live attack you run against your own box — not asserted from memory.

!!! success "Mandatory"

    - Fresh minimal Debian/Ubuntu image — no cloud-provider "hardened" template.
    - SSH: key-only auth, root login disabled, non-default port, capped `MaxAuthTries`, idle timeout, `AllowUsers`/`AllowGroups` restricted to your account.
    - Firewall: default-deny inbound, final ruleset in raw **nftables** — explicit allow rules per service actually running.
    - Brute-force mitigation with a jail definition you wrote/tuned yourself — failure count, window, and ban duration each justified in writing.
    - Every enabled service audited from `systemctl list-unit-files`; every one you keep is justified in writing.
    - Unattended security updates configured, with a written note on what this does and does not protect against.
    - All of the above encoded in one idempotent script: running it twice produces identical system state, no duplicate rules, no errors.

!!! failure "Forbidden"

    - A hardening script copy-pasted without being able to delete any single line and correctly predict the consequence.
    - A control claimed without evidence.
    - A control left partially applied (e.g. firewall "enabled" with a catch-all allow rule that defeats it).

!!! note "Norm"

    See §II.3, plus: single entry-point script, idempotency checks before every mutation, config values isolated at the top of the file.

!!! tip "Bonus"

    TOTP 2FA on SSH; webhook alert on brute-force-jail trigger; full idempotent-tool (Ansible) rewrite of the hardening script.

### Exercise 01 — logsentry

- **Turn-in dir:** linux_admin_depth/ex01/
- **Files:** logsentry.sh, README.md, sample_logs/
- **Allowed:** grep, awk, sed, sort, uniq, cut, date, comm, join, zcat/zgrep, bash builtins
- **Forbidden:** python, perl, ruby, any interpreter invoked anywhere in the pipeline

**Description.** A pure-Bash CLI that ingests a real auth.log/journalctl stream — including rotated, gzip-compressed history — and surfaces brute-force patterns, ranked offenders, and attack timing.

!!! success "Mandatory"

    - Parses real `auth.log` or `journalctl -u ssh` output, plus a rotated `.gz` log, extracting source IP, timestamp, attempted username, success/failure per line.
    - Computes: top-N offending IPs by failed-attempt count, per-hour attempt buckets, first-seen/last-seen per IP.
    - Implements a configurable sliding-window brute-force detector (N attempts in M seconds) using only bash/awk/`date` arithmetic.
    - Output as both a human-readable table and machine-parseable TSV/CSV via a flag.

!!! failure "Forbidden"

    - Shelling out to an interpreter for date-math or windowing logic.
    - Hardcoded log-format/year assumptions that break silently on a different distro's syslog layout, with no detection or error.
    - Silently discarding malformed lines — they must be counted and reported.

!!! note "Norm"

    See §II.3, plus: separate functions for extract / aggregate / detect / format; `set -euo pipefail`; trap-based temp-file cleanup; no magic numbers for window sizes.

!!! tip "Bonus"

    ASCII bar chart of attempts per hour in pure bash; offline ASN/network-range grouping with no GeoIP service call.

### Exercise 02 — procwatch

- **Turn-in dir:** linux_admin_depth/ex02/
- **Files:** procwatch.sh, README.md
- **Allowed:** /proc filesystem only
- **Forbidden:** lsof, netstat, ss, any /proc-wrapping library

**Description.** A Bash tool that enumerates every process and every listening/established socket purely by reading `/proc`, manually correlating socket inode numbers to owning PIDs via file descriptors.

!!! success "Mandatory"

    - Enumerate all `/proc/[pid]` entries: cmdline, `exe` symlink target, owning uid/gid, and **PPID** — all read from `/proc/[pid]/status`.
    - Parse `/proc/net/tcp`, `tcp6`, `udp`, `udp6`: decode local address:port from hex, decode connection state.
    - Correlate each socket's inode (from the `/proc/net/tcp` inode column) to its owning PID by scanning `/proc/[pid]/fd/*` for `socket:[inode]` targets.
    - Output per flagged process: PID, PPID, name, owning user, port(s), state, executable path.
    - Flag processes listening on `0.0.0.0`/`::` as higher-risk than loopback-only.
    - Using the PPID chain, flag any listening process whose parent is not an expected ancestor (`systemd`/PID 1, or another explicitly allow-listed service manager) — a process spawned by `cron`, `at`, or a shell and now holding a listening socket is exactly this pattern.

!!! failure "Forbidden"

    - ss/lsof/netstat inside the shipped tool logic (external comparison during your own testing is fine).
    - Hardcoding known ports instead of generically decoding the hex address field.
    - Crashing or silently omitting a process when `/proc/[pid]/fd` is unreadable — must be reported as permission-denied.
    - Flagging parentage by process *name* instead of walking the actual PPID chain — a renamed process must not evade the ancestry check.

!!! note "Norm"

    See §II.3, plus: separate functions for proc enumeration, socket-table parsing, inode-to-PID correlation, output formatting; named constants for the `/proc/net/tcp` column layout.

!!! tip "Bonus"

    Continuous watch mode diffing against the previous scan; cross-reference against a baseline allow-list file.

### Exercise 03 — suidwatch

- **Turn-in dir:** linux_admin_depth/ex03/
- **Files:** suidwatch.sh, baseline.conf, README.md
- **Allowed:** find, stat, coreutils
- **Forbidden:** any prewritten SUID-auditing tool

**Description.** A Bash tool that walks the filesystem, finds every setUID/setGID binary and every world-writable file/directory, classifies each against a real baseline, and produces a risk-annotated report you can defend line by line.

!!! success "Mandatory"

    - Full `find`-based traversal for setUID (04000), setGID (02000), and world-writable (`o+w`) files/directories; world-writable directories missing the sticky bit flagged as higher risk.
    - Exclusions (e.g. `/proc`, `/sys`) minimal and explicitly justified — not a blanket skip of large parts of the tree.
    - Every found setUID/setGID binary cross-referenced against a maintained baseline of expected binaries for your distro; anything not on the baseline is flagged as unexpected.
    - Report per flagged item: path, permission bits (symbolic + octal), owner, group, mtime, and a one-line note on what the binary actually does — looked up, not guessed.
    - Runs without root where possible; unscanned paths due to permissions are explicitly reported, never silently skipped.

!!! failure "Forbidden"

    - A static allowlist copied from a blog without verifying it against your actual system.
    - Treating "found" as automatically "dangerous" with no investigation of what the binary does.
    - Excluding large filesystem regions "to save time" without written justification.

!!! note "Norm"

    See §II.3, plus: modular functions for traversal, classification, baseline diff, reporting; baseline lives in a config file, never hardcoded inline.

!!! tip "Bonus"

    Diff mode against a saved prior report; expose this as a callable module for the Chapter IV capstone's permission-drift check.

### Exercise 04 — linux_for_security_engineers

- **Turn-in dir:** linux_admin_depth/ex04/
- **Files:** README.md (published externally, link required)
- **Allowed:** your own terminal output only
- **Forbidden:** copied screenshots, copied explanations

**Description.** A published reference document on the Linux permission model, `/proc` internals, local auth internals, and log semantics — rigorous enough that another engineer could learn the material from it alone.

!!! success "Mandatory"

    Every section below must include command output you personally generated, plus a "why this matters for security" paragraph:

    - Filesystem hierarchy — **`/proc`, `/sys`, `/dev`, `/etc`, and `/var/log` each explicitly covered**, not summarized as one generic "filesystem" section — and what each exposes to an attacker.
    - Full permission model with worked numeric examples of setUID/setGID/sticky bit.
    - `/etc/passwd` and `/etc/shadow` field-by-field including hash-algorithm identification.
    - Process/signal model with a real fork/exec trace (e.g. via strace).
    - systemd unit anatomy using a real unit file you wrote.
    - iptables/nftables chain/table concepts against a real ruleset you built.
    - Linux capabilities — **`CAP_NET_BIND_SERVICE` and `CAP_SYS_PTRACE` specifically explained** (what each grants, what it would let an attacker do if present on a compromised process), plus drop one real capability from a real process and show the resulting behavior change.
    - `/proc/[pid]/maps` and `/proc/[pid]/fd` walked against a real running process.
    - **Cron and scheduled-task persistence** — `/etc/crontab`, `/etc/cron.d/`, per-user crontabs (`crontab -l`), and systemd timers, with a real (planted-then-removed) example of a cron-based persistence mechanism on your own VPS and the exact artifact it leaves behind.
    - auth.log/syslog field breakdown using real (redacted) log lines.
    - Published externally.

!!! failure "Forbidden"

    - Unattributed lifting of explanations from tutorials/blogs.
    - Screenshots or output you didn't personally generate.
    - Purely definitional sections with no security-implication paragraph.

!!! note "Norm"

    See §II.3, plus: consistent structure per section (concept → command → output → implication); no jargon introduced without a first-use definition.

!!! tip "Bonus"

    French-language version; companion cheat-sheet PDF generated from the writeup.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** filesystem hierarchy knowledge, the full permissions model, users/groups/authentication internals, processes and signals, systemd, iptables/nftables, Linux capabilities, cron/persistence mechanisms, and log analysis — all in one running system. No exercise above requires more than two or three of these at once; this one requires all of them, simultaneously, under one running process. Someone who only learned log parsing can build the detector, but the daemon will not start without correct capability/systemd configuration. Someone who only learned nftables can block IPs, but has no detection signal to act on. Someone who only learned `/proc` can enumerate sockets, but cannot turn that into a defensible, auditable, self-limiting response. Someone who only read about cron abuse in the abstract has never had to actually diff a live crontab against a baseline under a running daemon. Partial knowledge fails visibly at integration, not at the end.

### Capstone — sentineld

- **Turn-in dir:** linux_admin_depth/capstone/
- **Files:** src/, sentineld.service, config/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.6

**Description.** Build and operate `sentineld`: a systemd-managed daemon, running as a dedicated unprivileged system user with the minimum Linux capabilities required, that continuously detects SSH brute-force patterns, unexpected listening sockets, and setUID/permission drift, and automatically contains detected threats via nftables rules with automatic expiry — with a full structured audit trail.

!!! success "Mandatory"

    - Runs as a systemd service under a dedicated non-root system account created by you (`User=`, `Group=` in the unit), never root.
    - Drops to the minimal capability set required (e.g. `CAP_NET_ADMIN` only, via `AmbientCapabilities`/`CapabilityBoundingSet` or `setcap`) — you must be able to justify why full root is unnecessary.
    - Implements, as one integrated system:
        - An auth log / `journalctl` parser detecting sliding-window SSH brute force (configurable N attempts in M seconds).
        - A `/proc`-only process & socket scanner cross-referencing listening sockets against a baseline allow-list, flagging new unexpected listeners, and flagging PPID-chain ancestry anomalies exactly as in Exercise 02.
        - A permission-drift auditor that snapshots setuid/setgid/world-writable state at startup and alerts on any change from that baseline.
        - A cron/systemd-timer persistence auditor that snapshots the system crontab, every file under `/etc/cron.d/`, every per-user crontab, and all enabled systemd timer units at startup, and alerts on any entry added, removed, or modified since that baseline — the same drift-detection pattern applied to scheduled-task persistence instead of file permissions.
        - Automatic nftables containment: flagged IPs get dropped in a dedicated chain your daemon creates and manages, with configurable automatic expiry.
        - A structured JSON audit log of every detection and every action taken.
    - Proper systemd integration: `Restart=on-failure`, logs via journald (not a bypassing custom file logger), and a `SIGHUP` handler that reloads configuration without a full restart — handled explicitly in your code.
    - Baseline (allowed ports, allowed setuid binaries) driven entirely by a config file — no hardcoded values.
    - A dry-run mode that logs proposed nftables actions without applying them, and a live mode that applies them.
    - Demonstrated end-to-end on a real VPS (the same one from Exercise 00) against a real simulated brute-force attack (e.g. hydra/medusa from a second host) — captured as a full terminal transcript or recording showing detection through automatic block through automatic expiry.

!!! failure "Forbidden"

    - fail2ban, OSSEC, Wazuh, auditd rules, or any existing HIDS doing the detection logic for you.
    - Any high-level log-management library that does the pattern matching for you — the sliding-window algorithm must be hand-implemented.
    - lsof/netstat/ss for socket enumeration anywhere in the daemon.
    - Any prewritten cron/persistence-auditing tool doing the crontab/timer diffing for you.
    - Running the daemon as root, ever, in the delivered artifact.
    - Wrapping someone else's iptables script and calling it "your nftables integration."
    - Swallowing exceptions/errors silently — every failure path is logged with cause.

!!! note "Norm"

    See §II.3, plus: modular by concern (log parser, proc scanner, permission auditor, firewall controller, audit logger) as separably testable units; functions under ~40 lines; no magic numbers for thresholds/windows/expiry.

!!! tip "Bonus (§II.6)"

    Webhook/Slack/email alerting; a read-only minimal dashboard as a separate unprivileged process; SQLite-backed audit trail with a query CLI; an allowlist-learning mode that proposes baseline updates for human review instead of trusting blindly.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
linux_admin_depth/
├── ex00/
├── ex01/
├── ex02/
├── ex03/
├── ex04/
└── capstone/
```

Each exercise is defended live, on your running VPS, from a clean terminal — not from slides, not from a pre-recorded demo unless the exercise explicitly allows a recording as evidence (capstone only). The evaluator may modify inputs, kill processes, corrupt state, or attack the system live and expects your program to behave exactly as specified in the Mandatory section, no better, no worse. An evaluator who cannot get your project to fail through a specified edge case should mark the exercise as passed; one who finds an unhandled case not explicitly listed in this subject applies §II.2 and asks you to defend it live.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense, the same way you'd rehearse against a barème before a real 42 defense.

### A.0 — bastion0

**Defense questions**

1. Walk me through what happens to a SYN packet on your SSH port from an IP with no matching rule yet — trace it through your actual ruleset.
2. Why this SSH port specifically, and what does changing it protect against — and what does it not protect against?
3. What's your exact fail2ban failure-count/window/ban-duration, and why those numbers instead of the defaults?
4. If I get valid key access to a low-privilege account on this box, what's my realistic path to root, and what have you done to make that harder?
5. A security update needs a service restart mid-incident — is that a risk with your current config? How would you know it happened?
6. Prove your script is idempotent — run it twice now and diff `nft list ruleset` before and after.
7. What's still exposed on this box right now, and why is that an acceptable risk?
8. What does raw nftables give you here that UFW would not have?

**Test / edge cases**

- [ ] Root SSH login attempt: rejected at auth, logged.
- [ ] 6 rapid failed SSH attempts from one IP inside the fail2ban window: IP banned, verified by a subsequent connection actually failing.
- [ ] Script run twice back-to-back: identical `nft list ruleset` output, no errors.
- [ ] Full port scan from an external host: only explicitly allowed ports respond.
- [ ] Simulated disk-full during log write: fail2ban/sshd protection doesn't silently stop.

### A.1 — logsentry

**Defense questions**

1. Show me, in actual bash, how you compute elapsed seconds between two syslog timestamps without invoking an interpreter.
2. Syslog's traditional timestamp has no year — how does your tool behave across a Dec 31 → Jan 1 boundary, and did you actually test that?
3. Feed it a line with a corrupted timestamp right now — show me what happens.
4. Why awk over raw bash string-splitting (or vice versa) — what did you actually measure?
5. Does this scale to a 2GB log file? Did you test at that size, or just on a small sample?
6. How does your IPv4/IPv6 detection regex differ, and does the sliding-window logic still hold for both?

**Test / edge cases**

- [ ] 10,000+ line log, mixed IPv4/IPv6.
- [ ] Gzip-rotated log where a single attack spans the rotation boundary — merges correctly by time.
- [ ] Malformed line mid-file — script continues, reports malformed count.
- [ ] Two IPs tied on failed-attempt count — tie-break behavior defined and documented.
- [ ] Zero failed attempts in the log — clean exit, no error.

### A.2 — procwatch

**Defense questions**

1. Walk me through the exact byte layout of the `local_address` column in `/proc/net/tcp` — what encoding, what byte order?
2. Show me your inode-to-PID correlation running live, line by line.
3. What happens when you lack permission to read another user's `/proc/[pid]/fd`? Prove it, don't describe it.
4. A process listening on `::` also serves v4 traffic in dual-stack mode — does your tool represent that correctly?
5. A process opens and closes a socket between two of your polling passes — could you miss it? Is that acceptable for this tool's stated purpose?
6. What do hex codes `0A` and `01` mean in the TCP state column?
7. How does correlation perform against a process holding 500 file descriptors — did you actually test that?
8. Walk the PPID chain of a flagged process live, right now, up to PID 1 — show me you're actually reading `/proc/[pid]/status` at each hop, not trusting `ps`'s tree view.
9. I spawn a listener from a cron job so its parent is a short-lived cron child that has already exited by the time you scan — does your ancestry check still work, or does it depend on the parent still being alive?

**Test / edge cases**

- [ ] Process listening on loopback only vs. `0.0.0.0` — correctly distinguished.
- [ ] Process you don't own with a listening socket — permission handling verified, no crash.
- [ ] Multiple processes sharing one socket via `SO_REUSEPORT` — handled correctly or the limitation is explicitly documented.
- [ ] Short-lived process opening/closing a port within one polling interval.
- [ ] Zero listening sockets system-wide — clean empty output.
- [ ] Process with a deleted-but-running binary (`exe (deleted)`) — handled without crashing.
- [ ] A process listening on a port whose parent is `systemd` (expected): not flagged. The same process re-parented to PID 1 after its original parent dies (a classic daemonizing pattern): correctly not confused with a malicious reparent.
- [ ] A process spawned by `cron` that opens a listening socket: flagged by the ancestry check specifically because its parent is `cron`, not an allow-listed service manager.

### A.3 — suidwatch

**Defense questions**

1. Walk me through what the kernel does differently at `execve()` when the setUID bit is set.
2. Pick a binary your tool flagged as unexpected — what does it do, and how did you verify that rather than guess from the name?
3. World-writable file vs. world-writable directory without the sticky bit — give me a concrete exploitation scenario for each.
4. How does your tool treat a symlink with the setUID bit on the target versus on the link itself?
5. I create a new setUID binary in `/tmp` right now — does a re-run catch it, and how fast relative to your traversal strategy?
6. Why exclude `/proc` and `/sys` specifically — what breaks if you don't?
7. What happens when your tool hits a directory it can't read into owned by root — does it report that clearly?

**Test / edge cases**

- [ ] New setUID binary in a non-standard path — flagged.
- [ ] Standard expected setUID binary (`/usr/bin/passwd`) — classified as expected, not flagged.
- [ ] World-writable directory with sticky bit (`/tmp`) vs. without — distinguished correctly.
- [ ] setGID-only binary — identified and labeled separately from setUID.
- [ ] Directory the running user can't traverse — reported as unscanned, not silently omitted.
- [ ] Symlink with different permissions than its target — both states captured.

### A.4 — linux_for_security_engineers

**Defense questions**

1. Pick any command output at random — explain every field without your notes.
2. Where did you actually run this (container/VM/bare metal), and does that change any internals you described?
3. Show the `/etc/shadow` line you documented — how do you identify its hash algorithm from the prefix?
4. Walk through the syscall sequence of the fork/exec you captured — what differs between parent and child return values?
5. Show your `setcap`/`getcap` output — what changes if that capability is removed?
6. `CAP_NET_BIND_SERVICE` and `CAP_SYS_PTRACE` — what does each grant specifically, and what could an attacker do with a process that holds one of them but is not root?
7. You planted a cron-based persistence example and then removed it — show me the exact file/line you added, and where its trace would still be visible in logs even after the crontab entry itself is deleted.
8. What's the difference in attacker value between `/etc/crontab`, `/etc/cron.d/`, and a per-user crontab — why would an attacker prefer one over another depending on their access level?
9. Pick one of `/dev` or `/sys` — show a real file under it and explain what reading or writing to it actually does at the kernel level.

**Test / edge cases**

- [ ] Every command must be independently reproducible on a stock Debian/Ubuntu VPS.
- [ ] Every log-field claim verifiable against the shown line.
- [ ] At least one worked example per section uses a non-trivial configuration, not just a default `systemctl status`.
- [ ] The cron-persistence example must show both the planting command and the specific log/artifact evidence it leaves, and confirm its removal leaves the system in its original state.

### A.5 — Capstone: sentineld

**Defense questions**

1. Why this specific capability set instead of root, and what's still possible if this daemon itself is compromised?
2. Walk me through, at the syscall level, what happens when your daemon opens `/proc/net/tcp`.
3. Four failed attempts at t=0, a fifth at t=61s, window is 60s — detection or not? Justify from your actual window semantics.
4. journald is configured volatile (no disk persistence) and the box reboots mid-attack — what state do you lose, and does the daemon handle recovery?
5. How does the daemon distinguish a legitimate service restart opening a new port from an actual backdoor listener? What's your false-positive reasoning?
6. Show me the nftables chain your daemon creates — why a dedicated chain instead of modifying `INPUT` directly?
7. Two brute-force sources hit simultaneously — could there be a race condition in rule insertion? Show me you've thought about it.
8. If someone gets a shell as the unprivileged user this daemon runs as, what's the blast radius — what can they not do that root could?
9. Your permission-drift baseline snapshot happens at startup — if a setuid binary is added five seconds into initialization, before the baseline finishes, do you catch it? How do you know?
10. Walk through `SIGHUP` end to end: from `kill -HUP <pid>` to reloaded config in your code — why not just restart the service instead?
11. Why nftables over iptables here, concretely — name the specific feature you're actually relying on, not "it's newer."
12. Theory names `CAP_NET_BIND_SERVICE` and `CAP_SYS_PTRACE` as the classic examples of "root isn't monolithic" — why does `sentineld` need neither of those, and `CAP_NET_ADMIN` instead? What would you need to add if a future version had to bind a low port itself?
13. Your cron/timer auditor snapshots at startup — walk me through exactly where you read state from for: root's crontab, a regular user's crontab, `/etc/cron.d/`, and systemd timers. What about an `at` job — would your current design catch that, and if not, is that an acceptable documented gap or a real hole?
14. I add a new file under `/etc/cron.d/` while the daemon is running — show me the detection happen live, and explain why you're diffing against a startup baseline instead of re-reading the baseline file every cycle.

**Test / edge cases**

- [ ] 4 failed attempts spaced 20s apart, then a 5th at second 61 from the first: correctly NOT flagged per your defined window.
- [ ] 5 failed attempts within 45 seconds, same IP: flagged and blocked.
- [ ] A successful login interleaved among failures from the same IP: your reset-or-not behavior is explicit and justified.
- [ ] IPv6 source addresses throughout the log: parsed correctly, never dropped silently.
- [ ] Log rotation or journald restart mid-run: window state isn't corrupted, daemon doesn't crash.
- [ ] New process binds an unallowlisted port while running: detected within your defined polling interval.
- [ ] A listening process whose parent is `cron` rather than an allow-listed service manager: flagged via the PPID-ancestry check inherited from Exercise 02.
- [ ] setuid bit added to a normally clean binary during runtime: caught on next scan cycle.
- [ ] A new entry added to a regular (non-root) user's crontab mid-run: detected on the next scan cycle.
- [ ] A new file dropped into `/etc/cron.d/` mid-run: detected on the next scan cycle.
- [ ] A systemd timer unit enabled mid-run: detected on the next scan cycle.
- [ ] A cron entry removed and immediately re-added with identical content: your drift detector's behavior on this (silent, since state matches baseline again, or logged as a transient event) is explicit and justified.
- [ ] nftables rule expiry: blocked IP is provably reachable again once TTL elapses.
- [ ] `SIGHUP` arrives mid-write to the audit log: no corruption, no lost in-flight event.
- [ ] Malformed/truncated log line: parser doesn't crash.
- [ ] Daemon started with an impossible capability request: fails loudly with a clear error, no silent degradation.
- [ ] Two instances started at once: no duplicate nftables rules, no corrupted shared state.
