# ReguGuard Dataset Strategy & Authentic Oversight Evidence Catalog

## 1. Overview & Dataset Integrity Standard

ReguGuard evaluates cybersecurity audit compliance and remediation feasibility using **authentic, publicly documented federal oversight findings**.

Unlike synthetic audit simulators or manually approximated records, all primary datasets in ReguGuard are directly extracted from official U.S. Government Accountability Office (GAO) reports and Inspector General (OIG) investigations.

Every record in ReguGuard maintains:
- **Official Publication Date:** Verified as **December 11, 2025** across all records and documentation.
- **Verifiable Provenance:** Direct URL to the official government publication, exact report number (`GAO-26-107980`), exact table or section name, and line/paragraph citations.
- **Exact Numeric Fidelity:** All vulnerability counts, remediation action tallies, concurrence stances, and completion dates match official records verbatim.
- **Clear Status Distinction:** System finding remediations are explicitly labeled as **VA-reported remediations as of July 2025**. They are **not** labeled as independently verified closures.
- **Separation of Source Findings vs. AI Analysis:** Official source findings contain exclusively what GAO, MITRE, and VA OIG reported. Regulatory crosswalks (NIST SP 800-53, SOC 2 TSC) and compensating control recommendations are segregated into `data/analysis/framework_mappings.json`.
- **System Anonymisation Preserved:** The five high-impact systems are designated strictly as **System 1, System 2, System 3, System 4, and System 5** (per GAO-26-107980, Table 3 footnote a). No artificial system names or weaknesses have been assigned.

---

## 2. Authentic Primary Datasets

The primary oversight dataset is partitioned into three distinct, verified JSON files in `data/processed/`:

### A. Program Findings (`data/processed/program_findings.json`)
- **Source:** GAO-26-107980, Table 1 (MITRE Finding Descriptions), Table 4 (Remediation Plan & VA Concurrence), Table 6 (July 2025 Reported Progress).
- **Scope:** 11 Information Security Program Finding Areas.
- **Official Publication Date:** December 11, 2025.
- **Verified Metrics:**
  - 55 total planned remediation actions across the 11 finding areas.
  - 20 actions completed as of July 2025; 35 actions in progress or delayed.
  - VA concurred with 9 finding areas and non-concurred with 2 (`Customer Service to Systems Teams` and `Cybersecurity Governance`).
  - Documented delays in `Medical Devices` (delayed to May 2027), `Cyber Protection` (delayed to FY 2026), and `Cyber Response and Recovery` (delayed to FY 2026).

### B. High-Impact System Findings (`data/processed/system_findings.json`)
- **Source:** GAO-26-107980, Table 3 (Findings & Plan Dates), Table 5 (July 2025 Remediation Progress).
- **Scope:** 5 Anonymised High-Impact Information Systems (System 1–5).
- **Official Publication Date:** December 11, 2025.
- **Status Distinction:** All figures represent **VA-reported remediation progress as of July 2025** and are not labeled as independently verified or closed.
- **Verified Metrics:**
  - **442 total findings** across the 5 systems (System 1: 107, System 2: 65, System 3: 107, System 4: 56, System 5: 107).
  - **29 high-risk vulnerabilities** (27 reported remediated by VA by July 2025, 93%).
  - **155 moderate-risk vulnerabilities** (135 reported remediated by VA by July 2025).
  - **258 low-risk vulnerabilities** (217 reported remediated by VA by July 2025).
  - **379 of 442 total findings reported remediated by VA** as of July 2025 (86%).
  - Original estimated completion dates: System 5 (12/31/2024), System 4 (01/31/2025), System 3 (03/30/2025), System 1 (12/31/2025), System 2 (01/02/2028).

### C. VA OIG Recommendations Discussed by GAO (`data/processed/oig_recommendations.json`)
- **Source:** GAO-26-107980, Section 4 (lines 5397–5404), Executive Summary (lines 3611–3616), Footnote 33 (lines 5858–5867).
- **Official Publication Date:** December 11, 2025.
- **Scope:** 2 Priority Recommendation Themes from VA OIG FISMA Audits (Audit 23-01105-69 & Audit 24-01233-90).
- **Verified Status (as of July 2025):** Both recommendations remained **`Not implemented`**.
  1. *Theme 1: POA&M Tracking and Updating* – Ensure the department tracks and updates planned remediation documents (GAO found an un-updated high-risk vulnerability past due by 15 months).
  2. *Theme 2: Mitigating Controls for Delayed Vulnerabilities* – Improve process for resolving vulnerabilities that cannot be addressed within policy timeframes by ensuring implementation of mitigating controls (GAO found two high-risk vulnerabilities unmitigated over a 17-to-21-month period).

---

## 3. Separate ReguGuard AI & Compliance Analysis (`data/analysis/framework_mappings.json`)

To preserve documentation integrity, regulatory interpretations are isolated from official findings:
- **NIST SP 800-53 Rev. 5 Controls:** e.g., `CA-7`, `CM-2`, `CM-6`, `AC-2`, `AC-6`, `SC-7`, `SI-2`, `PM-1`, `RA-3`.
- **NIST Cybersecurity Framework (CSF) 2.0 Categories:** e.g., `GV.PO`, `GV.GO`, `ID.RA`, `GV.RR`, `DE.CM`, `PR.PS`, `PR.DS`, `PR.AA`, `DE.AE`, `RS.MI`.
- **AICPA SOC 2 Type II Criteria:** e.g., `CC1.1`, `CC2.1`, `CC3.1`, `CC6.1`, `CC6.6`, `CC6.8`, `CC7.1`, `CC7.4`.
- **AI Risk Interpretations:** Diagnostic reasoning regarding root causes (siloed teams, legacy system constraints, alert fatigue).
- **Compensating Control Recommendations:** Practical engineering mechanisms (standardized SLAs, network segmentation, zero trust patterns).

---

## 4. Verification Sign-Off

See [`docs/AUDIT_VERIFICATION_REPORT.md`](AUDIT_VERIFICATION_REPORT.md) for the complete, record-by-record verification matrix matching all 18 records against official report `GAO-26-107980`.
