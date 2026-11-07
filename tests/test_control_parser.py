import pytest
from backend.services.control_parser import ControlParser

def test_explicit_control_code_extraction():
    inquiry = "Auditor identified direct root credentials on staging cluster under CC6.1."
    invariant = ControlParser.extract_control_invariant(inquiry)
    assert invariant.control_code == "CC6.1"
    assert "Logical Access" in invariant.control_title

def test_heuristic_keyword_extraction():
    inquiry = "Terminated contractor accounts were still active 48 hours after offboarding."
    invariant = ControlParser.extract_control_invariant(inquiry)
    assert invariant.control_code == "CC6.2"
    assert "User Registration" in invariant.control_title

def test_code_review_dependency_extraction():
    inquiry = "Unreviewed pull request merged directly to main without vulnerability scan."
    invariant = ControlParser.extract_control_invariant(inquiry)
    assert invariant.control_code == "CC6.8"
