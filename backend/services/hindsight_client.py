import logging
from typing import Dict, Any, List, Optional
import httpx
from ..config import settings
from ..models.schemas import HindsightMemoryRecord

logger = logging.getLogger(__name__)

class HindsightClient:
    """Client for interacting with Vectorize Hindsight long-term agent memory."""

    def __init__(self, api_key: Optional[str] = None, bank_id: Optional[str] = None):
        self.api_key = api_key or settings.HINDSIGHT_API_KEY
        self.api_url = settings.HINDSIGHT_API_URL
        self.bank_id = bank_id or settings.HINDSIGHT_BANK_ID
        # In-memory local bank for offline testing / fallback
        self._local_memory_bank: List[HindsightMemoryRecord] = []

    async def retain(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Stores an episodic memory record (past audit finding, rejected proposal, or approved compensating control).
        """
        metadata = metadata or {}
        record = HindsightMemoryRecord(
            bank_id=self.bank_id,
            content=content,
            metadata=metadata
        )

        if self.api_key and self.api_key != "your_hindsight_api_key_here":
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        f"{self.api_url}/v1/banks/{self.bank_id}/retain",
                        headers={"Authorization": f"Bearer {self.api_key}"},
                        json={"content": content, "metadata": metadata}
                    )
                    if response.status_code in [200, 201]:
                        logger.info("Successfully retained memory to Hindsight Cloud.")
                        self._local_memory_bank.append(record)
                        return True
                    logger.warning(f"Hindsight API responded with status {response.status_code}, falling back to local bank.")
            except Exception as e:
                logger.error(f"Error communicating with Hindsight Cloud: {e}. Storing locally.")

        # Local fallback execution
        self._local_memory_bank.append(record)
        return True

    async def recall(self, query: str, context: Optional[Dict[str, Any]] = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves relevant historical memories matching query parameters and contextual filters.
        """
        context = context or {}

        if self.api_key and self.api_key != "your_hindsight_api_key_here":
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        f"{self.api_url}/v1/banks/{self.bank_id}/recall",
                        headers={"Authorization": f"Bearer {self.api_key}"},
                        json={"query": query, "context": context, "top_k": top_k}
                    )
                    if response.status_code == 200:
                        return response.json().get("results", [])
            except Exception as e:
                logger.error(f"Error querying Hindsight Cloud: {e}. Searching local bank.")

        # Local heuristic recall matching for testing / offline demo
        results = []
        query_words = set(query.lower().split())
        for rec in self._local_memory_bank:
            match_score = sum(1 for w in query_words if w in rec.content.lower())
            if match_score > 0:
                results.append({
                    "content": rec.content,
                    "metadata": rec.metadata,
                    "score": round(match_score / len(query_words), 3),
                    "created_at": rec.created_at.isoformat()
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def get_all_local_records(self) -> List[HindsightMemoryRecord]:
        """Inspects all records stored in the active session memory."""
        return self._local_memory_bank
