"""
Automated Validation Tests for ReguGuard Authentic Oversight Datasets
Validates exact figures against GAO Report GAO-26-107980:
- 442 total system findings across Systems 1-5.
- 29 high-risk, 155 moderate-risk, 258 low-risk vulnerabilities.
- 379 VA-reported remediated findings (not labeled independently closed).
- 11 program finding areas.
- 55 total program actions, 20 completed as of July 2025.
- Official publication date: December 11, 2025.
- Zero missing source provenance or unverified claims.
- System 1-5 anonymisation integrity.
- Two distinct VA OIG recommendation themes with FY23 and FY24 FISMA citations.
"""

import json
from pathlib import Path
import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"
ANALYSIS_DIR = DATA_DIR / "analysis"

@pytest.fixture(scope="module")
def program_findings():
    with open(PROCESSED_DIR / "program_findings.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="module")
def system_findings():
    with open(PROCESSED_DIR / "system_findings.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="module")
def oig_recommendations():
    with open(PROCESSED_DIR / "oig_recommendations.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="module")
def framework_analysis():
    with open(ANALYSIS_DIR / "framework_mappings.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ==============================================================================
# 1. Official Report Publication Date & Provenance Tests
# ==============================================================================

def test_publication_date_consistency(program_findings, system_findings, oig_recommendations, framework_analysis):
    """Verifies that the publication date is strictly December 11, 2025 everywhere."""
    expected_date = "December 11, 2025"

    for p in program_findings:
        assert p["source_evidence"]["publication_date"] == expected_date
        assert p["source_evidence"]["report_number"] == "GAO-26-107980"
        assert p["source_evidence"]["source_url"] == "https://files.gao.gov/reports/GAO-26-107980/index.html"

    for s in system_findings:
        assert s["source_evidence"]["publication_date"] == expected_date
        assert s["source_evidence"]["report_number"] == "GAO-26-107980"
        assert s["source_evidence"]["source_url"] == "https://files.gao.gov/reports/GAO-26-107980/index.html"

    for o in oig_recommendations:
        assert o["source_evidence"]["publication_date"] == expected_date
        assert o["source_evidence"]["report_number"] == "GAO-26-107980"
        assert o["source_evidence"]["source_url"] == "https://files.gao.gov/reports/GAO-26-107980/index.html"

    assert framework_analysis["analysis_metadata"]["publication_date"] == expected_date
    assert framework_analysis["analysis_metadata"]["report_evaluated"] == "GAO-26-107980"

# ==============================================================================
# 2. Dataset B: System Findings Validation (442 Total, 29/155/258, 379 Remediated)
# ==============================================================================

def test_system_findings_counts_and_risk_breakdown(system_findings):
    """
    Verifies Table 3 and Table 5 figures:
    - 5 anonymised systems (System 1 to System 5).
    - 442 total findings.
    - 29 high-risk, 155 moderate-risk, 258 low-risk vulnerabilities.
    - 379 VA-reported remediated findings.
    """
    assert len(system_findings) == 5

    expected_systems = ["System 1", "System 2", "System 3", "System 4", "System 5"]
    actual_systems = [s["system_identifier"] for s in system_findings]
    assert actual_systems == expected_systems

    total_findings = sum(s["total_findings"] for s in system_findings)
    assert total_findings == 442, f"Expected 442 total findings, got {total_findings}"

    # Verify Table 3 per-system counts: 107, 65, 107, 56, 107
    expected_per_system = [107, 65, 107, 56, 107]
    assert [s["total_findings"] for s in system_findings] == expected_per_system

    # Verify risk breakdown across all 5 systems
    total_high = sum(s["vulnerabilities"]["high_risk"]["total"] for s in system_findings)
    total_mod = sum(s["vulnerabilities"]["moderate_risk"]["total"] for s in system_findings)
    total_low = sum(s["vulnerabilities"]["low_risk"]["total"] for s in system_findings)

    assert total_high == 29, f"Expected 29 high-risk vulnerabilities, got {total_high}"
    assert total_mod == 155, f"Expected 155 moderate-risk vulnerabilities, got {total_mod}"
    assert total_low == 258, f"Expected 258 low-risk vulnerabilities, got {total_low}"
    assert total_high + total_mod + total_low == 442

    # Verify VA-reported remediation progress (Table 5)
    high_remediated = sum(s["vulnerabilities"]["high_risk"]["reported_remediated_by_va_july_2025"] for s in system_findings)
    mod_remediated = sum(s["vulnerabilities"]["moderate_risk"]["reported_remediated_by_va_july_2025"] for s in system_findings)
    low_remediated = sum(s["vulnerabilities"]["low_risk"]["reported_remediated_by_va_july_2025"] for s in system_findings)

    assert high_remediated == 27, f"Expected 27 high-risk remediated (93%), got {high_remediated}"
    assert mod_remediated == 135, f"Expected 135 mod-risk remediated, got {mod_remediated}"
    assert low_remediated == 217, f"Expected 217 low-risk remediated, got {low_remediated}"

    total_remediated = sum(s["vulnerabilities"]["reported_remediated_count"] for s in system_findings)
    assert total_remediated == 379, f"Expected 379 total remediated by VA, got {total_remediated}"
    assert high_remediated + mod_remediated + low_remediated == 379

def test_system_anonymisation_and_verification_label(system_findings):
    """Ensures systems remain anonymised and are explicitly labeled as VA-reported."""
    for s in system_findings:
        assert "anonymisation_note" in s
        assert "sensitivity of the systems" in s["anonymisation_note"]
        assert "VA-reported remediation" in s["verification_distinction"]
        assert "not independently verified as closed" in s["verification_distinction"]

# ==============================================================================
# 3. Dataset A: Program Findings Validation (11 Areas, 55 Total Actions, 20 Completed)
# ==============================================================================

def test_program_findings_metrics(program_findings):
    """
    Verifies Table 1, Table 4, and Table 6 figures:
    - 11 program finding areas.
    - 55 total remediation actions across all findings.
    - 20 actions completed as of July 2025.
    - 35 actions in progress or delayed.
    - VA concurred with 9 and non-concurred with 2.
    """
    assert len(program_findings) == 11

    total_actions = sum(p["remediation_actions_total"] for p in program_findings)
    completed_actions = sum(p["remediation_actions_completed_july_2025"] for p in program_findings)
    in_progress_actions = sum(p["remediation_actions_in_progress_july_2025"] for p in program_findings)

    assert total_actions == 55, f"Expected 55 total actions, got {total_actions}"
    assert completed_actions == 20, f"Expected 20 completed actions, got {completed_actions}"
    assert in_progress_actions == 35, f"Expected 35 in progress actions, got {in_progress_actions}"
    assert completed_actions + in_progress_actions == 55

    non_concur_areas = [p["finding_area"] for p in program_findings if p["va_concurrence"] == "Non-concur"]
    assert len(non_concur_areas) == 2
    assert "Office of Information Security Customer Service to Systems Teams" in non_concur_areas
    assert "Cybersecurity Governance" in non_concur_areas

    concur_areas = [p["finding_area"] for p in program_findings if p["va_concurrence"] == "Concur"]
    assert len(concur_areas) == 9

def test_program_documented_delays(program_findings):
    """Verifies documented delay reporting in Medical Devices, Cyber Protection, and Cyber Response."""
    delayed_findings = {p["finding_area"]: p for p in program_findings if p["delay_documented"]}
    assert "Medical Devices" in delayed_findings
    assert delayed_findings["Medical Devices"]["estimated_remediation_date"] == "May 2027"

    assert "Cyber Protection" in delayed_findings
    assert delayed_findings["Cyber Protection"]["estimated_remediation_date"] == "Fiscal year 2026"

    assert "Cyber Response and Recovery" in delayed_findings
    assert delayed_findings["Cyber Response and Recovery"]["estimated_remediation_date"] == "Fiscal year 2026"

# ==============================================================================
# 4. Dataset C: VA OIG Recommendations Validation
# ==============================================================================

def test_oig_recommendations_themes_and_sources(oig_recommendations):
    """
    Verifies Section 4 and Footnote 33 figures:
    - Exactly 2 recommendations.
    - Separate themes: POA&M tracking vs. mitigating controls.
    - Status is 'Not implemented' as of July 2025.
    - Provenance cites both FY23 and FY24 FISMA audit reports.
    """
    assert len(oig_recommendations) == 2

    themes = [o["recommendation_theme"] for o in oig_recommendations]
    assert "Plan of Action and Milestones (POA&M) Tracking and Updating" in themes
    assert "Mitigating Controls for Delayed Vulnerabilities" in themes

    for o in oig_recommendations:
        assert o["implementation_status_july_2025"] == "Not implemented"
        assert len(o["original_oig_sources"]) == 2
        sources_text = " ".join(o["original_oig_sources"])
        assert "Audit 23-01105-69" in sources_text
        assert "Audit 24-01233-90" in sources_text
        assert o["source_evidence"]["footnote"] == "Footnote 33"

# ==============================================================================
# 5. Dataset D: Separate AI & Compliance Analysis Validation
# ==============================================================================

def test_framework_analysis_separation_and_disclaimer(framework_analysis):
    """Verifies that AI analysis is strictly isolated with mandatory disclaimer."""
    disclaimer = framework_analysis["analysis_metadata"]["disclaimer"]
    assert "NOT official findings or determinations made by GAO or VA" in disclaimer
    assert len(framework_analysis["program_finding_mappings"]) == 11
    assert len(framework_analysis["system_finding_mappings"]) == 5
    assert len(framework_analysis["oig_recommendation_mappings"]) == 2
