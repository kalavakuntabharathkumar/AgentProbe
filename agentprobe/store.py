from typing import Any
from pymongo import MongoClient
from pymongo.collection import Collection


class TraceStore:
    """Small store with an in-memory fallback for local demos."""

    def __init__(self, mongo_uri: str | None = None, database: str = "agentprobe"):
        self._memory: list[dict[str, Any]] = []
        self._client: MongoClient | None = None
        self._collection: Collection | None = None
        if mongo_uri:
            self._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=1500)
            self._collection = self._client[database]["evaluations"]

    def add(self, record: dict[str, Any]) -> None:
        if self._collection is not None:
            self._collection.insert_one(record.copy())
        else:
            self._memory.append(record.copy())

    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        if self._collection is not None:
            docs = list(self._collection.find({}, {"_id": 0}).sort("created_at", -1).limit(limit))
            return docs
        return list(reversed(self._memory[-limit:]))

    def close(self) -> None:
        if self._client:
            self._client.close()
