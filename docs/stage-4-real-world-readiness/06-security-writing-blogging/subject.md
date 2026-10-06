---
title: "The Subject"
description: "The closing Stage 4 subject, and the one that turns everything else in this roadmap into something a hiring manager or a client can find, read, and be con…"
---
# Professional Security Writing and Blogging: The Subject

*Subject 6 of 6 — Real-World Readiness and Portfolio · Version 1.0 — September 2026*

> The closing Stage 4 subject, and the one that turns everything else in this roadmap into something a hiring manager or a client can find, read, and be convinced by — the roadmap's own portfolio strategy names a minimum of 15 posts of real technical depth, hosted on your own domain, as the actual finish line.

## Foreword

> *A writeup that narrates tool commands with no analysis looks like fake portfolio padding to anyone technical enough to hire you. A writeup that explains root cause is the single most reliable signal that you actually understand what you did.*

## Why This Subject

This roadmap has generated an enormous amount of writing material already — every exercise's writeup, every capstone's evidence trail, every CVE reproduction's analysis — this subject is specifically about the craft of turning that raw material into public, well-structured technical writing that builds a reputation instead of just documenting completion.

## What You Must Understand

### What separates a real writeup from a walkthrough

The single most repeated distinction across this entire roadmap's capstones: a walkthrough narrates steps ("I clicked here, then here"); a real writeup explains root cause, why the vulnerability class exists, and what an attacker actually achieves — the same standard every DVWA/PortSwigger/CVE writeup in this roadmap has already been held to.

- Structure that works consistently: concept/context → vulnerability → root cause → exploitation → fix → broader lesson
- A reader should walk away understanding the vulnerability *class*, not just this one instance of it — exactly the transferable-pattern standard from Secure Code Review's checklist work

### Choosing what to write about

The roadmap's own material is the deepest available source: a Stage 1-2 exercise's root-cause explanation, a CVE reproduction's independent analysis, a tool's design rationale, or an original synthesis connecting two vulnerability classes you noticed while building a capstone.

- Original synthesis (a pattern you noticed connecting, say, SSRF and XXE's shared "borrows server capability" shape) is rarer and more valuable than another walkthrough of a well-known CVE
- Writing immediately after finishing a subject, while the reasoning is fresh, produces sharper root-cause explanations than reconstructing it weeks later

### Publishing infrastructure

A self-hosted or self-owned-domain blog (not only a platform-hosted profile) signals ownership and permanence — the roadmap explicitly calls out considering bilingual (English/French) publishing to open both the English-speaking and Francophone African/French consulting markets.

- A static site generator (Hugo, Jekyll, or similar) hosted cheaply, with your own domain, is a lightweight, durable setup requiring minimal ongoing maintenance
- Cross-posting to a platform like Medium/dev.to for reach while keeping the canonical version on your own domain gets you both discoverability and ownership

### Technical writing craft

Concrete, learnable habits: real screenshots/output over descriptions of what you saw, code blocks that are actually copy-paste-runnable, a consistent voice, and editing for the reader's time — most technical readers skim first and only commit to a full read if the opening paragraph earns it.

- An opening paragraph that states the vulnerability class and impact immediately (not buried after three paragraphs of setup) respects a skimming reader
- Every code snippet tested to actually run as shown — a broken copy-paste example undermines credibility instantly

## Practical Outputs

!!! success "Practical outputs"

    - A published personal blog on your own domain, with at least 15 posts of genuine technical depth — reusing and substantially rewriting (never merely reposting) your strongest exercise writeups, CVE reproductions, and tool-design rationale from across this entire roadmap.
    - At least 3 posts representing original synthesis (a pattern or connection across vulnerability classes) rather than a single exercise's writeup, demonstrating the transferable, teach-it-forward understanding this roadmap has emphasized throughout.
    - A consistent structural template applied across all posts, refined from at least one round of self-editing against the "walkthrough vs. real writeup" standard.
    - A bilingual pilot: at least one post published in both English and French, with a written note on what the translation process taught you about explaining the same technical concept to two different audiences.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "I'll write it all up at the end, once I have enough material." Writing immediately after each piece of work, while the reasoning is fresh, consistently produces better root-cause explanations than a bulk retrospective effort.
    - "A walkthrough is basically a writeup." The roadmap has drawn this line explicitly and repeatedly — a technical reader (and a hiring manager) can tell the difference immediately, and it's the single fastest way a portfolio reads as padding instead of substance.
    - "Nobody reads security blogs from beginners." A well-written root-cause explanation of a real vulnerability class is valuable regardless of the author's seniority — clarity and correctness matter more than credentials for this specific kind of writing.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Take one of your own existing exercise writeups and revise it live against the walkthrough-vs-real-writeup standard, narrating each change.
    - Explain your blog's publishing infrastructure choice and what tradeoff you made.
    - Present one piece of original synthesis writing and defend why the pattern you identified is real and useful, not superficial.
    - Read an unfamiliar draft writeup (the evaluator's) and critique it against the same standard you've applied to your own work.
