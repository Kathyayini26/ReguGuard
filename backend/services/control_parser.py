import re
from typing import Dict, Any
from ..models.schemas import ControlInvariant

# NIST SP 800-53 Rev. 5 & SOC 2 Crosswalk Control Catalog
NIST_CONTROL_CATALOG: Dict[str, Dict[str, Any]] = {
    "CA-7": {
        "control_title": "Continuous Monitoring",
        "framework": "NIST_SP_800_53_REV5",
        "core_risk": "Lack of timely visibility into asset state, vulnerabilities, and unauthorized changes",
        "standard_remediation": "Deploy continuous automated vulnerability scanning, configuration assessments, and active risk monitoring",
        "soc2_crosswalk": ["CC7.1", "CC7.2"],
        "keywords": ["continuous monitoring", "control assessment", "vulnerability scan", "software management", "scanning", "assessment", "ca-7"]
    },
    "CM-2": {
        "control_title": "Baseline Configuration",
        "framework": "NIST_SP_800_53_REV5",
        "core_risk": "Undocumented system states, unapproved baseline drifts, and unmanaged cloud tenant resources",
        "standard_remediation": "Establish and document baseline configurations with automated policy-as-code enforcement",
        "soc2_crosswalk": ["CC6.8", "CC8.1"],
        "keywords": ["baseline configuration", "cloud configuration", "cloud security", "drift", "cm-2"]
    },
    "CM-6": {
        "control_title": "Configuration Settings",
        "framework": "NIST_SP_800_53_REV5",
        "core_risk": "Weak default configurations, open ports, and non-compliant cloud tenant settings",
        "standard_remediation": "Enforce mandatory hardening baselines, automated policy-as-code validation, and continuous configuration compliance scanning",
        "soc2_crosswalk": ["CC6.6", "CC6.8"],
        "keywords": ["configuration settings", "compliance", "hardening", "cloud tenant", "cm-6"]
    },
    "AC-2": {
        "control_title": "Account Management",
        "framework": "NIST_SP_800_53_REV5",
        "core_risk": "Orphaned accounts, delayed de-provisioning, and unauthorized account creation",
        "standard_remediation": "Automate user account provisioning, lifecycle tracking, and mandatory de-provisioning upon role change or termination",
        "soc2_crosswalk": ["CC6.1", "CC6.2"],
        "keywords": ["account management", "identity", "offboarding", "deprovisioning", "user account", "ac-2"]
    },
    "AC-6": {
        "control_title": "Least Privilege",
        "framework": "NIST_SP_800_53_REV5",
        "core_risk": "Excessive administrative rights and absence of segregation of duties",
        "standard_remediation": "Enforce role-based access control, ephemeral credentials, and automated peer review for privilege escalation",
        "soc2_crosswalk": ["CC6.1", "CC6.3"],
        "keywords": ["least privilege", "privilege creep", "admin", "excessive", "segregation of duties", "ac-6"]
    },
    "SC-7": {
        "control_title": "Boundary Protection",
        "framework": "NIST_SP_800_53_REV5",
        "core_risk": "Uncontrolled network perimeters, unsegmented VPCs, and unauthorized egress paths",
        "standard_remediation": "Implement managed network interfaces, micro-segmentation, and egress filtering with cryptographic inspection",
        "soc2_crosswalk": ["CC6.6"],
        "keywords": ["boundary protection", "network", "firewall", "perimeter", "segmentation", "sc-7"]
    },
    "SI-2": {
        "control_title": "Flaw Remediation",
        "framework": "NIST_SP_800_53_REV5",
        "core_risk": "Unpatched known vulnerabilities (CVEs) persisting in production systems",
        "standard_remediation": "Mandate patch remediation SLAs: 30 days for Critical/High, 90 days for Moderate, with POA&M milestone tracking",
        "soc2_crosswalk": ["CC7.1", "CC7.4"],
        "keywords": ["flaw remediation", "patch", "vulnerability remediation", "cve", "poa&m", "plan of action", "si-2"]
    },
    "PM-4": {
        "control_title": "Plan of Action and Milestones (POA&M) Process",
        "framework": "NIST_SP_800_53_REV5",
        "core_risk": "Unmonitored remediation backlogs, recurring milestone slippage, and unmitigated security debts",
        "standard_remediation": "Maintain central enterprise POA&M tracking with monthly status verification and automated closure reviews",
        "soc2_crosswalk": ["CC7.4"],
        "keywords": ["poa&m", "plan of action and milestones", "milestone", "schedule slippage", "pm-4"]
    }
}

# SOC 2 Trust Services Criteria (TSC) Common Criteria reference mappings
SOC2_CONTROL_CATALOG: Dict[str, Dict[str, Any]] = {
    "CC6.1": {
        "control_title": "Logical Access Security & Segregation of Duties",
        "framework": "SOC2_TYPE_II",
        "core_risk": "Unauthorized access to production environments or direct developer data tampering",
        "standard_remediation": "Restrict all direct access; enforce strict separation between engineering and production environments",
        "soc2_crosswalk": ["CC6.1"],
        "keywords": ["access", "privilege", "admin", "iam", "role", "replica", "direct", "permission", "ssh", "root"]
    },
    "CC6.2": {
        "control_title": "User Registration, Modification, and De-provisioning",
        "framework": "SOC2_TYPE_II",
        "core_risk": "Orphaned accounts or delayed offboarding leading to insider threat exposure",
        "standard_remediation": "Mandatory automated de-provisioning within 24 hours of employee departure",
        "soc2_crosswalk": ["CC6.2"],
        "keywords": ["offboarding", "provisioning", "deprovisioning", "termination", "inactive", "departed"]
    },
    "CC6.3": {
        "control_title": "Role-Based Access Modification & Periodic Entitlement Review",
        "framework": "SOC2_TYPE_II",
        "core_risk": "Privilege creep where users accumulate unneeded permissions across role changes",
        "standard_remediation": "Quarterly documented manager access reviews for all production access",
        "soc2_crosswalk": ["CC6.3"],
        "keywords": ["entitlement", "quarterly", "privilege creep", "review", "excessive", "least privilege"]
    },
    "CC6.6": {
        "control_title": "Boundary Protection, Ingress/Egress & Network Segmentation",
        "framework": "SOC2_TYPE_II",
        "core_risk": "Unprotected network perimeters allowing lateral movement or public exposure",
        "standard_remediation": "Strict firewall rules, DMZ segregation, and zero public ingress to internal services",
        "soc2_crosswalk": ["CC6.6"],
        "keywords": ["network", "perimeter", "firewall", "ingress", "egress", "subnet", "public", "dmz", "vpc"]
    },
    "CC6.8": {
        "control_title": "Malicious Software Prevention & Unauthorized Code Execution",
        "framework": "SOC2_TYPE_II",
        "core_risk": "Deploying unreviewed, vulnerable, or malicious packages into production artifacts",
        "standard_remediation": "Branch protection rules requiring automated CI/CD scans and signed commits",
        "soc2_crosswalk": ["CC6.8"],
        "keywords": ["vulnerability", "malicious", "dependency", "pull request", "approval", "code review", "cicd"]
    }
}

class ControlParser:
    """Parses natural language auditor inquiries into standard control invariants (NIST & SOC 2)."""

    @staticmethod
    def extract_control_invariant(inquiry_text: str) -> ControlInvariant:
        """
        Extracts the canonical regulatory control code by keyword density and regex matching.
        Supports both NIST SP 800-53 (e.g. CA-7, CM-6, SC-7) and SOC 2 TSC (e.g. CC6.1, CC6.8).
        """
        text_lower = inquiry_text.lower()
        
        # 1. Direct explicit NIST SP 800-53 control code mention (e.g., CA-7, CM-6, AC-2, SI-2, SC-7, PM-4)
        nist_match = re.search(r"\b([a-z]{2}-\d{1,2})\b", text_lower)
        if nist_match:
            code = nist_match.group(1).upper()
            if code in NIST_CONTROL_CATALOG:
                meta = NIST_CONTROL_CATALOG[code]
                return ControlInvariant(
                    control_code=code,
                    control_title=meta["control_title"],
                    framework=meta["framework"],
                    core_risk=meta["core_risk"],
                    standard_remediation_expectation=meta["standard_remediation"],
                    soc2_crosswalk=meta.get("soc2_crosswalk", [])
                )

        # 2. Direct explicit SOC 2 control code mention (e.g., CC6.1, CC6.8)
        soc2_match = re.search(r"\b(cc\d\.\d)\b", text_lower)
        if soc2_match:
            code = soc2_match.group(1).upper()
            if code in SOC2_CONTROL_CATALOG:
                meta = SOC2_CONTROL_CATALOG[code]
                return ControlInvariant(
                    control_code=code,
                    control_title=meta["control_title"],
                    framework=meta["framework"],
                    core_risk=meta["core_risk"],
                    standard_remediation_expectation=meta["standard_remediation"],
                    soc2_crosswalk=[code]
                )

        # 3. Heuristic scoring across combined catalog
        combined_catalog = {**NIST_CONTROL_CATALOG, **SOC2_CONTROL_CATALOG}
        best_code = "CA-7"
        max_score = -1

        for code, meta in combined_catalog.items():
            score = sum(1 for kw in meta["keywords"] if kw in text_lower)
            if score > max_score:
                max_score = score
                best_code = code

        meta = combined_catalog[best_code]
        return ControlInvariant(
            control_code=best_code,
            control_title=meta["control_title"],
            framework=meta["framework"],
            core_risk=meta["core_risk"],
            standard_remediation_expectation=meta["standard_remediation"],
            soc2_crosswalk=meta.get("soc2_crosswalk", [best_code] if best_code.startswith("CC") else [])
        )
