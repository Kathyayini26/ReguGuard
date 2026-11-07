# ReguGuard System Architecture & Technical Specification

## 1. System Vision
ReguGuard converts regulatory audit defense from an annual scramble into a cumulative, experiential advantage. By capturing the negotiated outcomes of previous audits—including both accepted compensating controls and rejected proposals—ReguGuard prevents organizations from repeating compliance mistakes.

## 2. Architectural Data Flow

```
[ Auditor Inquiry / Exception ]
              │
              ▼
[ Control Invariant Parser ] ──────────> Extracts standard criterion (e.g., CC6.1)
              │
              ▼
[ Hindsight Memory Engine ] ───────────> recall_async(control_code, auditor_firm)
              │
              ▼
[ Groq Diagnostic Reasoning ] ────────> Fuses Inquiry + Control Baseline + Recalled Memory
              │
              ▼
[ Defense Briefing ] ──────────────────> Surfaces:
                                         • 🟢 Verified Precedent (if available)
                                         • 🔴 Anti-Pattern Warning (if past proposal failed)
                                         • Evidence Tier: Confirmed / Likely / Unknown
              │
              ▼
[ Human Approval Gate ] ───────────────> SRE / Compliance Officer verifies briefing
              │
              ▼
[ Compensating Control Memo ] ─────────> Formatted defense memo submitted to auditor
              │
              ▼
[ Post-Audit Determination ] ──────────> retain_async(new_outcome, metadata)
```

## 3. The Core Memory Triad
ReguGuard utilizes Vectorize's Hindsight long-term agent memory across three operational dimensions:

1. **Episodic Memory:** Storing the narrative timeline of each audit cycle, including the specific audit firm, lead auditor, and technical scope.
2. **Procedural Memory:** Storing explicit action-outcome pairs:
   - `Proposal A` (Manual spreadsheet review) $\rightarrow$ `Negative Outcome` (Rejected: lacks tamper-evidence).
   - `Proposal B` (KMS digest validation) $\rightarrow$ `Positive Outcome` (Accepted: cryptographic proof).
3. **Temporal Adaptation:** When queried in subsequent years, Hindsight does not just return raw text; it prioritizes recent determinations and flags recurring anti-patterns.
