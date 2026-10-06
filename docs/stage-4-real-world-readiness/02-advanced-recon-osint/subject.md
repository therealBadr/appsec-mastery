---
title: "The Subject"
description: "Bash and Python for Security built a minimal subdomain enumerator and recon pipeline from raw sockets."
---
# Advanced Reconnaissance and OSINT: The Subject

*Subject 2 of 6 — Real-World Readiness and Portfolio · Version 1.0 — September 2026*

> Bash and Python for Security built a minimal subdomain enumerator and recon pipeline from raw sockets. This subject scales that instinct into the full professional recon discipline — ASN mapping, GitHub dorking, and open-source intelligence gathering — because in both bug bounty and real pentest engagements, the attack surface you never found is the one that gets missed entirely.

## Foreword

> *Most real-world breaches don't start with a zero-day. They start with a forgotten subdomain, a leaked key in a public repo, or a staging environment nobody remembered to take down.*

## Why This Subject

Reconnaissance is unglamorous compared to exploitation, which is exactly why it's where a huge fraction of real findings live — an attacker (or a hunter) who maps a target's full attack surface more thoroughly than the target's own security team consistently finds what everyone else missed.

## What You Must Understand

### Passive subdomain enumeration

Discovering subdomains without ever sending the target a single probe request — Certificate Transparency logs, DNS aggregators, and search-engine dorking — extending your Bash and Python for Security capstone's bonus CT-log module into a primary technique.

- Certificate Transparency (crt.sh and similar) surfaces every certificate ever issued for a domain, including subdomains a company forgot existed
- DNS aggregator services (e.g. SecurityTrails-style historical DNS data) reveal infrastructure that has since moved but left a footprint

### ASN and IP-range mapping

Identifying a target organization's full owned IP space via its Autonomous System Number registration — surfacing infrastructure with no DNS name pointing at it at all, which passive subdomain enumeration alone would never find.

- WHOIS/RDAP lookups and BGP-route-viewing services map an organization's registered IP ranges
- An IP range with no friendly hostname is often the least-monitored part of an organization's footprint — exactly where a forgotten admin panel or dev environment tends to live

### GitHub/code-host dorking

Public code repositories — including a company's own public repos, and former employees' personal repos — as an OSINT source, directly relevant to Secrets Detection's lesson that a committed secret is permanent: someone else's leaked credential is exactly as usable as one you found through exploitation.

- Search-operator dorking for company-specific config file patterns, internal hostnames, or credential-shaped strings across public repos
- A former employee's personal repository can leak internal context (naming conventions, architecture hints, even credentials) the company itself never published

### OSINT for social/organizational attack surface

Publicly available information about an organization's technology stack, employees, and structure — job postings revealing exact technology versions in use, LinkedIn revealing org structure useful for a social-engineering-aware pentest (Stage 4's Full Pentest Methodology subject), and public breach-database cross-referencing for reused credentials.

- A job posting listing "5 years of experience with [specific framework version]" is a direct technology-stack disclosure
- This roadmap does not build active social-engineering skill (out of scope per the roadmap's own stated focus) — the value here is the passive intelligence, not a phishing-pretext exercise

## Practical Outputs

!!! success "Practical outputs"

    - A full passive recon report against a real, in-scope bug bounty target (reusing Bug Bounty Methodology's program) or your own domain: subdomains via CT logs and DNS aggregation, IP ranges via ASN mapping, with zero active probes sent to the target during this phase.
    - A GitHub/code-host dork sweep against a real organization's public footprint (yours, or an authorized target), with any findings responsibly triaged — a live credential found this way is reported through the same responsible-disclosure channel as any other finding, never exploited further.
    - A consolidated attack-surface map combining all sources into one document: every discovered asset, its source, and its apparent purpose/risk.
    - A written comparison of what active recon (your Bash and Python for Security pipeline) versus passive recon each surface, and why a real engagement needs both.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "Active scanning finds everything eventually." Passive sources surface forgotten/decommissioned-but-still-live infrastructure that active enumeration against current DNS records will never reach.
    - "OSINT is just googling." Systematic OSINT — ASN mapping, CT-log analysis, code-host dorking — is a repeatable methodology with real technique, not casual searching.
    - "A leaked secret found via GitHub dorking is fair game to use." It's a finding to report responsibly, identically to any other vulnerability — using it to access systems beyond proving impact crosses the same line Bug Bounty Methodology drew for any other finding.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Produce a full passive attack-surface map for an unfamiliar domain using at least three independent source types.
    - Explain what ASN mapping surfaces that subdomain enumeration alone cannot.
    - Walk through a responsible-disclosure decision for a hypothetical credential found via code-host dorking.
    - Justify, for a real engagement, the specific balance of active versus passive recon you'd use and why.
