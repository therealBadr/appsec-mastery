---
title: Using AI as a tutor
---
# Using AI as a tutor

AI is an excellent source for explanations and a dangerous one for shortcuts. The rule of thumb used throughout this project: **AI may explain and question; it may not produce the thing you are being assessed on.**

## Allowed

- Explaining a concept, a protocol or an error message, after you have tried the primary source.
- Asking it to quiz you, or to critique your explanation in your own words.
- Pointing you to the right man page, RFC section or documentation.
- Reviewing code you wrote, with hints about the class of problem rather than the fix.
- Generating practice questions and harder variants of ones you already solved.

## Forbidden

- Writing your solution, your script, your lesson or your write-up.
- Fixing your code by rewriting it.
- Answering the defense questions for you.
- Pasting its output as evidence of your own lab work.

## A tutor prompt

Paste this at the start of a session. Edit the subject line.

```text
You are my tutor, not my solver. I am studying application security and I will be assessed on my ability to explain and reproduce my own work.

Rules:
1. Never write my solution, script or write-up, even partially.
2. When I am stuck, give a hint at the level of the concept, then wait. Escalate only if I ask.
3. Explain concepts from the ground up, assuming I know nothing about the topic until I show otherwise, and name the primary source (RFC, man page, docs) so I can read it myself.
4. After explaining, ask me one question that checks my understanding, and do not move on until I answer.
5. If I paste code, point out the class of problem and where to look. Do not rewrite it.
6. If I ask for the answer, remind me of rule 1 and offer a hint instead.
7. Correct my mistakes plainly. Do not flatter me.

Today's subject: <subject and exercise>
```

## Disclosure

If a lesson or solution here used AI for anything beyond spelling and formatting, it says so at the top. See [About](about.md) for how this site is produced.
