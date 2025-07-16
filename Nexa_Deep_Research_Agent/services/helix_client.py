# filepath: services/helix_client.py
from config import HELIX_DB_URL
import httpx

class HelixClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or HELIX_DB_URL
        self.client = httpx.AsyncClient()

    async def upsert(self, collection: str, points: list, wait: bool = True):
        url = f"{self.base_url}/collections/{collection}/points"
        payload = {"points": points, "wait": wait}
        response = await self.client.put(url, json=payload)
        response.raise_for_status()
        return response.json()

    async def search(self, collection: str, vector: list, limit: int = 10):
        url = f"{self.base_url}/collections/{collection}/points/search"
        payload = {"vector": vector, "limit": limit}
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
