import asyncio
from services.exa_client import search

async def research_section(section: dict) -> dict:
    # Simulate converting the outline to a search query and fetching results (Stage 3: Research Loop)
    query = section.get("outline", "")
    await asyncio.sleep(1)  # Simulate network delay
    results = search(query, num_results=5)
    section["research"] = results
    return section

async def iterative_research(research_plan: dict, pass_type: str = "full") -> dict:
    paragraphs = research_plan.get("paragraphs", [])
    if pass_type == "direct":
        # Direct Cache Pass: bypass research if report is cached already
        return research_plan
    elif pass_type == "half":
        # Half Pass: process only sections missing research data
        tasks = []
        for section in paragraphs:
            if not section.get("research"):
                tasks.append(research_section(section))
            else:
                tasks.append(asyncio.sleep(0, result=section))
        updated_paragraphs = await asyncio.gather(*tasks)
    else:  # full pass
        tasks = [research_section(p) for p in paragraphs]
        updated_paragraphs = await asyncio.gather(*tasks)
    research_plan["paragraphs"] = updated_paragraphs
    return research_plan

if __name__ == "__main__":
    import json
    plan = {
      "topic": "AI in Healthcare",
      "paragraphs": [
          {"title": "Introduction", "outline": "Intro outline", "research": [], "latest_summary": ""},
          {"title": "Body", "outline": "Body outline", "research": [], "latest_summary": ""},
          {"title": "Conclusion", "outline": "Conclusion outline", "research": [], "latest_summary": ""}
      ]
    }
    loop = asyncio.get_event_loop()
    updated_plan = loop.run_until_complete(iterative_research(plan, pass_type="full"))
    print(json.dumps(updated_plan, indent=2))
