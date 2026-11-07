import re
from typing import Dict, Any
from ..models.schemas import ControlInvariant

# SOC 2 Trust Services Criteria (TSC) Common Criteria reference mappings
SOC2_CONTROL_CATALOG: Dict[str, Dict[str, str]] = {
    "CC6.1": {
        "control_title": "Logical Access Security & Segregation of Duties",
        "core_risk": "Unauthorized access to production environments or direct developer data tampering",
        "standard_remediation": "Restrict all direct access; enforce strict separation between engineering and production environments",
        "keywords": ["access", "privilege", "admin", "iam", "role", "replica", "direct", "permission", "ssh", "root"]
    },
    "CC6.2": {
        "control_title": "User Registration, Modification, and De-provisioning",
        "core_risk": "Orphaned accounts or delayed offboarding leading to insider threat exposure",
        "standard_remediation": "Mandatory automated de-provisioning within 24 hours of employee departure",
        "keywords": ["offboarding", "provisioning", "deprovisioning", "termination", "inactive", "departed"]
    },
    "CC6.3": {
        "control_title": "Role-Based Access Modification & Periodic Entitlement Review",
        "core_risk": "Privilege creep where users accumulate unneeded permissions across role changes",
        "standard_remediation": "Quarterly documented manager access reviews for all production access",
        "keywords": ["entitlement", "quarterly", "privilege creep", "review", "excessive", "least privilege"]
    },
    "CC6.6": {
        "control_title": "Boundary Protection, Ingress/Egress & Network Segmentation",
        "core_risk": "Unprotected network perimeters allowing lateral movement or public exposure",
        "standard_remediation": "Strict firewall rules, DMZ segregation, and zero public ingress to internal services",
        "keywords": ["network", "perimeter", "firewall", "ingress", "egress", "subnet", "public", "dmz", "vpc"]
    },
    "CC6.8": {
        "control_title": "Malicious Software Prevention & Unauthorized Code Execution",
        "core_risk": "Deploying unreviewed, vulnerable, or malicious packages into production artifacts",
        "standard_remediation": "Branch protection rules requiring automated CI/CD scans and signed commits",
        "keywords": ["vulnerability", "malicious", "dependency", "pull request", "approval", "code review", "cicd"]
    }
}

class ControlParser:
    """Parses natural language auditor inquiries into standard control invariants."""

    @staticmethod
    def extract_control_invariant(inquiry_text: str) -> ControlInvariant:
        """
        Extracts the canonical regulatory control code by keyword density and regex matching.
        """
        text_lower = inquiry_text.lower()
        
        # 1. Direct explicit control code mention (e.g., CC6.1, CC6.8)
        direct_match = re.search(r"\b(cc\d\.\d)\b", text_lower)
        if direct_match:
            code = direct_match.group(1).upper()
            if code in SOC2_CONTROL_CATALOG:
                meta = SOC2_CONTROL_CATALOG[code]
                return ControlInvariant(
                    control_code=code,
                    control_title=meta["control_title"],
                    core_risk=meta["core_risk"],
                    standard_remediation_expectation=meta["standard_remediation"]
                )

        # 2. Heuristic scoring across keyword sets
        best_code = "CC6.1"
        max_score = -1

        for code, meta in SOC2_CONTROL_CATALOG.items():
            score = sum(1 for kw in meta["keywords"] if kw in text_lower)
            if score > max_score:
                max_score = score
                best_code = code

        meta = SOC2_CONTROL_CATALOG[best_code]
        return ControlInvariant(
            control_code=best_code,
            control_title=meta["control_title"],
            core_risk=meta["core_risk"],
            standard_remediation_expectation=meta["standard_remediation"]
        )
