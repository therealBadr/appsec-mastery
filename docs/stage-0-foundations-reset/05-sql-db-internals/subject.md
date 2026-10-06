---
title: "The Subject"
description: "Go under the ORM and the ?"
---
# SQL and Database Internals: The Subject

*Subject 5 of 6 — Foundations Reset · Version 1.0 — September 2026*

> Go under the ORM and the ? placeholder to where a query actually becomes a parse tree — because SQL injection is not a list of payloads to memorize, it is what happens when user input crosses from data into syntax at parse time.

## Chapter 00 — Foreword

> *A parameterized query is not "safer SQL." It is a different message to the database entirely — data and syntax sent on separate channels instead of concatenated into one string and hoped over.*

Every SQL injection tutorial teaches payloads. Almost none teach why a payload works: that a database driver tokenizes and parses a query string before it ever looks at a value, and that string concatenation lets attacker input rewrite the parse tree itself. Once you've seen that mechanism directly, injection stops being a list of tricks and becomes one idea applied everywhere data crosses into syntax — not just SQL.

## Chapter I — Introduction

You will stand up a real vulnerable login query and break it by hand — no SQLMap — then extract an entire schema through UNION injection, rewrite every vulnerable query as a parameterized one and prove the fix holds against your own exploit, and end by building a tool that demonstrates blind boolean and time-based extraction, the techniques that work even when the application shows you nothing.

## Chapter II — General Instructions

**II.1** **Crash policy.** Your programs must never crash, hang indefinitely, or exit uncleanly on malformed input, an unreachable host, or unexpected data. Any behavior not explicitly specified is undefined behavior — free to do anything *except* crash, hang, or corrupt state.

**II.2** **Norm (code-quality baseline), applies to every exercise.** Functions do one thing and are named for what they do. No magic numbers — ports, offsets, thresholds, and protocol constants are named constants, never bare literals. No block of code you cannot explain, unprompted, line by line, during defense. Every non-obvious line carries a comment explaining why, not what.

**II.3** **Evidence, not assertions.** Every claim of the form "this detects X" or "this parses Y correctly" must be backed by a reproducible capture, transcript, or log — captured in your turn-in. Assertions without evidence are treated as unmet requirements during defense.

**II.4** **Bonus rule.** Bonus parts are evaluated only if the mandatory part is 100% functional and correct. A single mandatory-part flaw — even a minor one — zeroes the bonus evaluation for that exercise, no exceptions.

**II.5** **Scope.** Every target in this subject is a database and application you stood up yourself (MySQL/PostgreSQL/SQLite behind a small app you write or a deliberately vulnerable app like DVWA). None of this is authorized against a third party's database, ever, under any framing.

**II.6** **Global forbidden list.** SQLMap, or any automated injection tool, is forbidden for every exercise's mandatory part. You are building the understanding SQLMap automates; reading its source for technique ideas is allowed.

## Chapter III — Mandatory Part

### Exercise 00 — manualsqli0

- **Turn-in dir:** sql_db_internals/ex00/
- **Files:** login_vuln.py, EXPLOIT.md, evidence/
- **Allowed:** Python, sqlite3 or MySQL/Postgres driver, Burp for capturing requests
- **Forbidden:** SQLMap, any automated SQL injection tool

**Description.** A minimal login endpoint built with raw string-concatenated SQL, exploited entirely by hand to bypass authentication, with the exact parse-tree-level explanation of why each payload works.

!!! success "Mandatory"

    - A login query built via string concatenation (e.g. `f"SELECT * FROM users WHERE username='{u}' AND password='{p}'"`) against a real (local) database with at least three seeded users.
    - A working authentication-bypass payload (e.g. `' OR '1'='1' --` or the DB-specific equivalent) that logs in as an arbitrary user without knowing their password, captured with the raw request and the resulting query string logged server-side for evidence.
    - A written, precise explanation of what the database's parser actually does differently with and without the payload — draw or describe the resulting token stream / parse tree for both the intended query and the injected one, not just "it becomes true."
    - A second payload logging in specifically as a target user by name (e.g. `admin'--`) without needing the universal-true trick, demonstrating targeted exploitation, not just a lucky bypass.
    - A note on why comment-based termination (`--`, `#`) is necessary in some contexts and not others, based on what trails the injection point in the original query string.

!!! failure "Forbidden"

    - SQLMap or any tool that generates the payload for you.
    - A payload that happens to work without you being able to explain, unprompted, why.
    - Testing against a database you don't control.

!!! note "Norm"

    See §II.2, plus: the vulnerable query isolated in its own function, request logging separated from query execution.

!!! tip "Bonus"

    Demonstrate the same bypass against both MySQL and PostgreSQL syntax and document the two or three syntax differences that mattered.

### Exercise 01 — unionharvest

- **Turn-in dir:** sql_db_internals/ex01/
- **Files:** EXPLOIT.md, evidence/
- **Allowed:** browser/Burp, manual requests
- **Forbidden:** SQLMap

**Description.** A UNION-based injection against a vulnerable search/listing endpoint, manually extracting the database version, full schema (table and column names via `information_schema`), and table contents — entirely by hand.

!!! success "Mandatory"

    - Determine the number of columns in the original query using `ORDER BY` incrementing or a UNION SELECT with NULLs, showing the exact error/behavior change that reveals the count.
    - Identify which columns are reflected in the output (visible in the response) by injecting recognizable markers into a UNION SELECT, one column at a time.
    - Extract the database version and current database name via the appropriate built-in (e.g. `@@version`/`version()`, `database()`/`current_database()`).
    - Enumerate all tables in the current database via `information_schema.tables` (or the DB-specific equivalent), then all columns of a target table via `information_schema.columns`, then extract full row contents from that table using `GROUP_CONCAT`/`string_agg` or repeated UNION rows.
    - A written walkthrough of the full chain in order, each step's payload and the specific response change that told you it worked.

!!! failure "Forbidden"

    - SQLMap.
    - Skipping straight to a known table name instead of demonstrating the enumeration via `information_schema`.
    - Extracting data from a database that is not your own seeded instance.

!!! note "Norm"

    See §II.2, plus: EXPLOIT.md structured as one numbered step per payload, each with request, response excerpt, and interpretation.

!!! tip "Bonus"

    Repeat the same extraction as error-based injection (forcing the DB to leak data via a crafted error message) on a database/config where UNION is blocked but verbose errors are on.

### Exercise 02 — paramfix

- **Turn-in dir:** sql_db_internals/ex02/
- **Files:** login_fixed.py, PROOF.md
- **Allowed:** parameterized queries via your DB driver's native placeholder support
- **Forbidden:** manual escaping/sanitization as a substitute for parameterization; an ORM used as a black box you cannot explain

**Description.** Every vulnerable query from Exercise 00 and 01 rewritten as a parameterized query, with your own Exercise 00/01 exploits re-run against the fixed version and proven to fail — plus a from-first-principles explanation of why parameterization actually closes the hole.

!!! success "Mandatory"

    - Every string-concatenated query rewritten using your driver's native parameter placeholders (e.g. `?` or `%s` with a separate values tuple) — never manual escaping or blocklisting as the fix.
    - Your exact Exercise 00 authentication-bypass payload and Exercise 01 UNION payloads re-run against the fixed endpoints, captured failing (the payload is now treated as literal data, e.g. a failed login for a nonexistent username containing quote characters).
    - A written, parser-level explanation of why this specifically works: the query structure is parsed and compiled by the database *before* the parameter values are ever substituted, so there is no point at which attacker-controlled bytes can be interpreted as SQL syntax.
    - A written note on why a blocklist-based "fix" (stripping quotes, blocking the word "SELECT") is not equivalent and can be bypassed — with at least one concrete bypass example against a blocklist you deliberately write and then defeat.
    - A note on ORM safety: one example of an ORM call that is still safe (uses parameterization under the hood) and one example of an ORM escape hatch (raw SQL / string-built filter) that reintroduces the exact same vulnerability.

!!! failure "Forbidden"

    - Calling `str.replace()`-based quote-escaping a fix.
    - A blocklist-based mitigation presented as equivalent to parameterization.
    - An ORM example you cannot explain the generated SQL for.

!!! note "Norm"

    See §II.2, plus: PROOF.md is exploit-attempt → observed failure → root-cause explanation, per query fixed.

!!! tip "Bonus"

    Show a second-order injection: data safely parameterized on insert, but later concatenated unsafely into a different query when read back and reused — and fix that too.

## Chapter IV — Capstone

!!! info "How this capstone forces everything together"

    **This exercise forces together** query-parser-level understanding (to construct payloads that are syntactically valid in context, not copy-pasted), `information_schema` enumeration (to know what to extract before extracting it), parameterized-query awareness (to correctly test whether a target is actually vulnerable versus falsely triggering on an unrelated response difference), and patient statistical reasoning about timing and response differences. A tool that only knows UNION injection is useless here — there is nothing to UNION into a response the attacker never sees. It has to infer one bit of information at a time from a true/false signal or a measured delay, thousands of times, without ever seeing the data directly.

### Capstone — blindextract

- **Turn-in dir:** sql_db_internals/capstone/
- **Files:** src/, README.md, evidence/
- **Grading:** mandatory-only; bonus per §II.7

**Description.** A tool that extracts data from a SQL injection point that returns no visible output and no verbose errors — using boolean-based blind and time-based blind techniques, both implemented as a generic binary-search character extractor against any injectable parameter you point it at.

!!! success "Mandatory"

    - Boolean-blind module: given a URL/request template with an injection point and a way to detect true vs. false (e.g. response length, a specific string present/absent, or an HTTP status difference — configurable, not hardcoded to one target), performs binary search over each character of a target value (starting with database version, then table names, then column contents) using conditions like `AND SUBSTRING((SELECT ...),N,1) > 'X'`.
    - Time-based-blind module: same character-by-character extraction, but using a conditional time delay (e.g. `IF(condition, SLEEP(N), 0)` or the DB-specific equivalent) and a statistically sound threshold (not a fixed magic number — justified against baseline request timing variance you measured).
    - Both modules extract, at minimum: database version, current database name, and the full contents of one column in one table you specify — end to end, unattended.
    - A calibration step run before extraction that measures baseline response time/length variance against the target, so the true/false or fast/slow threshold is derived from the target, not assumed.
    - Extraction progress and results logged in real time (not only at the end), so a long-running extraction can be interrupted and inspected mid-run.
    - Demonstrated against your own Exercise 00/01 application modified to suppress all error output and visible query results (simulating a truly blind endpoint), with a full character string successfully extracted and verified correct against the known seeded value.

!!! failure "Forbidden"

    - SQLMap, or wrapping SQLMap and relabeling it.
    - Hardcoding the true/false detection string or the timing threshold for one specific target instead of deriving both from calibration/configuration.
    - A char-extraction loop with no upper bound that can hang forever against a target that stops responding as expected.
    - Claiming successful extraction without the verification step against a known value.

!!! note "Norm"

    See §II.2, plus: calibration, boolean-oracle, time-oracle, and binary-search-extraction each in their own function; the extraction algorithm shared between both oracle types (only the oracle function itself differs).

!!! tip "Bonus (§II.7)"

    Out-of-band extraction technique (e.g. DNS exfiltration via a function the target DB supports) as a third oracle module, demonstrated in a lab where you control the receiving DNS server.

## Chapter V — Submission and Peer-Evaluation

Turn in this subject as a single git repository:

```text
sql_db_internals/
├── ex00/
├── ex01/
├── ex02/
└── capstone/
```

Each exercise is defended live against a fresh copy of the target database (reseeded by the evaluator). For the capstone, the evaluator points your tool at a modified schema/value it has not seen before and expects a correct, verified extraction — a plausible-looking wrong answer is a failure.

## Appendix A — Evaluation Scale (Defense Guide)

> Companion to Chapter III/IV. Not part of the subject proper — this is the scale an evaluator uses. Read it as a self-test before your defense.

### A.0 — manualsqli0

**Defense questions**

1. Write out, right now, the literal final query string your payload produces, character by character.
2. Why does `' OR '1'='1` without a trailing comment sometimes still work depending on what follows in the original query — walk through a case where it would and one where it would break.
3. What is the actual parser-level difference between a value and a keyword in SQL, and how does your payload exploit the boundary between them?
4. Why would a WAF that blocks the literal string `OR 1=1` still be bypassable, in principle, by this same class of bug?

### A.1 — unionharvest

**Defense questions**

1. Walk me through determining the column count live, from scratch, against a fresh copy of the target.
2. Why does column type matter when choosing where to place your extracted string in the UNION — what happens if you put a string where the original column was an integer?
3. Show me your `information_schema` queries — why does this system view exist in the database at all, from the vendor's perspective?
4. What's the difference in evidence between a UNION-based extraction and an error-based one, and when would you have to fall back to the latter?

### A.2 — paramfix

**Defense questions**

1. Re-run your original Exercise 00 payload against this fixed endpoint live — walk me through exactly what the database does with it now.
2. Why doesn't parameterization protect a dynamically-built `ORDER BY` column name the same way it protects a value — what's structurally different about that case?
3. Show me your blocklist bypass — what did the blocklist author fail to anticipate?
4. Point to the ORM raw-SQL escape hatch you demonstrated — why does an ORM even expose that, and when is it legitimately necessary?

### A.3 — Capstone: blindextract

**Defense questions**

1. Walk me through one full character extraction, live, narrating each binary-search step and what response signal told you which half to keep.
2. Why is time-based blind extraction dramatically slower and noisier than boolean-based, and what does your calibration step do about the noise?
3. Show me your calibration output — what did baseline timing variance on this target actually look like, and how did you pick your threshold from it?
4. What happens if the target's response time is affected by something unrelated to your payload (e.g. server load) mid-extraction — does your tool have any resilience to that, or is it a documented limitation?
5. Why can't you just reuse your Exercise 01 UNION approach here — what specifically is different about this target?
6. Extract one new value live that you have not pre-tested, from the same schema, and verify it against the database directly.

**Test / edge cases**

- [ ] A target value containing a single-quote or SQL-meaningful character itself: extracted correctly without breaking the injection payload.
- [ ] An empty string as the true value (extraction should terminate immediately, not loop looking for a first character that never comes).
- [ ] A target column value longer than expected: extraction doesn't truncate silently, length is determined first via `LENGTH()`/`len()` before character extraction begins.
- [ ] Network hiccup mid-extraction (one request times out): retried or logged as a gap, not silently treated as a false result that corrupts the extracted string.
- [ ] Boolean oracle where the "true" condition also changes response length by an amount close to normal variance: calibration catches this and the tool reports low confidence rather than false-positive matches.
- [ ] Time-based oracle against a target with highly variable baseline latency: threshold adapts or the tool explicitly reports that time-based extraction is unreliable here.
- [ ] Case sensitivity in extracted values: correctly preserved, not normalized away by a case-insensitive comparison in the binary search.
