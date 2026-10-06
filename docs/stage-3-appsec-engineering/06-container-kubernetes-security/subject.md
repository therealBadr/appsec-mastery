---
title: "The Subject"
description: "Your Inception project gave you real Docker and container-networking depth already."
---
# Container and Kubernetes Security: The Subject

*Subject 6 of 9 — Secure Development / AppSec Engineering · Version 1.0 — September 2026*

> Your Inception project gave you real Docker and container-networking depth already. This subject turns that operational familiarity into a security lens: image provenance, runtime isolation boundaries, and the specific ways a Kubernetes cluster's own control plane becomes an attacker's next target after an initial container compromise.

## Foreword

> *A container is a process with a nicer filesystem view, not a virtual machine. Every security property you assume from "it's isolated" needs to be checked against what the kernel actually enforces.*

## Why This Subject

This subject deliberately builds on your existing Inception-project Docker depth rather than re-teaching containers from zero — the security-specific layer is image supply chain (what's actually inside the image you're running), runtime hardening (what the container can do to the host if compromised), and Kubernetes-specific attack surface (the orchestrator's own API and RBAC model, which is a second, separate authorization system on top of whatever the application implements).

## What You Must Understand

### Image security

What actually ships inside a container image — base image provenance, vulnerable OS/library packages baked in, secrets accidentally committed into a layer, and the difference between "scanned once at build time" and "still accurate six months later."

- Image scanning (Trivy, Grype) against both OS packages and application dependencies — SCA's reachability discipline applies here too
- Minimal base images (distroless, alpine) reduce attack surface by simply containing less to exploit
- A secret committed into an intermediate build layer persists in the image history even if a later layer deletes the file — multi-stage builds are the actual fix

### Runtime hardening

The kernel-level controls that determine what a compromised container can actually do to its host: capabilities (the same Linux capability model from Linux Administration Depth, applied to containers), seccomp profiles, and read-only root filesystems.

- Running as non-root inside the container, with no capability to escalate, directly reuses the least-privilege reasoning from Secure Coding Principles
- A container running `--privileged` has essentially no meaningful isolation from the host at all
- seccomp profiles restrict which syscalls a container can make — a direct extension of the syscall-level reasoning from OS Internals

### Kubernetes RBAC and the API server

Kubernetes has its own authorization system (Roles, ClusterRoles, RoleBindings) sitting alongside whatever the application implements — a second access-control surface, with the identical BOLA/BFLA failure modes (an overly broad Role is a BFLA finding for the cluster itself).

- A ServiceAccount token mounted into every pod by default is a credential an attacker who compromises one container can use against the Kubernetes API itself
- Overly permissive ClusterRoleBindings (e.g. cluster-admin bound broadly) are the Kubernetes-native version of a mass-assignment or excessive-privilege finding

### Pod-to-node and cluster escape paths

The specific chain from "compromised one container" to "compromised the whole cluster": a mounted host path, an overprivileged ServiceAccount, or a reachable Kubernetes API server with weak RBAC — the concrete instance of SSRF's "borrows the server's network position" idea applied at cluster scale.

- Sensitive hostPath mounts (e.g. the Docker socket itself mounted into a pod) hand a compromised container direct control over the host
- The Kubernetes API server, if reachable and under-restricted, is itself a high-value SSRF-reachable target from inside the cluster — directly analogous to the cloud metadata endpoint from File Handling and Cloud SSRF

## Practical Outputs

!!! success "Practical outputs"

    - An image-scanning report (Trivy/Grype) against a real application image, with findings triaged for reachability, mirroring the SCA and SAST triage discipline.
    - A hardened Dockerfile/runtime configuration (non-root user, dropped capabilities, read-only filesystem, minimal base image) for one of your own earlier vulnerable-app containers, with a before/after capability comparison.
    - A Kubernetes RBAC audit of a small cluster you stand up (kind/minikube is fine): enumerate every ServiceAccount, Role, and Binding, and flag anything overly permissive using the same BOLA/BFLA-style reasoning from Stage 2.
    - A written attack-path narrative: starting from a compromised container in your lab cluster, document the specific misconfiguration(s) that would let an attacker reach the node or the broader cluster, and the fix for each.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "Containers are inherently secure/isolated." A container shares the host kernel; isolation is a set of specific, checkable controls (namespaces, cgroups, capabilities, seccomp), not a property you get for free.
    - "We scanned the image once at build time, we're covered." New CVEs are published continuously against packages baked into an image months ago — scanning has to be recurring, not a one-time gate.
    - "Kubernetes RBAC is someone else's (the platform team's) problem." An application-security review that ignores the cluster's own authorization layer misses an entire, often more permissive, access path.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Explain precisely what a container's isolation actually consists of at the kernel level, and where it can fail.
    - Given a Dockerfile, identify every hardening gap (root user, unnecessary capabilities, bloated base image) without notes.
    - Audit an unfamiliar Kubernetes cluster's RBAC configuration and identify the most dangerous overprivileged binding.
    - Walk through a full compromised-container-to-cluster-compromise attack path you've personally reproduced in your lab.
