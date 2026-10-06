---
title: "Secure Code Review Methodology"
description: "Everything in this roadmap so far has been black-box: you found the bug by attacking it."
---
# Secure Code Review Methodology

*Stage 2: Hands-On Web Security and Code Review · Subject 5 of 7 · Full depth subject*

> Everything in this roadmap so far has been black-box: you found the bug by attacking it. This subject flips the vantage point — given the source, find the same bug classes faster, more completely, and with a fix you can propose in the same pull request.

## What you will build

- **Exercise 00 — reviewchecklist0.** Description **Description.** A personal, source-mapped code-review checklist: for every vulnerability class covered in Stages 0-2 so far, the exact source-code pattern that indicates risk, in the language(s) you review most.
- **Exercise 01 — dataflowtrace0.** Description **Description.** A single, complete, hand-traced data flow through a real multi-file application: from the exact line where user input enters, through every function it passes through, to the exact sink where it's used — with every intermediate transformation and every missed (or present) sanitization step documented.
- **Exercise 02 — fullaudit0.** Description **Description.** A full, line-numbered, checklist-driven manual audit of a real deliberately-vulnerable open-source application's source, producing a professional vulnerability report with every finding's exact location, root cause, and fix.
- **Capstone — diffreview.** Description **Description.** A differential code reviewer: given a git diff (a pull request), applies your Exercise 00 checklist patterns specifically to the changed lines and their immediate data-flow neighborhood, reporting only what the diff newly introduces or newly fixes — the actual shape of code review inside a real engineering team, where nobody re-audits the whole codebase on every commi…

## In this chapter

- [Lessons](lessons/index.md): what I wrote while studying this subject, in the order I wrote it
- [The Subject](subject.md): the full specification, with mandatory, forbidden and bonus parts per exercise, a capstone and defense questions

## Status

<!-- status:start -->
**Planned.** 0 lesson(s) and 0 solution(s) published.

Not started yet. Follow the repository to be notified when this chapter begins.
<!-- status:end -->

## Order

Recommended after [File Handling Vulnerabilities and Cloud SSRF](../04-file-handling-cloud-ssrf/index.md).
