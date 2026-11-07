import logging
from typing import Dict, Any, List, Optional
import httpx
from ..config import settings
from ..models.schemas import HindsightMemoryRecord

logger = logging.getLogger(__name__)

class HindsightClient:
    """Client for interacting with Vectorize Hindsight long-term agent memory."""

    def __init__(self, api_key: Optional[str] = None, bank_id: Optional[str] = None, api_url: Optional[str] = None):
        self.api_key = api_key if api_key is not None else settings.HINDSIGHT_API_KEY
        self.api_url = api_url or settings.HINDSIGHT_API_URL
        self.bank_id = bank_id or settings.HINDSIGHT_BANK_ID
        # In-memory local bank for offline testing / fallback
        self._local_memory_bank: List[HindsightMemoryRecord] = []

        # Try initializing official Hindsight SDK if available
        self._sdk_client = None
        if self.api_key and self.api_key != "your_hindsight_api_key_here":
            try:
                from hindsight_client import Hindsight
                self._sdk_client = Hindsight(base_url=self.api_url, api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize official Hindsight SDK: {e}")

    async def check_cloud_connection(self) -> Dict[str, Any]:
        """
        Actively probes the configured Hindsight Cloud endpoint and checks authentication status.
        Returns live connectivity diagnostics, status code, and blocker reasons.
        """
        has_key = bool(self.api_key and self.api_key != "your_hindsight_api_key_here")
        diagnostics = {
            "api_url": self.api_url,
            "bank_id": self.bank_id,
            "api_key_configured": has_key,
            "cloud_reachable": False,
            "authenticated": False,
            "status_code": None,
            "response_body": None,
            "blocker": None
        }

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                headers = {}
                if has_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                # Probe the bank endpoint
                response = await client.post(
                    f"{self.api_url}/v1/default/banks/{self.bank_id}/memories/recall",
                    headers=headers,
                    json={"query": "health_check"}
                )
                diagnostics["cloud_reachable"] = True
                diagnostics["status_code"] = response.status_code
                try:
                    diagnostics["response_body"] = response.json()
                except Exception:
                    diagnostics["response_body"] = response.text

                if response.status_code == 200:
                    diagnostics["authenticated"] = True
                elif response.status_code == 401:
                    diagnostics["authenticated"] = False
                    diagnostics["blocker"] = (
                        "HINDSIGHT_API_KEY is not configured or lacks valid credentials. "
                        f"Server responded 401 Unauthorized: {diagnostics['response_body']}"
                    )
                else:
                    diagnostics["blocker"] = f"Unexpected response from Hindsight Cloud: HTTP {response.status_code}"
        except httpx.ConnectError as e:
            diagnostics["blocker"] = f"Network connection failed: Unable to reach {self.api_url} ({e})"
        except httpx.TimeoutException:
            diagnostics["blocker"] = f"Connection timed out while probing {self.api_url}"
        except Exception as e:
            diagnostics["blocker"] = f"Error probing Hindsight Cloud service: {str(e)}"

        return diagnostics

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
                if self._sdk_client:
                    # Sanitize metadata for official SDK (expects string-string dict)
                    str_meta = {k: str(v) for k, v in metadata.items() if not isinstance(v, (dict, list))}
                    await self._sdk_client.aretain(
                        bank_id=self.bank_id,
                        content=content,
                        metadata=str_meta
                    )
                    logger.info("Successfully retained memory to Hindsight Cloud via SDK.")
                    self._local_memory_bank.append(record)
                    return True
                else:
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        response = await client.post(
                            f"{self.api_url}/v1/default/banks/{self.bank_id}/memories",
                            headers={"Authorization": f"Bearer {self.api_key}"},
                            json={"content": content, "metadata": metadata}
                        )
                        if response.status_code in [200, 201]:
                            logger.info("Successfully retained memory to Hindsight Cloud via HTTP.")
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
                if self._sdk_client:
                    resp = await self._sdk_client.arecall(
                        bank_id=self.bank_id,
                        query=query,
                        budget="mid"
                    )
                    results = []
                    for item in getattr(resp, "results", []):
                        results.append({
                            "content": getattr(item, "text", ""),
                            "metadata": getattr(item, "metadata", {}),
                            "score": 1.0,
                            "created_at": None
                        })
                    if results:
                        return results[:top_k]
                else:
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        response = await client.post(
                            f"{self.api_url}/v1/default/banks/{self.bank_id}/memories/recall",
                            headers={"Authorization": f"Bearer {self.api_key}"},
                            json={"query": query, "context": context, "top_k": top_k}
                        )
                        if response.status_code == 200:
                            return response.json().get("results", [])
            except Exception as e:
                logger.error(f"Error querying Hindsight Cloud: {e}. Searching local bank.")

        # Local enhanced semantic & heuristic recall matching
        results = []
        # Filter out trivial stop words to improve keyword precision
        stop_words = {"the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "of", "with", "is", "was", "by"}
        raw_words = [w.strip(".,;:?!'\"()[]{}") for w in query.lower().split()]
        query_words = [w for w in raw_words if w and w not in stop_words]

        if not query_words:
            return []

        for rec in self._local_memory_bank:
            content_lower = rec.content.lower()
            meta_str = " ".join(f"{k}:{v}" for k, v in rec.metadata.items()).lower()
            combined_text = f"{content_lower} {meta_str}"

            # Calculate keyword match count
            matched_words = sum(1 for w in query_words if w in combined_text)

            # Check for phrase bonus
            phrase_bonus = 0.5 if query.lower() in combined_text else 0.0

            # Match context filters if specified
            context_match = True
            for ck, cv in context.items():
                if ck in rec.metadata:
                    if str(rec.metadata[ck]).lower() != str(cv).lower():
                        context_match = False
                        break

            if matched_words > 0 and context_match:
                # Require at least 25% query word overlap or a strong multi-word match
                overlap = matched_words / len(query_words)
                if overlap >= 0.20 or matched_words >= 2 or phrase_bonus > 0:
                    results.append({
                        "content": rec.content,
                        "metadata": rec.metadata,
                        "score": round(overlap + phrase_bonus, 3),
                        "created_at": rec.created_at.isoformat()
                    })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def get_all_local_records(self) -> List[HindsightMemoryRecord]:
        """Inspects all records stored in the active session memory."""
        return self._local_memory_bank

