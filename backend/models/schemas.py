from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime, timezone

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class AuditorInquiry(BaseModel):
    """Represents an incoming inquiry or exception raised by an external auditor."""
    inquiry_id: str = Field(..., description="Unique identifier for the inquiry")
    auditor_firm: str = Field(..., description="Name of the external auditing firm (e.g., Schellman, Coalfire, PwC)")
    framework: Literal["SOC2_TYPE_II", "ISO27001", "HIPAA", "PCI_DSS"] = Field("SOC2_TYPE_II", description="Applicable regulatory framework")
    inquiry_text: str = Field(..., description="Exact inquiry or exception narrative provided by the auditor")
    affected_resource: Optional[str] = Field(None, description="System, cluster, or repository identified in the exception")
    severity: Literal["HIGH", "MEDIUM", "LOW"] = Field("MEDIUM", description="Inquiry audit severity")
    timestamp: datetime = Field(default_factory=utc_now)

class ControlInvariant(BaseModel):
    """Canonical regulatory control classification."""
    control_code: str = Field(..., description="Standard control ID (e.g., CC6.1, CC6.3, CC6.8)")
    control_title: str = Field(..., description="Standard title of the control criteria")
    core_risk: str = Field(..., description="Underlying security or compliance risk")
    standard_remediation_expectation: str = Field(..., description="Textbook compliance baseline")

class CompensatingControlPrecedent(BaseModel):
    """Historical compensating control approved by this or similar audit firm."""
    precedent_id: str
    historical_incident_id: str
    auditor_firm: str
    year_accepted: int
    title: str
    description: str
    technical_mechanism: str
    evidence_artifacts_required: List[str]
    confidence_score: float = Field(ge=0.0, le=1.0)

class AntiPatternWarning(BaseModel):
    """Remediation proposal that previously failed or was rejected by auditors."""
    rejected_proposal: str
    rejection_reason: str
    auditor_firm: str
    year_rejected: int
    severity: Literal["CRITICAL", "WARNING"]

class DefenseBriefing(BaseModel):
    """Synthesized defense recommendation presented to the compliance officer."""
    inquiry_id: str
    auditor_firm: str
    control_invariant: ControlInvariant
    evidence_tier: Literal["Confirmed", "Likely", "Unknown"]
    anti_pattern_warning: Optional[AntiPatternWarning] = None
    approved_precedent: Optional[CompensatingControlPrecedent] = None
    recommended_defense_action: str
    rationale: str
    confidence: float

class CompensatingControlMemo(BaseModel):
    """Official formal defense memorandum generated for auditor sign-off."""
    memo_id: str
    inquiry_id: str
    control_code: str
    auditor_firm: str
    target_resource: str
    compensating_control_title: str
    architectural_justification: str
    tamper_proof_evidence_summary: str
    historical_precedent_reference: Optional[str]
    status: Literal["DRAFT", "SUBMITTED", "ACCEPTED", "REJECTED"] = "DRAFT"
    generated_at: datetime = Field(default_factory=utc_now)

class HindsightMemoryRecord(BaseModel):
    """Payload stored into or retrieved from Vectorize Hindsight memory."""
    memory_id: Optional[str] = None
    bank_id: str
    content: str
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)
