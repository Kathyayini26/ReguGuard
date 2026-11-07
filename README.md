# ReguGuard: The Experiential Audit Intelligence Agent

> **The Institutional Memory Layer for Enterprise Compliance & Auditor Defense**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Powered by Hindsight](https://img.shields.io/badge/Memory-Vectorize%20Hindsight-6C5CE7.svg)](https://github.com/vectorize-io/hindsight)

---

## 1. Overview

Enterprise software, critical infrastructure, and public-sector organizations spend hundreds of thousands of dollars on annual compliance audits (NIST SP 800-53, FISMA, SOC 2 Type II, ISO 27001). However, audits are not deterministic checklists; they are subjective negotiations between engineering teams and external oversight bodies (GAO, OIG, Schellman, Coalfire, Big 4).

When oversight bodies issue **Audit Findings or Deficiencies** on complex controls (e.g., continuous configuration monitoring drift, legacy system patch delays, cloud tenant governance), engineering teams must implement defensible **remediation plans or compensating controls**.

Because remediation histories, rejected proposals, and technical delays are scattered across historical reports, organizations suffer from **institutional amnesia**:
- New engineers repeatedly propose remediation plans that auditors previously rejected or that caused multi-year schedule slippages.
- Teams fail to leverage historically accepted compensating controls, repeating identical audit findings across cycles.

**ReguGuard** is an AI-powered compliance intelligence agent that remembers historical audit exceptions, auditor precedents, and authentic remediation outcomes—empowering compliance officers and SREs to defend their infrastructure with precedent-backed evidence and eliminate recurring audit friction.

---

## 2. Authentic Public Oversight Dataset

ReguGuard is evaluated on **authentic, publicly documented federal oversight records** with verifiable provenance:
- **GAO-26-107980:** Independent MITRE Corporation assessment of the Department of Veterans Affairs cybersecurity posture (December 2025). Evaluates 11 Programmatic Finding Areas, 5 High-Impact IT Systems, 1,215 vulnerabilities, and 55 planned remediation actions.
- **GAO-23-104705 (CPAG):** Cybersecurity Program Audit Guide defining standard federal audit methodology across Governance, Identify, Protect, Detect, Respond, and Recover.
- **Dual Framework Architecture:** Primary alignment with **NIST SP 800-53 Rev. 5** and **NIST CSF 2.0**, with transparent crosswalks to **SOC 2 Trust Services Criteria (TSC)**.

See [docs/DATASET.md](docs/DATASET.md) for full provenance records, status definitions, and finding inventories.

---

## 3. Core Architecture

```
                                [ Auditor Inquiry / Finding Area ]
                                                │
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. CONTROL INVARIANT PARSER                                                                            │
│    • Maps inquiries to NIST SP 800-53 Rev. 5 (CA-7, CM-2, CM-6, AC-2, SI-2) & SOC 2 Crosswalks (CC6.1) │
│    • Identifies affected resources, framework invariant, and compliance risk                          │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. HINDSIGHT MEMORY RETRIEVAL (recall_async)                                                           │
│    • Queries dedicated Bank ID by control invariant & oversight profile                                │
│    • Retrieves: Authentic remediation records, schedule slippage warnings, accepted precedents         │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 3. DIAGNOSTIC REASONING AGENT (Groq API - Qwen3-32B / Llama 3)                                         │
│    • Synthesizes Evidence-Backed Precedent Briefing:                                                   │
│      - 🟢 Approved Precedent (Official GAO/OIG verification reference)                                 │
│      - 🔴 Anti-Pattern Warning ("DO NOT propose manual reviews; causes recurring milestone slippage") │
│      - Evidence Tier: Confirmed / Likely / Unknown                                                     │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 4. HUMAN-IN-THE-LOOP DEFENSE CONSOLE                                                                   │
│    • SRE / Compliance Officer reviews briefing and clicks: [Generate Remediation Memo]                │
│    • Exports formal defense memorandum citing historical oversight precedents                          │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                             (Post-Audit Determination Received)
                                                │
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 5. HINDSIGHT EXPERIENCE RETENTION (retain_async)                                                       │
│    • Commits new auditor sign-off or remediation outcome into persistent memory for future cycles      │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Project Structure

```
ReguGuard/
├── .env.example               # Environment variables template
├── .gitignore                 # Strict ignore rules (secrets, venv, caches)
├── requirements.txt           # Python backend dependencies
├── README.md                  # Flagship project documentation
├── backend/
│   ├── main.py                # FastAPI entrypoint
│   ├── config.py              # Environment configuration & settings
│   ├── models/
│   │   └── schemas.py         # Pydantic schemas (AuditorInquiry, ControlInvariant, Provenance, etc.)
│   ├── services/
│   │   ├── hindsight_client.py# Vectorize Hindsight API client (retain/recall)
│   │   ├── llm_engine.py      # Groq LLM inference wrapper
│   │   └── control_parser.py  # NIST SP 800-53 & SOC 2 control parser
│   └── routers/
│       ├── audit.py           # Audit defense and triage endpoints
│       └── memory.py          # Memory inspection and real data seeding endpoints
├── data/
│   ├── raw/                   # Raw public oversight reports (GAO-26-107980.html)
│   ├── processed/             # 18 authentic audit records with full provenance
│   ├── metadata/              # Source catalog and audit authority inventory
│   └── evaluation/            # Ground truth benchmark test cases
├── docs/
│   ├── DATASET.md             # Dataset strategy, provenance citations, and status taxonomy
│   ├── ARCHITECTURE.md        # Deep architectural specification
│   ├── DEMO_SCRIPT.md         # 2-session demonstration script
│   └── SOC2_CONTROL_MAPPING.md# NIST SP 800-53 to SOC 2 crosswalk reference
├── scripts/
│   └── build_dataset.py       # Automated authentic dataset extractor and validator
└── tests/
    ├── test_control_parser.py # Unit tests for NIST & SOC 2 control extraction
    ├── test_hindsight_mock.py # Unit tests for Hindsight memory loops
    ├── test_api.py            # Integration tests for FastAPI endpoints
    └── fixtures/              # Test fixtures
```

---

## 5. Getting Started

### Prerequisites
- Python 3.10+
- A Vectorize Hindsight API Key ([Hindsight Cloud](https://ui.hindsight.vectorize.io))
- A Groq API Key ([Groq Console](https://console.groq.com))

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Kathyayini26/ReguGuard.git
cd ReguGuard

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your actual HINDSIGHT_API_KEY and GROQ_API_KEY
```

### Ingesting Authentic Audit Dataset

```bash
# Ingest 18 authentic GAO oversight records into Hindsight memory
curl -X POST http://localhost:8000/api/memory/seed-real-data
```

### Running the Backend

```bash
uvicorn backend.main:app --reload --port 8000
```
Interactive API Documentation will be available at: `http://localhost:8000/docs`

### Running Tests

```bash
pytest -v
```

---

## 6. Official Resources & References

- **GAO-26-107980 Report:** [https://files.gao.gov/reports/GAO-26-107980/index.html](https://files.gao.gov/reports/GAO-26-107980/index.html)
- **GAO Cybersecurity Program Audit Guide (GAO-23-104705):** [https://www.gao.gov/products/gao-23-104705](https://www.gao.gov/products/gao-23-104705)
- **Hindsight Documentation:** [https://hindsight.vectorize.io/](https://hindsight.vectorize.io/)
- **Hindsight GitHub:** [https://github.com/vectorize-io/hindsight](https://github.com/vectorize-io/hindsight)
- **Vectorize Agent Memory:** [https://vectorize.io/what-is-agent-memory](https://vectorize.io/what-is-agent-memory)
