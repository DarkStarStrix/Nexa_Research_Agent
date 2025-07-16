import os
import httpx

EXA_API_KEY = os.getenv("EXA_API_KEY")
EXA_SEARCH_URL = os.getenv("EXA_SEARCH_URL", "https://api.exa.ai/search")

async def search(query: str, num_results: int = 5) -> list:
    """
    Perform a neural search via Exa.ai.
    """
    headers = {"Authorization": f"Bearer {EXA_API_KEY}"}
    payload = {
        "query": query,
        "num_results": num_results,
        "exclude_domains": ["reddit.com", "twitter.com", "forum_sites"],
        "start_crawl_date": "2020-01-01",
        "end_crawl_date": "current_date",
        "use_autoprompt": True,
        "type": "neural",
        "contents": {"text": {"max_characters": 2000}}
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(EXA_SEARCH_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        # Expecting `data["results"]` to be a list of {title, url, snippet}
        return data.get("results", [])

