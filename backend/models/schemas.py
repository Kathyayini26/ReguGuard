from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime, timezone

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class AuditorInquiry(BaseModel):
    """Represents an incoming inquiry, deficiency, or finding raised by an oversight body or auditor."""
    inquiry_id: str = Field(..., description="Unique identifier for the inquiry")
    auditor_firm: str = Field(..., description="Name of the auditing body (e.g., GAO, OIG, Schellman, Coalfire, PwC)")
    framework: Literal["NIST_SP_800_53_REV5", "NIST_CSF_2_0", "SOC2_TYPE_II", "ISO27001", "FISMA"] = Field(
        "NIST_SP_800_53_REV5", 
        description="Applicable regulatory framework"
    )
    inquiry_text: str = Field(..., description="Exact finding, exception narrative, or inquiry text")
    affected_resource: Optional[str] = Field(None, description="System, agency, cloud tenant, or repository identified")
    severity: Literal["HIGH", "MODERATE", "LOW", "MEDIUM"] = Field("MODERATE", description="Audit finding severity")
    timestamp: datetime = Field(default_factory=utc_now)

class ControlInvariant(BaseModel):
    """Canonical regulatory control classification (NIST SP 800-53 with SOC 2 crosswalk)."""
    control_code: str = Field(..., description="Primary control ID (e.g., CA-7, CM-6, CC6.1, AC-2)")
    control_title: str = Field(..., description="Standard title of the control criteria")
    framework: str = Field("NIST_SP_800_53_REV5", description="Primary framework for this control")
    core_risk: str = Field(..., description="Underlying security or compliance risk")
    standard_remediation_expectation: str = Field(..., description="Standard compliance baseline expectation")
    soc2_crosswalk: Optional[List[str]] = Field(default_factory=list, description="Crosswalk to SOC 2 Trust Services Criteria")

class AuditProvenance(BaseModel):
    """Verifiable public provenance metadata for authentic oversight records."""
    source_url: str
    source_type: str
    page_or_section: str
    report_number: Optional[str] = None
    extracted_at: Optional[str] = None

class CompensatingControlPrecedent(BaseModel):
    """Historical remediation precedent or compensating control documented in oversight reports."""
    precedent_id: str
    historical_incident_id: str
    auditor_firm: str
    year_accepted: int
    title: str
    description: str
    technical_mechanism: str
    evidence_artifacts_required: List[str]
    implementation_status: Literal[
        "Open / Not implemented",
        "Resolved / Agreed to implement",
        "Implemented / Closed",
        "Partially implemented",
        "Pending verification",
        "Unknown / Not publicly documented"
    ] = "Implemented / Closed"
    confidence_score: float = Field(ge=0.0, le=1.0)
    provenance: Optional[AuditProvenance] = None

class AntiPatternWarning(BaseModel):
    """Remediation proposal or implementation failure that caused audit findings or schedule delays."""
    rejected_proposal: str
    rejection_reason: str
    auditor_firm: str
    year_rejected: int
    severity: Literal["CRITICAL", "WARNING"]
    provenance_reference: Optional[str] = None

class DefenseBriefing(BaseModel):
    """Synthesized defense recommendation and experiential analysis presented to compliance/security teams."""
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
    """Official formal defense or remediation memorandum citing historical precedent and audit evidence."""
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
