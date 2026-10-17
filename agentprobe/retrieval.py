from typing import Any


class QdrantTraceSearch:
    """Optional Qdrant adapter. Supply embeddings from your chosen embedding model."""

    def __init__(self, url: str, collection: str, api_key: str | None = None):
        from qdrant_client import QdrantClient
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection = collection

    def search(self, vector: list[float], limit: int = 5) -> list[dict[str, Any]]:
        hits = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=limit,
            with_payload=True,
        ).points
        return [{"id": str(hit.id), "score": hit.score, "payload": hit.payload} for hit in hits]
