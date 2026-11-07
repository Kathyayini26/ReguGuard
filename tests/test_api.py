import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "ReguGuard"
    assert data["status"] == "online"

def test_seed_and_inquiry_flow():
    # 1. Seed historical memory (Session 1)
    seed_res = client.post("/api/memory/seed")
    assert seed_res.status_code == 200

    # 2. Inquire on similar control in Session 2
    inquiry_payload = {
      "inquiry_id": "INQ-2026-TEST",
      "auditor_firm": "Schellman",
      "framework": "SOC2_TYPE_II",
      "inquiry_text": "Excessive administrative credentials found on GPU nodes under CC6.1.",
      "severity": "HIGH"
    }
    inquire_res = client.post("/api/audit/inquire", json=inquiry_payload)
    assert inquire_res.status_code == 200
    briefing = inquire_res.json()

    assert briefing["control_invariant"]["control_code"] == "CC6.1"
    assert briefing["evidence_tier"] == "Confirmed"
    assert briefing["anti_pattern_warning"] is not None
    assert "manual spreadsheet" in briefing["anti_pattern_warning"]["rejected_proposal"].lower()
    assert briefing["approved_precedent"] is not None
