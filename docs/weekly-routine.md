---
title: "Weekly Study Routine"
description: "The 42 subjects have no weeks or months attached on purpose — a stage ends when you clear its exit gate, not on a date."
---
# Weekly Study Routine

> The 42 subjects have no weeks or months attached on purpose — a stage ends when you clear its exit gate, not on a date. This document is the missing piece: how to structure the hours you actually have, around a full-time job, so that time consistently turns into cleared exit gates instead of scattered effort. It assumes roughly 12-18 hours a week of deep, undistracted study/build time — adjust the block counts, not the block types, if your real number is different.

## Foreword

> *Three hours building a tool beats three hours watching a course. Ask at the end of every session: what did I produce?*

That rule, carried over directly from the roadmap itself, is the organizing principle of this entire document. Every block type below produces something — a working exploit, a fixed bug, a note file, a writeup, a flag — because the roadmap's own diagnosis of failure isn't lack of intelligence, it's people who stop producing when it gets hard and call the stopping "studying."

## Chapter I — The Weekly Time Budget

Working full-time changes the shape of a study plan more than it changes the total hours available — the failure mode isn't usually "not enough time," it's long, unscheduled weekend binges that produce a burst of progress followed by a week of nothing. A weekday/weekend split, held consistently, beats an ambitious plan abandoned by week three.

- **Weeknights (Mon-Fri):** 1-2 focused hours after work, 4-5 nights a week. Short enough to actually happen consistently; long enough to finish one real unit of work (one exercise, one tool feature, one lab machine).
- **Weekend:** One longer 3-5 hour deep block, once a week — reserved for capstones, full-audit exercises, and anything that doesn't fit cleanly into a weeknight interruption.
- **Buffer:** Deliberately unscheduled. A week that runs long on a hard exercise borrows from this, not from sleep or from next week's plan.
- **Minimum viable week:** If a week genuinely only allows 4-5 hours total, protect the note-taking and review blocks first — they're what keeps a slow week from becoming a forgotten one.

## Chapter II — The Five Block Types

Every study session is exactly one of these five things. Naming the type before you sit down (not mid-session) is what keeps a "study block" from quietly turning into passive video-watching — the roadmap's single most-named failure mode.

### 1. Build — the roadmap's core unit of work

Writing code against a subject's mandatory-part checklist: an exercise, a capstone module, a fix verified against your own exploit. This is where most weeknight and all weekend-deep-block hours go.

- Start every build session by re-reading the exercise's Mandatory/Forbidden blocks — not from memory
- End every session with something that runs, even if incomplete — a half-finished function you can resume beats a mental model you have to reconstruct next time

### 2. Lab — applying a cleared subject against a new target

PortSwigger Academy labs, HackTheBox machines, a CTF challenge, or DVWA/Juice Shop at a harder setting — deliberately different targets from the ones a subject's own exercises used, so the skill being tested is transfer, not memorized steps against one known app.

- One lab machine or 2-3 PortSwigger labs per weeknight block is a sustainable pace
- A lab that stumps you for a full session is not wasted time if you write down exactly where you got stuck (see Chapter IV)

### 3. Notes and Writeups — every session, not a separate week

The roadmap's own rule: "every lab session ends with documentation... nothing written means nothing learned." This isn't a distinct block so much as the last 10-15 minutes of every Build and Lab block — protect that time explicitly rather than letting a session run long and eat it.

- A lab writeup: objective, environment, steps taken, what failed, root cause, fix, lesson
- A wiki entry: topic → concept → how it works → why it matters for security → example → resources — never copy-pasted, always rewritten in your own words

### 4. Review — scheduled, not incidental

Revisiting a cleared subject's exit gate cold, re-reading old notes, or re-running an old capstone against a fresh target — the block type most people cut first under time pressure, and the one whose absence produces the "I passed this six months ago but can't explain it now" failure the roadmap warns against directly.

- Not new material — the point is retention, not progress
- See Chapter V for a concrete spaced-repetition cadence

### 5. Portfolio — Stage 2 onward

Publishing a tool, polishing a writeup for external readers, submitting a bug bounty report, or working a Stage 4-5 output — distinct from Build because the bar here is "a stranger could use/read this," not "it passed my own exercise's defense."

- Batch this into the weekend deep block — it rarely fits well into a 90-minute weeknight slot
- One portfolio session every 2-3 weeks keeps the "build order" from the roadmap's own portfolio strategy actually moving

## Chapter III — A Sample Week

A template, not a mandate — the block *types* and their rough proportion matter far more than which exact evening each one lands on. Adjust freely around your actual schedule.

| Day | Block | Focus |
|---|---|---|
| Mon | Build (1.5h) | Current subject's next exercise, from a cold read of the Mandatory block |
| Tue | Build (1.5h) | Continue same exercise, or start the write-up if it's done |
| Wed | Lab (1.5h) | 2-3 PortSwigger labs or one HTB machine in the current topic area |
| Thu | Review (1h) | Re-derive one earlier exit-gate item cold, no notes, then check yourself against the original |
| Fri | Build (1h) or rest | Light session or a full skip — protect the weekend block by not arriving depleted |
| Sat | Deep block (3-5h) | Capstone work, a full-audit exercise, or a Portfolio session |
| Sun | Notes + plan (1h) | Finish any open writeups; pick next week's exercise and lab targets in advance, not Monday morning |

## Chapter IV — Note-Taking System

The roadmap specifies the structure; this section is how to actually run it week to week without the wiki turning into an unmaintained pile.

!!! success "Two note types, kept separate"

    - **The wiki** (Obsidian, Notion, or plain markdown in a git repo) — durable, reference-shaped knowledge: topic → concept → how it works → why it matters for security → example → commands/resources. One page per concept, cross-linked. This is what you re-read during Review blocks.
    - **The lab log** — one markdown file per lab/exercise session: objective, environment setup, steps taken (with real commands), what worked, what failed, root cause, fix, lessons learned. This is raw material; your strongest entries later become blog posts (Professional Security Writing).

!!! success "Weekly wiki maintenance (10 minutes, during the Sunday Notes+Plan block)"

    - Fold this week's lab-log lessons into the relevant wiki pages — a lab log that never gets distilled into the wiki produces notes nobody re-reads
    - Flag any wiki page you couldn't explain cleanly this week for extra attention in next week's Review block

## Chapter V — Spaced Review and Retention

A cleared exit gate is not a permanent state — the same "if you can't teach it, you don't know it yet" standard applies to material from three months ago as much as to what you learned yesterday. A lightweight, fixed cadence prevents the earliest, most foundational subjects (the ones every later capstone assumes) from quietly eroding while attention moves forward.

- **+1 week:** Re-attempt the exercise's hardest defense question cold. If it's shaky, that subject's wiki pages get priority in this week's Review block.
- **+1 month:** Re-run one capstone tool against a fresh target you haven't used before. A tool that still works and a defense you can still give cleanly is real retention; anything else is a signal, not a failure.
- **+3 months:** Re-read the subject's Common Delusions/exit gate cold, end to end, no notes. This is the check that catches "I passed it once" quietly decaying into "I used to know this."
- **Ongoing:** Every new Stage 1+ subject that explicitly reuses an earlier subject's technique (most of them do — see each subject's synthesis notes) is itself free spaced review of the thing it's reusing.

## Chapter VI — The Weekly Self-Audit

Five minutes, same time every week (the Sunday Notes+Plan block is the natural home for it), answering the roadmap's own review questions honestly rather than rhetorically.

!!! success "Ask every week, in writing"

    - What did I try this week? What worked, what didn't?
    - What's the actual gap between where I am and what the current subject's exit gate requires?
    - If I'm behind where I expected, why — and what changes next week, specifically (not "try harder")?
    - What did I produce this week that I could show someone? If the honest answer is nothing, what block type got skipped, and why?
    - Is there a topic I've been quietly avoiding because it's uncomfortable rather than because it's genuinely lower priority?

!!! warning "Note"

    **This audit is diagnostic, not punitive.** Its only job is catching drift early — a rough week answered honestly and adjusted for is a working system; a rough week skipped or rationalized away is how weeks turn into months with no forward motion, which the roadmap names directly as the actual reason most people who fail at this stop.

## Chapter VII — CTF and Lab Rotation

CTFs and standalone lab machines are Lab-block material, not a separate hobby competing with the roadmap — the roadmap's own warning against "random CTF addiction without depth" means rotation should be deliberate, tied to what the current stage is actually building, not opportunistic flag-chasing.

- **Stage 0-1:** PicoCTF and early HackTheBox "Starting Point" machines — fundamentals-heavy, forgiving difficulty curve while Stage 0-1's core vocabulary is still forming.
- **Stage 2:** PortSwigger Academy (mandatory, per the roadmap) as the primary rotation, supplemented by 20+ HackTheBox web-focused machines and 20+ web CTF challenges, exactly as the roadmap's Stage 2 practical outputs specify.
- **Stage 3-4:** HackTheBox Pro Labs (multi-host, closer to a real engagement) and live-scope bug bounty programs replace single-flag CTFs as the primary target — the skill being trained shifts from "find the flag" to "run a full methodology."
- **Always:** Depth over breadth: the roadmap's own standard is "50 web challenges fully understood beats 500 shallow flags." A CTF write-up that doesn't survive a Review-block re-explanation wasn't actually understood the first time.

## Chapter VIII — Sustainability and the Discipline Gap

The roadmap's closing line about itself is worth repeating here specifically because a weekly routine is where it either becomes true or doesn't: *the discipline gap is larger than the knowledge gap, and most people who fail at this stop when it gets hard, not because they lack intelligence.* A routine's entire job is making the hard weeks survivable without becoming quitting weeks.

!!! success "What actually protects consistency, in practice"

    - A minimum viable week (Chapter I) that's genuinely achievable even when work/life is heavy — a small consistent week beats an ambitious plan abandoned entirely
    - Treating a stuck lab or a failed defense-question rehearsal as data for the weekly self-audit, not a verdict on your ability — the roadmap's own "fail forward" rule
    - Protecting the Sunday Notes+Plan block above almost everything else — a week that starts without a picked target drifts into passive consumption by Tuesday
    - Remembering this roadmap has no weeks or months attached on purpose — a slower week is not falling behind a schedule that was never real to begin with; it's just a slower week
