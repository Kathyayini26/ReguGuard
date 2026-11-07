import asyncio
from backend.services.hindsight_client import HindsightClient

def test_hindsight_retain_and_recall_cycle():
    async def run_test():
        client = HindsightClient(bank_id="test-audit-bank")

        # Retain a past rejected proposal
        await client.retain(
            content="Auditor Schellman REJECTED manual spreadsheet for CC6.1.",
            metadata={"outcome": "REJECTED", "auditor_firm": "Schellman", "year": 2025}
        )

        # Retain an approved compensating control
        await client.retain(
            content="Auditor Schellman ACCEPTED Automated KMS Digest Pipeline for CC6.1.",
            metadata={"outcome": "ACCEPTED", "auditor_firm": "Schellman", "year": 2025}
        )

        # Query Hindsight memory
        results = await client.recall(query="Schellman CC6.1 compensating control", top_k=2)
        assert len(results) == 2
        assert any("REJECTED" in r["content"] for r in results)
        assert any("ACCEPTED" in r["content"] for r in results)

    asyncio.run(run_test())
