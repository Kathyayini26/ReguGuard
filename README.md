# ReguGuard: The Experiential Audit Intelligence Agent

> **The Institutional Memory Layer for Enterprise Compliance & Auditor Defense**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Powered by Hindsight](https://img.shields.io/badge/Memory-Vectorize%20Hindsight-6C5CE7.svg)](https://github.com/vectorize-io/hindsight)

---

## 1. Overview

Enterprise software and FinTech organizations spend hundreds of thousands of dollars on annual compliance audits (SOC 2 Type II, ISO 27001, HIPAA, PCI-DSS). However, third-party audits are not deterministic checklists; they are subjective negotiations between company engineers and external human audit firms (e.g., Schellman, Coalfire, Big 4).

When auditors issue **Management Exceptions** on ambiguous controls (e.g., direct engineer access to production replicas, shared service credentials), engineering teams must defend their architecture using **approved compensating controls**.

Because audit defense histories, negotiated exceptions, and auditor preferences are lost across annual cycles and team turnover, organizations suffer from **institutional amnesia**:
- New engineers repeatedly propose remediation plans that auditors previously rejected.
- Teams waste months re-architecting systems that were already covered by previously approved compensating controls.

**ReguGuard** is an AI-powered compliance intelligence agent that remembers historical audit exceptions, auditor firm preferences, and accepted compensating controls—empowering companies to defend their infrastructure with precedent-backed evidence and eliminate recurring audit friction.

---

## 2. Core Architecture

```
                                [ Auditor Inquiry / Management Exception ]
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. CONTROL INVARIANT PARSER                                                                            │
│    • Maps inquiries to standard regulatory frameworks (AICPA SOC 2 CC6.1 - CC6.8, NIST SP 800-53)      │
│    • Identifies affected resources and core compliance risk                                           │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. HINDSIGHT MEMORY RETRIEVAL (recall_async)                                                           │
│    • Queries dedicated Bank ID by control invariant & auditor firm profile                             │
│    • Retrieves: Historical auditor determinations, approved compensating controls, rejected proposals │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 3. DIAGNOSTIC REASONING AGENT (Groq API - Qwen3-32B / GPT-OSS-120B)                                    │
│    • Synthesizes Evidence-Backed Precedent Briefing:                                                   │
│      - 🟢 Approved Compensating Control (Precedent reference)                                         │
│      - 🔴 Anti-Pattern Warning ("DO NOT propose X; firm rejected this in 2025")                        │
│      - Evidence Tier: Confirmed / Likely / Unknown                                                     │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 4. HUMAN-IN-THE-LOOP DEFENSE CONSOLE                                                                   │
│    • SRE / Compliance Lead reviews precedent and clicks: [Generate Compensating Control Memo]         │
│    • Exports formal auditor defense memorandum ready for sign-off                                      │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
                                 (Post-Audit Determination Received)
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 5. HINDSIGHT EXPERIENCE RETENTION (retain_async)                                                       │
│    • Commits new auditor sign-off or rejection into persistent memory for next year's cycle           │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Project Structure

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
│   │   └── schemas.py         # Pydantic schemas (Inquiry, DefenseMemo, etc.)
│   ├── services/
│   │   ├── hindsight_client.py# Vectorize Hindsight API client (retain/recall)
│   │   ├── llm_engine.py      # Groq LLM inference wrapper
│   │   └── control_parser.py  # Regulatory control invariant extractor
│   └── routers/
│       ├── audit.py           # Audit defense and triage endpoints
│       └── memory.py          # Memory inspection and retention endpoints
├── docs/
│   ├── ARCHITECTURE.md        # Deep architectural specification
│   ├── DEMO_SCRIPT.md         # 2-session before-and-after demonstration script
│   └── SOC2_CONTROL_MAPPING.md# AICPA Trust Services Criteria reference
├── tests/
│   ├── test_control_parser.py # Unit tests for control invariant extraction
│   ├── test_hindsight_mock.py # Unit tests for Hindsight memory loops
│   └── test_api.py            # FastAPI integration tests
└── synthetic_data/
    ├── audit_scenarios.json   # Multi-session audit demonstration scenarios
    └── soc2_baseline_controls.json # Verified baseline compensating control catalog
```

---

## 4. Getting Started

### Prerequisites
- Python 3.10+
- A Vectorize Hindsight API Key ([Hindsight Cloud](https://ui.hindsight.vectorize.io))
- A Groq API Key ([Groq Console](https://console.groq.com))

### Installation

```bash
# 1. Clone repository
git clone https://github.com/kathy20075/ReguGuard.git
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

### Running the Backend

```bash
uvicorn backend.main:app --reload --port 8000
```
API Documentation will be available at: `http://localhost:8000/docs`

### Running Tests

```bash
pytest -v
```

---

## 5. Demonstration Workflow

1. **Session 1 (Learning Phase):** An auditor issues an exception on staging IAM access. A junior engineer's manual spreadsheet proposal is rejected. A senior CISO negotiates an automated tamper-evident KMS log control that the auditor accepts. The episode is retained in Hindsight.
2. **Session 2 (Recall Phase):** In next year's audit, a different auditor from the same firm raises a similar exception. ReguGuard triggers `recall()`, issues an **Anti-Pattern Warning** against the manual spreadsheet, and generates an official Compensating Control Memorandum citing the approved precedent.

---

## 6. Official Resources & References

- **Hindsight Documentation:** [https://hindsight.vectorize.io/](https://hindsight.vectorize.io/)
- **Hindsight GitHub:** [https://github.com/vectorize-io/hindsight](https://github.com/vectorize-io/hindsight)
- **Vectorize Agent Memory:** [https://vectorize.io/what-is-agent-memory](https://vectorize.io/what-is-agent-memory)
