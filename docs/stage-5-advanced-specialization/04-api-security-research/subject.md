---
title: "The Subject"
description: "Modern API Authorization built the practitioner's skill: find BOLA/BFLA/mass-assignment in a given API."
---
# API Security Research: The Subject

*Subject 4 of 7 — Advanced Specialization · Version 1.0 — September 2026*

> Modern API Authorization built the practitioner's skill: find BOLA/BFLA/mass-assignment in a given API. This specialization lane goes further into research territory — the protocol-level and specification-level issues that produce entire classes of findings across many APIs at once, the kind of work that produces a genuinely novel technique rather than another instance of a known one.

## Foreword

> *A practitioner finds the BOLA in this API. A researcher asks why the OpenAPI specification format itself makes BOLA this easy to introduce and this hard to catch by tooling, across every API that uses it.*

## Why This Subject

This lane assumes Modern API Authorization's practitioner skill as a prerequisite and reorients it toward research questions: instead of testing one API for known bug classes, study a protocol or specification format itself for structural weaknesses that would predict where new bug classes are likely to keep appearing.

## What You Must Understand

### gRPC and Protocol Buffers security

A binary, schema-defined RPC protocol increasingly used for service-to-service (and sometimes client-facing) communication — different attack surface than REST/GraphQL's text-based, self-describing formats, with its own specific research questions around reflection, schema exposure, and message-size/resource-exhaustion behavior.

- gRPC server reflection (if left enabled) discloses the full service/method schema, the direct protocol analogue of GraphQL introspection from Advanced Web Exploitation II
- Protobuf's binary format means many web-focused tools (built for text-based HTTP) don't natively understand it — a genuine tooling gap a researcher can productively work in

### WebSocket and real-time API security

A persistent, bidirectional connection breaks several assumptions the request/response-oriented techniques from Stage 1-2 depend on — CSRF-equivalent origin-validation questions apply differently, and message-level authorization has to be re-checked per message, not just at connection time.

- A WebSocket connection authenticated only at handshake time, with no per-message authorization check, is the real-time-API version of Access Control and IDOR's "checked once, trusted forever" failure mode
- Cross-Site WebSocket Hijacking: the CSRF-equivalent attack against a WebSocket endpoint with insufficient origin validation at connection time

### API specification-format weaknesses

Research at the level of the OpenAPI/GraphQL/gRPC specification formats themselves: what does each format make easy to express correctly (and what does it make easy to get wrong by default) — the kind of question whose answer predicts findings across every API built on that format, not just one.

- A specification field with an insecure-by-default value (if one exists in a format/framework combination you study) produces the same finding repeatedly across every API generated from it — a single research insight with wide practical reach
- This is precisely the research mode Real-World Readiness's CVE Reproduction and N-Day Research subject built the patch-diff/advisory-reading skill for, now aimed forward at original findings instead of backward at disclosed ones

### API gateway and aggregation-layer risk

A gateway sitting in front of many backend services introduces its own security surface distinct from any individual backend's — inconsistent auth enforcement across routes, request/response transformation bugs, and the gateway itself becoming a high-value single point of compromise for everything behind it.

- A gateway that terminates TLS and re-establishes an internal connection without equivalent authentication is a variant of the SSRF "borrows the server's network position" idea, now structural to the architecture rather than a bug in one endpoint
- Route-specific authentication/authorization configuration drift (one route's gateway config subtly differs from a sibling route's) is a realistic, checkable research target across real-world gateway configurations

## Practical Outputs

!!! success "Practical outputs"

    - A gRPC security assessment of a service you build (or a deliberately vulnerable gRPC target), including a reflection-based schema-enumeration finding and at least one authorization gap reusing your BOLA/BFLA methodology adapted to gRPC's call shape.
    - A WebSocket application (you build) with a deliberately weak per-message authorization model, exploited to demonstrate a message-level authorization bypass distinct from the connection-time auth check succeeding correctly.
    - A written research note on one API specification format's structural weakness — a genuine analysis of what the format makes easy to get wrong, with at least one concrete example finding produced from that structural insight, not just one API's individual bug.
    - An API gateway configuration review (yours, or a documented reference architecture) identifying at least one route-specific authentication/authorization inconsistency.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "Every API is basically REST with different syntax." gRPC and WebSocket-based APIs violate assumptions (request/response symmetry, connection-time-only authentication) that REST-focused tooling and technique take for granted — treating them identically produces false negatives.
    - "Research means finding something nobody's ever found before." Most valuable research work is systematic analysis that predicts and explains a class of findings, not necessarily a single unprecedented discovery — the CVE Reproduction subject's "independent reproduction is real research too" lesson applies here as well.
    - "The gateway is just plumbing, not part of the attack surface." A misconfigured gateway is frequently the highest-value single target in an entire architecture, precisely because it sits in front of everything else.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Assess an unfamiliar gRPC service for reflection exposure and at least one authorization gap.
    - Explain precisely why WebSocket authorization requires different reasoning than REST/GraphQL request-response authorization.
    - Present your specification-format research note and defend why the structural weakness you identified predicts findings beyond the one example you produced.
    - Review an unfamiliar API gateway configuration and identify a route-level inconsistency.
