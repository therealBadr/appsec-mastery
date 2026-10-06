---
title: "The Subject"
description: "Cross the line from \"I wrote C that ran\" to \"I know exactly what the kernel and the loader did with the bytes I wrote\" — memory layout, syscalls, the dyna…"
---
# OS Internals: The Subject

*Subject 4 of 6 — Foundations Reset · Version 1.0 — September 2026*

> Cross the line from "I wrote C that ran" to "I know exactly what the kernel and the loader did with the bytes I wrote" — memory layout, syscalls, the dynamic linker, and the exact mechanics that turn a bounds-checking mistake into a hijacked return address.

## Chapter 00 — Foreword

> *A buffer overflow is not a bug in your program. It is your program's memory obeying physics your mental model never accounted for.*

Software engineering trains you to think in variables, functions, and types. None of that exists at runtime — there is only a flat address space, a stack that grows down, a heap that grows up, and a return address sitting exactly where an attacker wants it. This subject rebuilds that ground-truth model from raw observation, not from a diagram in a textbook.

## Chapter I — Introduction

You will observe your own process's memory layout directly, trace syscalls with `strace`, deliberately overflow a stack buffer and find the overwritten return address in GDB, and build an `LD_PRELOAD` shim that instruments allocation calls in a running process you do not control the source of. The capstone forces all of it into one artifact: a memory-safety triage tool that classifies a crash the way a security engineer would on day one of an incident.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input, an unreachable host, or unexpected data. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline), applies to every exercise.** Functions do one thing and are named for what they do. No magic numbers — ports, offsets, thresholds, and protocol constants are named constants, never bare literals. No block of code you cannot explain, unprompted, line by line, during defense. Every non-obvious line carries a comment explaining why, not what.

**II.3** **Evidence, not assertions.** Every claim of the form "this detects X" or "this parses Y correctly" must be backed by a reproducible capture, transcript, or log — captured in your turn-in. Assertions without evidence are treated as unmet requirements during defense.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct. A single mandatory-part flaw — even a minor one — zeroes the bonus evaluation for that exercise, no exceptions.

**II.5** **Evaluation environment.** A Linux VM or container with ASLR togglable, GDB, GCC, and `strace` installed. Disabling ASLR system-wide for demonstration purposes is expected and must be re-enabled and noted afterward.

**II.6** **Scope.** Every vulnerable binary in this subject is one you wrote or were given explicitly for this exercise. None of this authorizes probing memory-safety bugs in software you don't own or a CTF you weren't invited to.

## Chapter III — Mandatory Part

### Exercise 00 — memmap0

- **Turn-in dir:** os_internals/ex00/
- **Files:** memmap0.c, README.md, evidence/
- **Allowed:** C, gcc, /proc/self/maps
- **Forbidden:** any memory-introspection library

**Description.** A C program that prints the runtime address of a stack variable, a heap allocation, a global variable, a function pointer, and an environment variable, then reads and annotates its own `/proc/self/maps` — with and without ASLR — to show the layout matches reality, not just the textbook diagram.

!!! success "Mandatory"

    - Prints, in one run: the address of a local (stack) variable, a `malloc()`'d block (heap), a global variable (BSS/data depending on initialization), the address of a function you wrote (text segment), and the address of an environment variable accessed via `environ`.
    - Cross-references each printed address against the corresponding region in `/proc/self/maps`, read and parsed by your own code, labeling which mapped region each address falls in.
    - Run twice with ASLR enabled and twice with it disabled (`echo 0 > /proc/sys/kernel/randomize_va_space`, restored after), capturing all four runs as evidence, with a written explanation of exactly which regions move between runs and which stay fixed even with ASLR off (and why).
    - A written explanation of why the heap sits above the BSS/data segment and grows upward while the stack sits near the top of the user address space and grows downward, and what security consequence follows from a stack overflow versus a heap overflow given that layout.

!!! failure "Forbidden"

    - Any address-introspection library instead of your own pointer-printing and `/proc/self/maps` parsing.
    - Leaving ASLR disabled on the system after the exercise.
    - Asserting the stack/heap growth direction from memory instead of demonstrating it with printed addresses across multiple calls.

!!! note "Norm"

    See §II.2, plus: one function per memory-region demonstration; `/proc/self/maps` parsing isolated in its own function with named field offsets.

!!! tip "Bonus"

    Demonstrate and explain stack-canary placement (`-fstack-protector`) by comparing disassembly with and without the flag.

### Exercise 01 — straceit

- **Turn-in dir:** os_internals/ex01/
- **Files:** REPORT.md, traces/
- **Allowed:** strace, any program you choose to trace
- **Forbidden:** ltrace as a substitute (may be used supplementally, not as your primary evidence)

**Description.** Trace five different programs with `strace`, and produce a report that reads each trace like a security engineer doing triage — not a transcript with no interpretation.

!!! success "Mandatory"

    - Trace at least: `ls`, `curl` against a real URL, your own compiled webserv/HTTP binary from Exercise 00 of HTTP Internals (or any C network program you've written), `ssh` connecting to a host, and `python3 -c "..."` running a short script that opens a file and a socket.
    - For each trace, identify and annotate: every file opened (`openat`) and whether it plausibly should have been, every network syscall (`socket`/`connect`/`sendto`) and the destination, and every process-spawning syscall (`execve`/`fork`/`clone`) if present.
    - For the network-facing programs, identify the exact syscall sequence of a TCP connection setup (socket → connect, or socket → bind → listen → accept) and map it back to the three-way handshake from Networking Depth.
    - A written section: "if this program's behavior were unexpected for its name" — pick one trace and describe, concretely, what a suspicious deviation would look like (e.g. `ls` making a network connection) and why that's exactly the signal a syscall-monitoring EDR looks for.

!!! failure "Forbidden"

    - Pasting raw strace output with no annotation or interpretation.
    - Skipping a trace because "it's obvious what it does."

!!! note "Norm"

    See §II.2, plus: one section per trace, consistent structure (command → annotated excerpt → interpretation).

!!! tip "Bonus"

    Use `strace -c` to produce a syscall-frequency summary for one long-running program and explain what the distribution tells you about its workload.

### Exercise 02 — stackoverflow0

- **Turn-in dir:** os_internals/ex02/
- **Files:** vuln.c, exploit_notes.md, evidence/
- **Allowed:** C, gcc (with protections disabled for the demo), gdb
- **Forbidden:** existing exploit-development frameworks (pwntools may be used only for the bonus, not the mandatory GDB walkthrough)

**Description.** A deliberately vulnerable C program with a stack buffer overflow, compiled with protections off, exploited far enough in GDB to overwrite the saved return address and prove it — plus a written explanation of exactly why each disabled protection was necessary to get there.

!!! success "Mandatory"

    - A minimal vulnerable program using an unbounded copy (e.g. `gets()` or `strcpy` with attacker-controlled length) into a fixed stack buffer, compiled with `-fno-stack-protector -z execstack -no-pie` and ASLR disabled for the demo, with every disabled protection listed and justified in writing (what it would otherwise have stopped).
    - In GDB: set a breakpoint at function entry, show the stack frame layout (buffer, saved base pointer, saved return address) via `x/` examine commands, then supply an input long enough to overwrite the saved return address with a recognizable marker value, and show the corrupted return address in the register/stack dump before the function returns.
    - Show the program crashing (SIGSEGV) when the overwritten "return address" is not a valid mapped address, and explain in writing what the next step toward a working exploit would be (redirecting to a known address, e.g. shellcode or a ROP gadget) without necessarily completing it.
    - A written, precise explanation of the exact offset (in bytes) from the start of your input to the start of the saved return address, and how you determined it (e.g. a cyclic/De Bruijn pattern or manual calculation from the struct layout) — not a number you guessed and got lucky with.

!!! failure "Forbidden"

    - Attacking any binary other than one you wrote for this exercise.
    - Leaving compiled vulnerable binaries or protection-disabling flags in any shared/production environment.
    - Asserting the offset without showing the derivation.

!!! note "Norm"

    See §II.2, plus: the vulnerable function isolated and minimal, no unrelated code obscuring the stack frame.

!!! tip "Bonus"

    With ASLR and the stack canary re-enabled one at a time, show the exploit failing against each individually and explain precisely what detects/blocks it in each case (canary check on return vs. address-space unpredictability).

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** the full memory layout model (to recognize which region a faulting address falls in), syscall-level observation (to see what the process was doing right before the crash), the mechanics of stack overflows from Exercise 02 (to recognize the signature of a smashed return address versus a wild pointer), and the `LD_PRELOAD`/dynamic-linking model (to instrument allocations without source access) — all at once, automatically, on an input the tool has never seen. Someone who only knows GDB can triage one crash manually; this tool has to encode the reasoning a human would use into rules that work on a crash the author didn't hand-pick.

### Capstone — crashtriage

- **Turn-in dir:** os_internals/capstone/
- **Files:** src/, samples/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A triage tool that takes a crashing binary plus a crashing input, runs it under GDB in batch mode, and automatically classifies the crash — stack overflow vs. heap corruption vs. null-deref vs. something else — the way a security engineer's first fifteen minutes on a fuzzer-found crash actually goes, including a syscall-trace and LD_PRELOAD-based allocation-tracking module for the heap cases.

!!! success "Mandatory"

    - Given a target binary and a crashing input file, runs the binary under GDB in batch/script mode (no manual interaction), captures the signal, the faulting instruction, and the register state at crash time.
    - Classifies the crash into one of: stack-buffer-overflow (return address or saved frame pointer corrupted with attacker-influenced bytes — verify by checking whether crash-time stack bytes match the input), null-pointer-dereference (faulting address is near zero), wild-pointer/heap-corruption (faulting address is a plausible heap address but not matching the input directly), or unclassified — never silently guessing.
    - For binaries linked dynamically, uses an `LD_PRELOAD` shim (built for this capstone, not copied) that logs every `malloc`/`free` call with size and pointer, so a heap-corruption classification can additionally report the allocation history leading up to the crash.
    - Runs the target once under `strace` alongside the GDB run and includes the last N syscalls before the crash in its report, to distinguish "crashed while processing network input" from "crashed on startup" from "crashed handling a file."
    - Produces one structured report per crash: classification, confidence reasoning (which specific evidence supports the classification), faulting address and instruction, relevant register/stack state, and (for heap cases) the allocation history.
    - Demonstrated against at least four different crashing inputs you produce: one clean stack-overflow (reusing/extending Exercise 02's vulnerable binary), one null-pointer-dereference, one heap-based corruption (a simple use-after-free or double-free you write for this purpose), and one crash that your tool correctly reports as unclassified rather than guessing wrong.

!!! failure "Forbidden"

    - AFL, libFuzzer, or any existing fuzzer/triage tool doing the classification for you — you may use one to \*find\* an interesting crash for testing, never to classify it.
    - GDB's own `exploitable`/`exploitable.py` plugin as your classification engine — read it for ideas, do not depend on it.
    - Guessing a classification when the evidence is ambiguous instead of reporting "unclassified" with the evidence shown.
    - Silently failing on a statically-linked binary instead of explicitly reporting that the `LD_PRELOAD` module could not attach and why.

!!! note "Norm"

    See §II.2, plus: GDB-driving, syscall-tracing, allocation-tracking, and classification each in their own module, with a single dispatcher; classification heuristics as named, documented functions, not one giant conditional.

!!! tip "Bonus (§II.7)"

    Extend classification to detect a likely format-string vulnerability (crash pattern consistent with attacker-controlled format specifiers); a minimal report-to-HTML renderer.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
os_internals/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live from a clean terminal on your VM/container. For Exercise 02 and the capstone, the evaluator may supply an additional crashing input built from a variant of your own vulnerable programs, and expects either a correct classification or an honest "unclassified" — a confident wrong answer is a failure regardless of how the rest of the demo went.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — memmap0

**Defense questions**

1. Show me your four captures — which addresses moved between ASLR-on runs and which didn't, and why?
2. Why does a heap overflow typically corrupt allocator metadata rather than a return address directly — what does that metadata corruption actually let an attacker eventually achieve?
3. Point to a line in `/proc/self/maps` and tell me exactly what's mapped there and why it has those permission bits.
4. What specifically does PIE (position-independent executables) add on top of stack/heap ASLR?

### A.1 — straceit

**Defense questions**

1. Pick a trace at random from your report — walk me through five consecutive syscalls without looking at your annotations first.
2. What's the difference between `fork()`+`execve()` and `vfork()`, and why would an attacker analyzing a sandboxed process care about which one is used?
3. Show me the exact syscalls corresponding to a TCP handshake in your network trace and map each one to a packet you'd see in Wireshark.
4. What would a syscall trace of a program doing something it has no business doing (e.g., a calculator reading `/etc/shadow`) look like, concretely, in this same format?

### A.2 — stackoverflow0

**Defense questions**

1. Show me your offset calculation live — derive it in front of me, don't read it from your notes.
2. Walk me through the stack frame in GDB right before the overflow and right after — point to the exact bytes that changed.
3. If I re-enable the stack canary only, what specifically breaks in your exploit and where does the program detect the corruption?
4. If I re-enable ASLR only, what specifically breaks, and why does a stack-only overflow with no info leak become far harder?
5. Why does `execstack` matter here even though you're not executing shellcode yet — what would the next step need it for?

### A.3 — Capstone: crashtriage

**Defense questions**

1. Run your tool live against a crash I hand you — narrate its classification reasoning as it runs.
2. Show me the exact evidence your stack-overflow classifier checks for, and explain a case where that evidence could be misleading (a false positive).
3. Walk through your `LD_PRELOAD` shim — why does it need to preserve the real `malloc`/`free` behavior exactly, not just log and no-op?
4. What does your tool do differently for a statically-linked binary, and why can't `LD_PRELOAD` help there?
5. Give me a crash your tool correctly refuses to classify — walk through why the evidence was genuinely ambiguous.
6. How does the syscall trace change your confidence in a classification — give a concrete example from your four demonstrated crashes.

**Test / edge cases**

- [ ] Statically-linked crashing binary: `LD_PRELOAD` module explicitly reported as inapplicable, tool does not crash or silently skip the whole report.
- [ ] A crash with a completely garbage/unmapped faulting address (wild jump): classified with low confidence and evidence shown, not force-fit into a category.
- [ ] A crashing input that does not actually crash on this run (a timing-dependent bug): reported as "did not reproduce," not a false classification.
- [ ] A binary that catches SIGSEGV itself via a signal handler: GDB still intercepts and reports correctly, or the limitation is explicitly documented.
- [ ] Multiple threads, one of which crashes: correct thread's register state reported, not thread 0 by default if thread 0 didn't crash.
- [ ] A heap corruption where the allocation log shows a clean double-free (same pointer freed twice): classified specifically as double-free, not generic heap corruption.
- [ ] An input file that is empty or zero bytes: tool reports "no crash" or "invalid input," never hangs.
- [ ] GDB itself failing to attach (e.g. permissions): reported clearly as a tool-environment failure, distinct from a crash-classification failure.
