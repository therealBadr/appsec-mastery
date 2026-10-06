---
title: "The Subject"
description: "A first specialization lane: everything this roadmap taught about web request/response security has a mobile analogue, plus an entire new surface — the AP…"
---
# Mobile AppSec: Android: The Subject

*Subject 1 of 7 — Advanced Specialization · Version 1.0 — September 2026*

> A first specialization lane: everything this roadmap taught about web request/response security has a mobile analogue, plus an entire new surface — the APK itself as a reverse-engineering target, and the Android platform's own permission and IPC model as a second authorization system, exactly the way Kubernetes RBAC was a second authorization system on top of the application's own.

## Foreword

> *A mobile app's client-side code is not a black box the way a web server's backend is. It ships to the attacker's device, in full, every single install.*

## Why This Subject

Mobile AppSec inherits every server-side vulnerability class from Stages 1-2 (the backend API a mobile app talks to is exactly as attackable as any web API), and adds a genuinely new dimension this roadmap hasn't covered: the client binary itself is fully in the attacker's hands, reversible, and instrumentable, which changes what "client-side security" can even mean.

## What You Must Understand

### APK structure and static analysis

An APK is a structured archive (manifest, DEX bytecode, resources, native libraries) that decompiles readably enough that "obfuscation" is a speed bump, not a barrier — the direct mobile analogue of reading unminified JavaScript in Client-Side Injection.

- AndroidManifest.xml declares permissions, exported components, and the app's attack surface before you've even decompiled a single class
- Tools like jadx/apktool decompile DEX bytecode back to near-readable Java/Kotlin — hardcoded secrets and logic flaws are frequently visible directly in the decompiled source, the same "read the client-side artifact" technique from Access Control and IDOR's Exercise 02

### Insecure local data storage

The mobile-specific instance of a recurring roadmap theme (Secrets Detection and Management, applied on-device): SharedPreferences, SQLite databases, and files written to app-private storage that turn out to be readable, or that store sensitive data unencrypted when the platform offered a secure alternative.

- A rooted device (or an emulator, no root needed) gives full filesystem access to inspect exactly what an app persisted locally, unencrypted
- The Android Keystore exists specifically to avoid this — an app storing a token in plain SharedPreferences instead of using it is the same "used the wrong tool for secret storage" mistake as Secrets Management's environment-variable delusion

### Insecure IPC (Inter-Process Communication)

Android's own second authorization model — Activities, Services, Broadcast Receivers, and Content Providers each have an "exported" flag and optional permission requirements, and a component exported without a permission check is directly reachable by any other app on the device.

- An exported Content Provider with no permission check is the mobile-platform version of an unauthenticated API endpoint — the same BOLA/BFLA reasoning from API Authorization applies, just at the OS-IPC layer instead of HTTP
- Intent-based communication that trusts the calling app's identity without verification is exploitable by any malicious app the user has installed

### Network communication and certificate pinning bypass

Mobile apps frequently talk to the same kind of backend API this roadmap has spent two stages attacking — proxying that traffic through Burp (as you've done throughout) requires defeating certificate pinning first, which is itself a well-understood, learnable technique.

- Frida-based runtime instrumentation to hook and neutralize a pinning check at the code level, rather than trying to defeat it at the network level
- Once pinning is bypassed, every Stage 1-2 API-focused technique (BOLA, mass assignment, injection) applies identically to the mobile app's backend traffic

## Practical Outputs

!!! success "Practical outputs"

    - A static analysis of a real (or deliberately vulnerable, e.g. an OWASP MASTG/MSTG crackme or vulnerable app) APK: decompiled and reviewed for hardcoded secrets, insecure storage patterns, and exported-component misconfiguration, using your Secure Code Review methodology directly.
    - A working exploitation of at least one insecure-IPC finding (an exported component reachable from a second, attacker-controlled app you build) demonstrated end to end.
    - A certificate-pinning bypass (Frida-based) against a pinned test app, with the underlying API traffic then proxied through Burp and tested with at least one Stage 1-2 technique (e.g. a BOLA probe against the mobile backend).
    - A written mapping document: for each finding class in this subject, the exact OWASP Mobile Top 10 category it corresponds to, and which earlier roadmap subject's technique it most directly reuses.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "Obfuscation is real security." Obfuscated code slows down analysis; it does not prevent it — treat it as a speed bump, and budget analysis time accordingly rather than assuming a "protected" app is actually protected.
    - "Mobile security is a totally separate discipline from web AppSec." The backend API is exactly as attackable as any web target; what's genuinely new is the client-binary and platform-IPC surface, not the entire field.
    - "Certificate pinning makes the app un-testable." Pinning is a speed bump against casual interception, not a barrier to a researcher willing to instrument the running process — treat a "pinning defeated my Burp proxy" moment as a prompt to learn Frida, not a dead end.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Statically analyze an unfamiliar APK and identify at least one real finding across storage, IPC, or hardcoded-secret categories without notes.
    - Explain Android's exported-component model precisely enough to identify a vulnerable configuration from the manifest alone.
    - Bypass certificate pinning on a test app and proxy its traffic through Burp, live.
    - Map a mobile finding to its OWASP Mobile Top 10 category and its nearest web-AppSec analogue.
