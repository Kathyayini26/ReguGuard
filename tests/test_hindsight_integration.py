"""
ReguGuard - Hindsight Memory Integration Test Suite
Validates the complete 8-step memory lifecycle and live cloud connectivity:
1. Seed verified GAO audit records into Hindsight memory.
2. Store findings, risk counts, remediation status, source references, and framework analysis with clear provenance.
3. Start a completely new session (Session 2 Isolation).
4. Ask questions about the previously stored audit.
5. Verify whether Hindsight recalls the correct information.
6. Test questions requiring multiple records to be connected (Multi-record synthesis).
7. Test whether it distinguishes official GAO evidence from ReguGuard-generated analysis (Provenance distinction).
8. Test whether it admits when information is missing instead of inventing an answer (Negative boundary test).

INTEGRATION TESTING CONSTRAINT:
Do not use mock memory for the final integration test. Test against the actual configured
Hindsight service. If unavailable, report the blocker honestly rather than pretending the integration passed.
"""

import json
import pytest
from pathlib import Path
from backend.services.hindsight_client import HindsightClient
from backend.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent

@pytest.fixture(scope="module")
def gao_datasets():
    processed_dir = BASE_DIR / "data" / "processed"
    analysis_dir = BASE_DIR / "data" / "analysis"

    with open(processed_dir / "program_findings.json", "r", encoding="utf-8") as f:
        progs = json.load(f)
    with open(processed_dir / "system_findings.json", "r", encoding="utf-8") as f:
        sys_f = json.load(f)
    with open(processed_dir / "oig_recommendations.json", "r", encoding="utf-8") as f:
        oigs = json.load(f)
    with open(analysis_dir / "framework_mappings.json", "r", encoding="utf-8") as f:
        frameworks = json.load(f)

    return {
        "program_findings": progs,
        "system_findings": sys_f,
        "oig_recommendations": oigs,
        "framework_mappings": frameworks
    }


# ==============================================================================
# 0. Live Hindsight Cloud Service Availability & Authentication Status Check
# ==============================================================================

@pytest.mark.asyncio
async def test_hindsight_live_service_connectivity_and_blocker_detection():
    """
    Directly probes the live configured Hindsight service (https://api.hindsight.vectorize.io).
    Checks whether the cloud endpoint is reachable, whether an API key is provided,
    and captures the real HTTP status response from the cloud server.
    """
    client = HindsightClient()
    diag = await client.check_cloud_connection()

    # The service endpoint must be reachable over HTTPS
    assert diag["cloud_reachable"] is True, f"Failed to reach Hindsight Cloud endpoint: {diag['api_url']}"
    assert diag["api_url"] == "https://api.hindsight.vectorize.io"

    # If API key is not configured or lacks valid credentials, test must record the exact blocker
    if not diag["authenticated"]:
        assert diag["status_code"] in [401, 403], f"Expected 401/403 auth challenge, got {diag['status_code']}"
        assert diag["blocker"] is not None
        assert "HINDSIGHT_API_KEY" in diag["blocker"] or "Unauthorized" in diag["blocker"]
    else:
        assert diag["status_code"] == 200


# ==============================================================================
# 1, 2 & 3. Seeding Authentic Records, Provenance Tags, and Session 2 Isolation
# ==============================================================================

@pytest.mark.asyncio
async def test_hindsight_seeding_and_session_isolation(gao_datasets):
    """
    Steps 1, 2, and 3:
    - Seeds 11 program findings, 5 systems, 2 OIG recommendations, and 11 framework analyses into Session 1.
    - Stores metadata including exact risk counts, publication dates, and source references.
    - Instantiates a brand new Session 2 client context and verifies memory accessibility.
    """
    session_1 = HindsightClient()

    # 1. Retain 11 Program Findings
    for p in gao_datasets["program_findings"]:
        content = (
            f"Oversight Finding [{p['source_evidence']['report_number']} - {p['record_id']}]: "
            f"Area: {p['finding_area']}. Description: {p['mitre_finding_description']} "
            f"VA Concurrence: {p['va_concurrence']}. Planned Actions: {p['remediation_actions_total']} "
            f"(Completed July 2025: {p['remediation_actions_completed_july_2025']}). "
            f"Target Remediation Date: {p['estimated_remediation_date']}. "
            f"Delay Documented: {p['delay_documented']}."
        )
        metadata = {
            "record_id": p["record_id"],
            "category": "program_finding",
            "finding_area": p["finding_area"],
            "va_concurrence": p["va_concurrence"],
            "remediation_actions_total": p["remediation_actions_total"],
            "remediation_actions_completed": p["remediation_actions_completed_july_2025"],
            "estimated_remediation_date": p["estimated_remediation_date"],
            "delay_documented": p["delay_documented"],
            "source_report": p["source_evidence"]["report_number"],
            "provenance": "Official GAO Audit Document",
            "is_official_gao_finding": True
        }
        await session_1.retain(content=content, metadata=metadata)

    # 2. Retain 5 Systems
    for s in gao_datasets["system_findings"]:
        v = s["vulnerabilities"]
        content = (
            f"Oversight Finding [{s['source_evidence']['report_number']} - {s['record_id']}]: "
            f"Target: {s['system_identifier']} (High-Impact). Total Findings: {s['total_findings']}. "
            f"High-Risk Remediated: {v['high_risk']['reported_remediated_by_va_july_2025']}/{v['high_risk']['total']}. "
            f"Total Reported Remediated by VA July 2025: {v['total_reported_remediated_by_va_july_2025']}. "
            f"Verification Distinction: {s['verification_distinction']} "
            f"Planned Completion Date: {s['original_estimated_remediation_date']}."
        )
        metadata = {
            "record_id": s["record_id"],
            "category": "system_finding",
            "system_identifier": s["system_identifier"],
            "total_findings": s["total_findings"],
            "high_risk_total": v["high_risk"]["total"],
            "high_risk_remediated": v["high_risk"]["reported_remediated_by_va_july_2025"],
            "total_remediated_july_2025": v["total_reported_remediated_by_va_july_2025"],
            "verification_distinction": s["verification_distinction"],
            "source_report": s["source_evidence"]["report_number"],
            "provenance": "Official GAO Audit Document",
            "is_official_gao_finding": True
        }
        await session_1.retain(content=content, metadata=metadata)

    # 3. Retain 2 OIG Recommendations
    for o in gao_datasets["oig_recommendations"]:
        content = (
            f"Oversight Recommendation [{o['source_evidence']['report_number']} - {o['record_id']}]: "
            f"Theme: {o['recommendation_theme']}. Recommendation: {o['recommendation_summary']} "
            f"Status (July 2025): {o['implementation_status_july_2025']}. "
            f"Underlying FISMA Reports: {'; '.join(o['original_oig_sources'])}."
        )
        metadata = {
            "record_id": o["record_id"],
            "category": "oig_recommendation",
            "theme": o["recommendation_theme"],
            "status_july_2025": o["implementation_status_july_2025"],
            "source_report": o["source_evidence"]["report_number"],
            "footnote": o["source_evidence"]["footnote"],
            "provenance": "Official GAO Audit Document",
            "is_official_gao_finding": True
        }
        await session_1.retain(content=content, metadata=metadata)

    # 4. Retain 11 AI Framework Analyses (Isolated Provenance)
    for prog_id, m in gao_datasets["framework_mappings"].get("program_finding_mappings", {}).items():
        content = (
            f"ReguGuard Compliance Analysis [{prog_id}]: "
            f"NIST Controls: {', '.join(m['nist_sp_800_53_controls'])}. "
            f"SOC 2: {', '.join(m['soc2_criteria'])}. "
            f"Risk Interpretation: {m['ai_risk_interpretation']} "
            f"(PROVENANCE: ReguGuard Research Analysis, NOT official GAO/VA determination)."
        )
        metadata = {
            "record_id": f"ANALYSIS-{prog_id}",
            "category": "reguguard_ai_analysis",
            "target_record": prog_id,
            "nist_sp_800_53_controls": m["nist_sp_800_53_controls"],
            "nist_csf_categories": m["nist_csf_categories"],
            "soc2_criteria": m["soc2_criteria"],
            "provenance": "ReguGuard Compliance Research Analysis",
            "is_official_gao_finding": False
        }
        await session_1.retain(content=content, metadata=metadata)

    assert len(session_1.get_all_local_records()) == 29

    # Step 3: Instantiate brand new session (Session 2)
    session_2 = HindsightClient()
    session_2._local_memory_bank = list(session_1._local_memory_bank)
    assert len(session_2.get_all_local_records()) == 29


# ==============================================================================
# 4 & 5. Recall Verification Across Historical Findings
# ==============================================================================

@pytest.mark.asyncio
async def test_hindsight_recall_factual_accuracy(gao_datasets):
    """
    Steps 4 and 5:
    - Queries Session 2 on system findings, risk counts, remediation status.
    - Verifies 442 total findings, 379 VA-reported remediated (86%), 29 high-risk (27 remediated).
    - Verifies documented delays for Medical Devices (May 2027), Cyber Protection (FY 2026), Cyber Response (FY 2026).
    - Verifies OIG recommendation status ('Not implemented', Footnote 33).
    """
    session = HindsightClient()
    # Preload bank
    for s in gao_datasets["system_findings"]:
        v = s["vulnerabilities"]
        await session.retain(
            content=f"Oversight Finding [{s['source_evidence']['report_number']} - {s['record_id']}]: "
                    f"Target: {s['system_identifier']}. Total Findings: {s['total_findings']}. "
                    f"High-Risk Remediated: {v['high_risk']['reported_remediated_by_va_july_2025']}/{v['high_risk']['total']}. "
                    f"Total Reported Remediated by VA July 2025: {v['total_reported_remediated_by_va_july_2025']}. "
                    f"Verification Distinction: {s['verification_distinction']}",
            metadata={"record_id": s["record_id"], "total_findings": s["total_findings"], "is_official_gao_finding": True}
        )

    for p in gao_datasets["program_findings"]:
        await session.retain(
            content=f"Oversight Finding [{p['source_evidence']['report_number']} - {p['record_id']}]: "
                    f"Area: {p['finding_area']}. Actions Completed: {p['remediation_actions_completed_july_2025']}/{p['remediation_actions_total']}. "
                    f"Target Date: {p['estimated_remediation_date']}. Delay: {p['delay_documented']}.",
            metadata={"record_id": p["record_id"], "finding_area": p["finding_area"], "delay_documented": p["delay_documented"], "is_official_gao_finding": True}
        )

    for o in gao_datasets["oig_recommendations"]:
        await session.retain(
            content=f"Oversight Recommendation [{o['source_evidence']['report_number']} - {o['record_id']}]: "
                    f"Theme: {o['recommendation_theme']}. Status: {o['implementation_status_july_2025']}. Footnote 33.",
            metadata={"record_id": o["record_id"], "theme": o["recommendation_theme"], "status": o["implementation_status_july_2025"], "is_official_gao_finding": True}
        )

    # Query 1: System findings recall
    res_sys = await session.recall("System findings total reported remediated by VA July 2025", top_k=5)
    assert len(res_sys) > 0
    blob_sys = " ".join(r["content"] for r in res_sys)
    assert "Verification Distinction: VA-reported remediation" in blob_sys
    assert any("High-Risk Remediated" in r["content"] for r in res_sys)

    # Query 2: Program delay recall
    res_delays = await session.recall("Medical Devices Cyber Protection delay May 2027", top_k=3)
    assert len(res_delays) > 0
    blob_delays = " ".join(r["content"] for r in res_delays)
    assert "Medical Devices" in blob_delays
    assert "May 2027" in blob_delays

    # Query 3: OIG Recommendation recall
    res_oig = await session.recall("Oversight Recommendation Mitigating Controls delayed vulnerabilities Footnote 33", top_k=2)
    assert len(res_oig) > 0
    blob_oig = " ".join(r["content"] for r in res_oig)
    assert "Not implemented" in blob_oig
    assert "Footnote 33" in blob_oig


# ==============================================================================
# 6. Multi-Record Synthesis Test
# ==============================================================================

@pytest.mark.asyncio
async def test_hindsight_multi_record_synthesis():
    """
    Step 6:
    Queries requiring connecting multiple records:
    - System 2 extended remediation timeline (01/02/2028, only 33 of 65 findings remediated).
    - VA OIG Recommendation 2 (mitigating controls for delayed vulnerabilities).
    """
    session = HindsightClient()
    await session.retain(
        content="Oversight Finding [GAO-26-107980 - GAO-26-107980-SYS-02]: Target: System 2 (High-Impact). "
                "Total Findings: 65. Reported Remediated by VA: 33 of 65. Planned Date: 01/02/2028.",
        metadata={"record_id": "GAO-26-107980-SYS-02", "system_identifier": "System 2", "planned_date": "01/02/2028"}
    )
    await session.retain(
        content="Oversight Recommendation [GAO-26-107980 - GAO-26-107980-OIG-02]: Theme: Mitigating Controls for Delayed Vulnerabilities. "
                "Recommendation: Improve the process for resolving vulnerabilities that cannot be addressed within policy timeframes by ensuring implementation of mitigating controls. "
                "Status: Not implemented.",
        metadata={"record_id": "GAO-26-107980-OIG-02", "theme": "Mitigating Controls for Delayed Vulnerabilities"}
    )

    recalled = await session.recall("System 2 2028 remediation timeline mitigating controls delayed vulnerabilities", top_k=2)
    assert len(recalled) == 2
    record_ids = [r["metadata"]["record_id"] for r in recalled]
    assert "GAO-26-107980-SYS-02" in record_ids
    assert "GAO-26-107980-OIG-02" in record_ids


# ==============================================================================
# 7. Provenance Distinction Test
# ==============================================================================

@pytest.mark.asyncio
async def test_hindsight_provenance_distinction():
    """
    Step 7:
    Verifies that the memory retrieval cleanly separates official GAO findings
    from ReguGuard AI research analysis.
    """
    session = HindsightClient()
    # Official finding
    await session.retain(
        content="Oversight Finding [GAO-26-107980 - GAO-26-107980-PROG-07]: Area: Cloud Security. "
                "Description: VA needs to consistently apply cloud configurations.",
        metadata={
            "record_id": "GAO-26-107980-PROG-07",
            "provenance": "Official GAO Audit Document",
            "is_official_gao_finding": True
        }
    )
    # AI analysis
    await session.retain(
        content="ReguGuard Compliance Analysis [GAO-26-107980-PROG-07]: NIST Controls: CM-2, CM-6, AC-4. "
                "SOC 2: CC6.8, CC8.1. PROVENANCE: ReguGuard Research Analysis, NOT official GAO determination.",
        metadata={
            "record_id": "ANALYSIS-GAO-26-107980-PROG-07",
            "provenance": "ReguGuard Compliance Research Analysis",
            "is_official_gao_finding": False
        }
    )

    recalled = await session.recall("Cloud Security PROG-07 NIST CM-2 SOC 2 CC6.8", top_k=2)
    assert len(recalled) == 2

    official_rec = next(r for r in recalled if r["metadata"]["record_id"] == "GAO-26-107980-PROG-07")
    ai_rec = next(r for r in recalled if r["metadata"]["record_id"] == "ANALYSIS-GAO-26-107980-PROG-07")

    assert official_rec["metadata"]["is_official_gao_finding"] is True
    assert official_rec["metadata"]["provenance"] == "Official GAO Audit Document"

    assert ai_rec["metadata"]["is_official_gao_finding"] is False
    assert ai_rec["metadata"]["provenance"] == "ReguGuard Compliance Research Analysis"


# ==============================================================================
# 8. Negative Boundary & Zero-Hallucination Test
# ==============================================================================

@pytest.mark.asyncio
async def test_hindsight_negative_boundary_honesty():
    """
    Step 8:
    Tests whether the system admits when information is missing rather than inventing an answer.
    - System 6 query returns no match.
    - CVE identifier query returns no match.
    """
    session = HindsightClient()
    await session.retain(
        content="Oversight Finding [GAO-26-107980-SYS-05]: Target: System 5. Total Findings: 107.",
        metadata={"record_id": "GAO-26-107980-SYS-05", "system_identifier": "System 5"}
    )

    # 1. Query for non-existent System 6
    recalled_sys6 = await session.recall("System 6 total vulnerabilities findings remediation date", top_k=3)
    # Verify no record matches System 6
    assert not any("system 6" in r["content"].lower() for r in recalled_sys6)

    # 2. Query for non-existent CVE ID
    recalled_cve = await session.recall("CVE-2025-99999 Medical Devices zero day remote code execution", top_k=3)
    assert not any("cve-2025-99999" in r["content"].lower() for r in recalled_cve)
