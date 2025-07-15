import requests

def search(query: str, num_results: int = 5) -> list:
    # Using OpenRouter for multimodel LLM routing (integration simulated)
    payload = {
        "query": query,
        "num_results": num_results,
        "include_domains": [],
        "exclude_domains": ["reddit.com", "twitter.com", "forum_sites"],
        "start_crawl_date": "2020-01-01",
        "end_crawl_date": "current_date",
        "use_autoprompt": True,
        "type": "neural",
        "contents": {
            "text": {"max_characters": 2000}
        }
    }
    # Instead of sending an HTTP request, return dummy search results
    return [{"title": f"Result {i+1} for query '{query}'", "url": f"http://example.com/{i+1}"} for i in range(num_results)]

if __name__ == "__main__":
    results = search("AI healthcare", 5)
    print(results)
