# ReguGuard: Official 2-Session Live Demonstration Script

This script provides the step-by-step walkthrough for recording the required 2–3 minute video presentation.

---

## Act 1: The Problem & Session 1 (Learning Phase) — [0:00 - 1:00]

1. **Context:** A fast-growing B2B software startup is undergoing its annual SOC 2 Type II audit by external audit firm **Schellman**.
2. **Inquiry Received:** Auditor Schellman flags a Management Exception under **CC6.1**:
   > *"Unrestricted IAM administrative role detected on the staging environment. Developers can assume admin rights without an independent approval gate."*
3. **The Naive Mistake:** A junior compliance engineer proposes a common textbook solution:
   > *"We will institute a weekly manual spreadsheet sign-off sheet for all staging access."*
4. **The Auditor Rejection:** Auditor Schellman officially **rejects** the proposal:
   > *"REJECTED: Manual spreadsheets lack cryptographic tamper-evidence and cannot be verified independently under Trust Services Criteria CC6.1."*
5. **The Verified Remediation:** The senior CISO steps in and negotiates an approved compensating control:
   > *"We will implement an automated GitHub Actions PR workflow where ephemeral IAM roles are granted only upon dual-peer review and logged to a tamper-proof S3 bucket with AWS CloudTrail KMS digest verification."*
6. **The Auditor Sign-Off:** Schellman accepts the compensating control and issues an unqualified (clean) audit report.
7. **The Retention:** ReguGuard captures the entire episode:
   - `retain()` stores the rejected proposal (spreadsheet review) as an **Anti-Pattern**.
   - `retain()` stores the approved compensating control (KMS digest pipeline) as an **Approved Precedent**.

---

## Act 2: Session 2 (Next Year's Audit — The Memory Payoff) — [1:00 - 2:15]

1. **Fast-Forward 12 Months:** The company is undergoing its next SOC 2 audit. A *different* auditor from Schellman is assigned.
2. **New Inquiry Received:** The new auditor flags a similar exception on a newly created AI training cluster:
   > *"Found developers assuming administrative roles on GPU training nodes without segregation of duties under CC6.1."*
3. **ReguGuard Query:** The new compliance officer opens ReguGuard and submits the inquiry.
4. **The Hindsight Moment:**
   - ReguGuard calls `hindsight.recall()`.
   - It recognizes the invariant control code `CC6.1` and matches audit firm `Schellman`.
   - **🔴 DANGER / ANTI-PATTERN WARNING FLASHES:**
     > *"DO NOT propose manual spreadsheet reviews! Schellman explicitly rejected this in 2025 citing lack of cryptographic tamper-evidence."*
   - **🟢 APPROVED PRECEDENT DISPLAYED:**
     > *"Precedent ID PREC-CC61-01: Schellman accepted 'Automated Ephemeral KMS Log Pipeline' with CloudTrail digest verification in 2025 under Memo #CC-104."*
5. **The One-Click Action:** The compliance officer clicks **[Generate Defense Memo]**.
6. **The Result:** An official, legally sound defense memorandum is generated in seconds. The auditor accepts the precedent immediately without issuing a finding.

---

## Act 3: Wrap-Up & Key Takeaway — [2:15 - 2:45]

- Without Hindsight: The team repeats past mistakes, wastes engineering weeks, or gets an audit qualification.
- With Hindsight: Every historical audit negotiation becomes a permanent corporate asset.
