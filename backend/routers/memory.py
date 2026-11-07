from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from ..services.hindsight_client import HindsightClient
from ..models.schemas import HindsightMemoryRecord

router = APIRouter(prefix="/api/memory", tags=["Hindsight Memory"])

# Reference shared client from audit router
from .audit import get_hindsight

@router.post("/retain")
async def retain_memory_record(
    content: str,
    metadata: Dict[str, Any],
    hindsight: HindsightClient = Depends(get_hindsight)
):
    """
    Persistently stores an audit outcome into Hindsight memory.
    """
    success = await hindsight.retain(content=content, metadata=metadata)
    return {"status": "success" if success else "failed", "content": content, "metadata": metadata}

@router.get("/inspect", response_model=List[HindsightMemoryRecord])
async def inspect_memory(hindsight: HindsightClient = Depends(get_hindsight)):
    """
    Inspects all historical memories stored in the local session bank.
    """
    return hindsight.get_all_local_records()

@router.post("/seed")
async def seed_demo_memory(hindsight: HindsightClient = Depends(get_hindsight)):
    """
    Pre-populates the Hindsight bank with Session 1 audit history:
    - Rejection of manual spreadsheet proposal by Schellman in 2025.
    - Approval of automated KMS CloudTrail digest compensating control.
    """
    # 1. Store the rejected proposal (Anti-Pattern)
    await hindsight.retain(
        content=(
            "Audit Finding 2025: Auditor Schellman REJECTED manual spreadsheet reviews for CC6.1. "
            "Verdict: Manual sheets lack cryptographic tamper-evidence and cannot be verified independently."
        ),
        metadata={
            "outcome": "REJECTED",
            "auditor_firm": "Schellman",
            "control_code": "CC6.1",
            "year": 2025,
            "proposal": "Manual spreadsheet access review sheet",
            "reason": "Lacks cryptographic tamper-evidence and independent auditability under CC6.1"
        }
    )

    # 2. Store the approved compensating control (Precedent)
    await hindsight.retain(
        content=(
            "Audit Determination 2025: Auditor Schellman ACCEPTED Automated Ephemeral KMS Log Pipeline under CC6.1. "
            "Technical mechanism: AWS CloudTrail + KMS digest verification with GitHub Actions dual-approval peer gate. "
            "Evidence: Cryptographic CloudTrail digest logs."
        ),
        metadata={
            "outcome": "ACCEPTED",
            "auditor_firm": "Schellman",
            "control_code": "CC6.1",
            "year": 2025,
            "precedent_id": "PREC-CC61-01",
            "title": "Automated Ephemeral KMS Log Pipeline",
            "description": "Automated dual-approval ephemeral IAM role logged to tamper-proof S3 bucket with KMS digest verification"
        }
    )

    return {"status": "seeded", "message": "Successfully seeded Session 1 historical memory into Hindsight"}

@router.post("/seed-real-data")
async def seed_real_audit_data(hindsight: HindsightClient = Depends(get_hindsight)):
    """
    Ingests all 18 authentic records from GAO-26-107980:
    - 11 Program Findings (program_findings.json)
    - 5 Anonymised High-Impact Systems (system_findings.json)
    - 2 VA OIG Recommendations (oig_recommendations.json)
    Preserves exact reported numbers, dates, and source evidence.
    """
    import json
    from pathlib import Path

    processed_dir = Path(__file__).resolve().parent.parent.parent / "data" / "processed"
    prog_file = processed_dir / "program_findings.json"
    sys_file = processed_dir / "system_findings.json"
    oig_file = processed_dir / "oig_recommendations.json"

    if not (prog_file.exists() and sys_file.exists() and oig_file.exists()):
        return {"status": "error", "message": "One or more authentic dataset files are missing in data/processed"}

    with open(prog_file, "r", encoding="utf-8") as f:
        prog_records = json.load(f)
    with open(sys_file, "r", encoding="utf-8") as f:
        sys_records = json.load(f)
    with open(oig_file, "r", encoding="utf-8") as f:
        oig_records = json.load(f)

    loaded_count = 0

    # 1. Ingest 11 Program Findings
    for p in prog_records:
        content = (
            f"Oversight Finding [{p['source_evidence']['report_number']} - {p['record_id']}]: "
            f"Area: {p['finding_area']}. Description: {p['mitre_finding_description']} "
            f"VA Concurrence: {p['va_concurrence']}. Planned Actions: {p['remediation_actions_total']} "
            f"(Completed July 2025: {p['remediation_actions_completed_july_2025']}). "
            f"Target Remediation Date: {p['estimated_remediation_date']}."
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
            "source_tables": p["source_evidence"]["tables"],
            "source_url": p["source_evidence"]["source_url"]
        }
        await hindsight.retain(content=content, metadata=metadata)
        loaded_count += 1

    # 2. Ingest 5 Anonymised Systems
    for s in sys_records:
        v = s["vulnerabilities"]
        content = (
            f"Oversight Finding [{s['source_evidence']['report_number']} - {s['record_id']}]: "
            f"Target: {s['system_identifier']} (High-Impact). Total Findings: {s['total_findings']}. "
            f"High-Risk Remediated (VA-Reported): {v['high_risk']['reported_remediated_by_va_july_2025']}/{v['high_risk']['total']}. "
            f"Moderate-Risk Remediated (VA-Reported): {v['moderate_risk']['reported_remediated_by_va_july_2025']}/{v['moderate_risk']['total']}. "
            f"Low-Risk Remediated (VA-Reported): {v['low_risk']['reported_remediated_by_va_july_2025']}/{v['low_risk']['total']}. "
            f"Total Reported Remediated by VA July 2025: {v['total_reported_remediated_by_va_july_2025']}. "
            f"Verification Distinction: {s['verification_distinction']} "
            f"Planned Completion Date: {s['original_estimated_remediation_date']}."
        )
        metadata = {
            "record_id": s["record_id"],
            "category": "system_finding",
            "system_identifier": s["system_identifier"],
            "total_findings": s["total_findings"],
            "total_remediated_july_2025": v["total_reported_remediated_by_va_july_2025"],
            "reported_remediated_count": v["reported_remediated_count"],
            "verification_distinction": s["verification_distinction"],
            "planned_date": s["original_estimated_remediation_date"],
            "source_report": s["source_evidence"]["report_number"],
            "source_tables": s["source_evidence"]["tables"],
            "source_url": s["source_evidence"]["source_url"]
        }
        await hindsight.retain(content=content, metadata=metadata)
        loaded_count += 1

    # 3. Ingest 2 OIG Recommendations
    for o in oig_records:
        content = (
            f"Oversight Recommendation [{o['source_evidence']['report_number']} - {o['record_id']}]: "
            f"Issuing Body: {o['issuing_body']}. Evaluated by: {o['evaluating_body']}. "
            f"Recommendation: {o['recommendation_summary']} "
            f"Status (July 2025): {o['implementation_status_july_2025']}."
        )
        metadata = {
            "record_id": o["record_id"],
            "category": "oig_recommendation",
            "issuing_body": o["issuing_body"],
            "status_july_2025": o["implementation_status_july_2025"],
            "source_report": o["source_evidence"]["report_number"],
            "source_url": o["source_evidence"]["source_url"]
        }
        await hindsight.retain(content=content, metadata=metadata)
        loaded_count += 1

    return {
        "status": "success",
        "ingested_records": loaded_count,
        "breakdown": {
            "program_findings": len(prog_records),
            "system_findings": len(sys_records),
            "oig_recommendations": len(oig_records)
        },
        "primary_source": "GAO-26-107980",
        "message": f"Successfully ingested {loaded_count} authentic audit records into Hindsight memory"
    }


