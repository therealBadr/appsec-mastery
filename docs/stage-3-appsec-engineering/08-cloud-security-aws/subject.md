---
title: "The Subject"
description: "The File Handling and Cloud SSRF subject reached the metadata endpoint via SSRF; this subject builds the rest of the cloud-specific attack surface around …"
---
# Cloud Security Fundamentals (AWS): The Subject

*Subject 8 of 9 — Secure Development / AppSec Engineering · Version 1.0 — September 2026*

> The File Handling and Cloud SSRF subject reached the metadata endpoint via SSRF; this subject builds the rest of the cloud-specific attack surface around it — IAM as the actual perimeter in a cloud environment, S3 misconfiguration as the single most common real-world cloud breach cause, and Lambda's own distinct security model.

## Foreword

> *In a data center, the perimeter was the network. In the cloud, the perimeter is an IAM policy document — and it's written in JSON, which means it's one misplaced wildcard away from meaning something nobody intended.*

## Why This Subject

A huge fraction of real-world cloud breaches trace back to three specific, well-understood misconfiguration classes: an S3 bucket left public, an IAM role granted far more than it needs, and a serverless function with an overprivileged execution role — none of which require any novel exploitation technique once you know exactly where to look and how AWS's own permission model actually resolves.

## What You Must Understand

### IAM as the real perimeter

AWS Identity and Access Management: policies (what's allowed), roles (identities services/users assume), and the actual evaluation logic (explicit deny always wins, otherwise any matching allow grants access) that determines what a compromised credential or role can actually do.

- The Principle of Least Privilege applied concretely: an IAM policy with `"Action": "*", "Resource": "*"` is the cloud-native version of running a container as root
- Policy evaluation logic specifically: an explicit Deny anywhere in the applicable policies always wins, which is a common source of "why isn't this working" confusion and also a real defense-in-depth tool

### S3 misconfiguration

The single most common real-world cloud-breach root cause: a bucket or bucket policy that grants public or overly broad read/write access, often through a misunderstood ACL, a permissive bucket policy, or Block Public Access settings left disabled.

- Bucket policy vs. ACL vs. account-level Block Public Access settings — three separate controls that all have to align for a bucket to actually be private
- A public-write (not just public-read) bucket is a far more severe finding — data tampering or hosting malicious content, not just disclosure

### IMDS and instance-role compromise

The direct continuation of File Handling and Cloud SSRF's metadata-endpoint work: what an attacker actually does with the temporary credentials obtained there — enumerate the attached IAM role's actual permissions and pivot outward from there.

- The stolen credentials are exactly as powerful as the EC2 instance's attached IAM role — an overprivileged instance role turns a single SSRF into a much larger compromise
- IMDSv2 plus a minimal, tightly-scoped instance role are complementary mitigations, not substitutes for each other

### Lambda and serverless security

A distinct execution model with its own security considerations: the function's execution role (its own IAM identity, separately scoped from anything else), event-source injection (an attacker-controlled event payload as a new kind of untrusted-input surface), and dependency/cold-start-specific risks.

- A Lambda's execution role, like an EC2 instance role, should be scoped to exactly what that one function needs — a shared, broad execution role across many functions violates least privilege the same way a shared broad service account does
- Event-source data (e.g. from an S3 trigger, an API Gateway request, a queue message) is still untrusted input and subject to every injection class from Stage 1, just arriving through a different entry point than an HTTP request

## Practical Outputs

!!! success "Practical outputs"

    - An AWS Free Tier lab: a deliberately exposed S3 bucket (public read, or public write) exploited to demonstrate real data disclosure/tampering, then fixed and re-verified as private using all three relevant controls (ACL, bucket policy, Block Public Access).
    - An over-permissioned IAM role exploited in your lab (e.g. a role attached to an EC2 instance with far more access than the instance's function requires), with the specific excessive permission identified and scoped down to least privilege.
    - A vulnerable Lambda function (e.g. one that evaluates untrusted event data unsafely, reusing an injection technique from Stage 1) exploited and fixed, with its execution role scoped to least privilege.
    - A written IAM policy review checklist you'd apply to an unfamiliar AWS account, prioritized by what to check first.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "Our data is safe because it's in the cloud." The cloud provider secures the infrastructure; the customer is responsible for configuring IAM, S3, and everything above it correctly — this is AWS's own shared-responsibility model, not an assumption to skip.
    - "IAM is too complex to fully understand, so we'll just grant broad access and move on." This is exactly the instinct that produces the majority of real-world cloud breaches — the complexity is a reason to learn the evaluation logic, not to avoid it.
    - "We rotated the instance's stolen credentials, we're done." If the role itself was overprivileged, the next SSRF or compromise gets the same excessive access again — the role's scope is the actual fix, not just the one incident's cleanup.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Given an IAM policy document, determine exactly what it allows and identify any overly broad grants without notes.
    - Explain the three separate S3 controls that must all align for a bucket to be genuinely private.
    - Walk through the full chain from SSRF/metadata-endpoint compromise to IAM-role-scoped blast radius, live.
    - Review an unfamiliar Lambda function's execution role and identify whether it follows least privilege.
