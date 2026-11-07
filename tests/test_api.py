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

def test_real_audit_data_seeding_and_recall():
    # 1. Ingest 18 authentic GAO oversight records
    seed_res = client.post("/api/memory/seed-real-data")
    assert seed_res.status_code == 200
    seed_data = seed_res.json()
    assert seed_data["status"] == "success"
    assert seed_data["ingested_records"] == 18
    assert "GAO-26-107980" in seed_data["primary_source"]

    # 2. Inquire on a real cloud security finding area (NIST CM-2 / CM-6)
    inquiry_payload = {
        "inquiry_id": "INQ-2026-CLOUD-DRIFT",
        "auditor_firm": "GAO",
        "framework": "NIST_SP_800_53_REV5",
        "inquiry_text": "Inconsistent application of baseline cloud security configurations and multi-cloud tenant drift under CM-2.",
        "severity": "MODERATE"
    }
    inquire_res = client.post("/api/audit/inquire", json=inquiry_payload)
    assert inquire_res.status_code == 200
    briefing = inquire_res.json()

    assert briefing["control_invariant"]["control_code"] == "CM-2"
    assert "Baseline Configuration" in briefing["control_invariant"]["control_title"]
    assert briefing["inquiry_id"] == "INQ-2026-CLOUD-DRIFT"

