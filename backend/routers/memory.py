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
    Ingests all 18 authentic public oversight records (GAO-26-107980, CPAG GAO-23-104705, etc.)
    into Vectorize Hindsight memory with complete verifiable provenance.
    """
    import json
    from pathlib import Path

    findings_file = Path(__file__).resolve().parent.parent.parent / "data" / "processed" / "real_audit_findings.json"
    if not findings_file.exists():
        return {"status": "error", "message": f"Dataset file not found at {findings_file}"}

    with open(findings_file, "r", encoding="utf-8") as f:
        records = json.load(f)

    loaded_count = 0
    for item in records:
        content = (
            f"Audit Finding [{item['report_number']} - {item['id']}]: "
            f"Agency: {item['agency']}. Finding Area: {item['finding_area']}. "
            f"Weakness: {item['identified_weakness']} "
            f"Auditor Recommendation: {item['auditor_recommendation']} "
            f"Remediation Action: {item['remediation_action']} "
            f"Status: {item['implementation_status']} ({item['status_details']}). "
            f"Primary Controls: {', '.join(item['framework_reference']['control_codes'])}."
        )
        metadata = {
            "record_id": item["id"],
            "agency": item["agency"],
            "report_number": item["report_number"],
            "publication_date": item["publication_date"],
            "finding_area": item["finding_area"],
            "implementation_status": item["implementation_status"],
            "status_details": item["status_details"],
            "control_codes": item["framework_reference"]["control_codes"],
            "soc2_crosswalk": item["framework_reference"]["soc2_crosswalk"],
            "provenance_url": item["provenance"]["source_url"],
            "provenance_section": item["provenance"]["page_or_section"]
        }
        await hindsight.retain(content=content, metadata=metadata)
        loaded_count += 1

    return {
        "status": "success",
        "ingested_records": loaded_count,
        "primary_source": "GAO-26-107980 & GAO-23-104705",
        "message": f"Successfully ingested {loaded_count} authentic audit records into Hindsight memory"
    }

