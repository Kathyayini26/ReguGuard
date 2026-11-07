import pytest
from backend.services.control_parser import ControlParser

def test_explicit_control_code_extraction():
    inquiry = "Auditor identified direct root credentials on staging cluster under CC6.1."
    invariant = ControlParser.extract_control_invariant(inquiry)
    assert invariant.control_code == "CC6.1"
    assert "Logical Access" in invariant.control_title

def test_explicit_nist_control_code_extraction():
    inquiry = "GAO reported continuous vulnerability scanning gaps under CA-7."
    invariant = ControlParser.extract_control_invariant(inquiry)
    assert invariant.control_code == "CA-7"
    assert "Continuous Monitoring" in invariant.control_title
    assert "CC7.1" in invariant.soc2_crosswalk

def test_heuristic_keyword_extraction():
    inquiry = "Terminated contractor accounts were still active 48 hours after offboarding."
    invariant = ControlParser.extract_control_invariant(inquiry)
    # Extracts primary NIST AC-2 (Account Management) with CC6.2 SOC 2 crosswalk
    assert invariant.control_code == "AC-2"
    assert "Account Management" in invariant.control_title
    assert "CC6.2" in invariant.soc2_crosswalk

def test_code_review_dependency_extraction():
    inquiry = "Unreviewed pull request merged directly to main without vulnerability scan under CC6.8."
    invariant = ControlParser.extract_control_invariant(inquiry)
    assert invariant.control_code == "CC6.8"

