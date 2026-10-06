---
title: "The Subject"
description: "The second half of the mobile lane, deliberately separated from Android because the platform model is genuinely different: a more locked-down OS, Objectiv…"
---
# Mobile AppSec: iOS: The Subject

*Subject 2 of 7 — Advanced Specialization · Version 1.0 — September 2026*

> The second half of the mobile lane, deliberately separated from Android because the platform model is genuinely different: a more locked-down OS, Objective-C/Swift binaries instead of DEX bytecode, and a jailbreak-dependent (rather than root-dependent) analysis workflow.

## Foreword

> *iOS's sandbox is stronger than Android's by default, which doesn't mean iOS apps are more secure — it means the same developer mistakes are simply harder for a researcher to reach, not less common.*

## Why This Subject

This subject deliberately parallels Mobile AppSec: Android's structure so the platform differences are the thing that stands out — the vulnerability classes (insecure storage, weak IPC-equivalent, defeatable pinning) are conceptually identical; the tooling, binary format, and platform security model are not, and conflating the two platforms is a common, career-limiting mistake for a mobile-focused specialist.

## What You Must Understand

### IPA structure and binary analysis

An IPA is a structured archive containing a Mach-O binary (Objective-C/Swift) and resources, analyzed with a different toolchain than Android's — class-dump/Hopper/Ghidra for static analysis, and the binary's far more limited "decompile to readable source" story compared to DEX.

- Objective-C's runtime message-passing model means method names are frequently still visible in the binary even without full decompilation, which is its own useful static-analysis signal
- Swift binaries are meaningfully harder to reverse than Objective-C ones — a real, current tooling-maturity gap worth knowing about going in

### Insecure local data storage on iOS

The same underlying mistake as Android's (data that should be in a secure, platform-provided store ending up in a plaintext file or a database instead), expressed through iOS-specific mechanisms — NSUserDefaults, an unencrypted local database, or a Keychain item stored with an overly permissive accessibility level.

- The iOS Keychain is the correct place for sensitive data — an app using NSUserDefaults for a session token instead is the direct iOS analogue of Android's SharedPreferences mistake
- Even correct Keychain usage can be undermined by a permissive accessibility attribute (e.g. accessible even when the device is locked) — a configuration nuance worth checking specifically, not assumed safe from Keychain usage alone

### App sandboxing and inter-app communication

iOS's sandbox is stronger by default than Android's, but Custom URL Schemes and Universal Links are the platform's IPC-equivalent attack surface — an app registering a URL scheme with no validation of the calling app or the URL's parameters is exploitable by any other installed app or a malicious webpage.

- A Custom URL Scheme handler that acts on parameters with no validation is directly the mobile-platform version of an injection sink — the same source/sink reasoning from Client-Side Injection applies
- Universal Links (HTTPS-based, domain-verified) are the more secure modern alternative — an app still using unvalidated Custom URL Schemes for sensitive actions is a real, checkable finding

### Jailbreak-dependent dynamic analysis

Where iOS most diverges from the Android workflow: full runtime instrumentation (Frida, Objection) and filesystem access for dynamic testing generally requires a jailbroken device or a jailbroken-equivalent research environment — a meaningfully higher setup cost than Android's emulator-based workflow.

- A jailbroken test device (or a corellium-style virtual research device, where accessible) unlocks the same class of certificate-pinning bypass and runtime hooking used in the Android subject
- iOS's more locked-down default posture means static analysis carries proportionally more weight in an iOS assessment than it typically does for Android, where dynamic analysis is cheaper to set up

## Practical Outputs

!!! success "Practical outputs"

    - A static analysis of a real (or deliberately vulnerable, e.g. an OWASP iGoat-style) IPA: binary and resource review for hardcoded secrets and insecure storage, mirroring the Android subject's methodology on iOS's toolchain.
    - A working exploitation of an insecure Custom URL Scheme handler (a crafted URL/webpage triggering unintended app behavior) demonstrated end to end.
    - A certificate-pinning bypass on a jailbroken (or jailbreak-equivalent) test device using Frida/Objection, with the resulting API traffic tested with a Stage 1-2 technique exactly as in the Android subject.
    - A written comparison document: for every finding class covered in both mobile subjects, the specific tooling and platform-model difference between Android and iOS, aimed at a reader deciding which platform to specialize in first.

## Common Delusions

!!! warning "Common delusions at this stage"

    - "iOS's sandbox means iOS apps don't have these bugs." The sandbox limits reachability from a researcher's or attacker's external vantage point; it does not stop a developer from making the identical storage or validation mistake inside their own app's sandbox.
    - "The Android and iOS mobile-security skillsets transfer completely." The vulnerability classes transfer; the tooling, binary format, and analysis workflow are different enough that real fluency in one doesn't automatically confer fluency in the other.
    - "You need a jailbroken device for everything." Static analysis (this subject's first topic) goes a long way without one — jailbreak-dependent dynamic analysis is a real cost worth reserving for when static analysis alone is insufficient.

## Exit Gate

!!! abstract "Exit gate: all of it, without notes"

    - Statically analyze an unfamiliar IPA and identify at least one real finding without notes.
    - Explain the specific accessibility-attribute nuance that can undermine otherwise-correct Keychain usage.
    - Exploit an insecure Custom URL Scheme handler, live, from a crafted trigger.
    - Articulate, specifically, what differs in tooling and workflow between an Android and an iOS assessment for the same underlying finding class.
