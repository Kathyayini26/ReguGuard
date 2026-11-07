import uuid
from fastapi import APIRouter, HTTPException, Depends
from ..models.schemas import (
    AuditorInquiry,
    DefenseBriefing,
    CompensatingControlMemo,
)
from ..services.control_parser import ControlParser
from ..services.hindsight_client import HindsightClient
from ..services.llm_engine import LLMEngine

router = APIRouter(prefix="/api/audit", tags=["Audit Defense & Triage"])

# Shared service instances
hindsight_client = HindsightClient()
llm_engine = LLMEngine()

def get_hindsight():
    return hindsight_client

def get_llm():
    return llm_engine

@router.post("/inquire", response_model=DefenseBriefing)
async def process_auditor_inquiry(
    inquiry: AuditorInquiry,
    hindsight: HindsightClient = Depends(get_hindsight),
    llm: LLMEngine = Depends(get_llm)
):
    """
    Ingests an auditor inquiry, extracts the regulatory control invariant, 
    recalls historical precedents from Hindsight, and synthesizes an evidence-backed defense briefing.
    """
    # 1. Parse regulatory control code (CC6.1, CC6.8, etc.)
    control_invariant = ControlParser.extract_control_invariant(inquiry.inquiry_text)

    # 2. Query Hindsight long-term agent memory
    search_query = f"{inquiry.auditor_firm} {control_invariant.control_code} compensating control exception"
    recalled_memories = await hindsight.recall(
        query=search_query,
        context={"auditor_firm": inquiry.auditor_firm, "control_code": control_invariant.control_code},
        top_k=3
    )

    # 3. Diagnostic reasoning using Groq LLM
    briefing = await llm.generate_defense_briefing(
        inquiry_id=inquiry.inquiry_id,
        auditor_firm=inquiry.auditor_firm,
        inquiry_text=inquiry.inquiry_text,
        control_invariant=control_invariant,
        recalled_memories=recalled_memories
    )

    return briefing

@router.post("/memo/generate", response_model=CompensatingControlMemo)
async def generate_defense_memo(
    briefing: DefenseBriefing,
    target_resource: str = "Staging/Production IAM Roles"
):
    """
    Generates an official Compensating Control Memorandum citing historical precedents.
    """
    precedent_ref = (
        f"Precedent ID: {briefing.approved_precedent.precedent_id} ({briefing.approved_precedent.year_accepted})"
        if briefing.approved_precedent else "Baseline Standard Control"
    )

    memo = CompensatingControlMemo(
        memo_id=f"MEMO-{uuid.uuid4().hex[:8].upper()}",
        inquiry_id=briefing.inquiry_id,
        control_code=briefing.control_invariant.control_code,
        auditor_firm=briefing.auditor_firm,
        target_resource=target_resource,
        compensating_control_title=(
            briefing.approved_precedent.title 
            if briefing.approved_precedent else "Standard Least Privilege Automation"
        ),
        architectural_justification=briefing.rationale,
        tamper_proof_evidence_summary=(
            "Cryptographic CloudTrail digest logs with automated dual-approval GitHub pull request metadata"
        ),
        historical_precedent_reference=precedent_ref,
        status="SUBMITTED"
    )
    return memo
