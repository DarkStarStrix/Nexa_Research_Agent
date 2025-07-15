def synthesize_section(section: dict) -> str:
    # Simulated synthesis of research results (Stage 4: Synthesis)
    research_chunks = section.get("research", [])
    summary = f"Synthesized content for '{section.get('title', '')}': " + " | ".join([r["title"] for r in research_chunks])
    return summary

def compile_report(research_plan: dict) -> str:
    sections = research_plan.get("paragraphs", [])
    compiled_sections = []
    for sec in sections:
        summary = synthesize_section(sec)
        sec["latest_summary"] = summary
        compiled_sections.append(f"### {sec.get('title', '')}\n{summary}")
    report = "\n\n".join(compiled_sections)
    return report

if __name__ == "__main__":
    plan = {
      "topic": "AI in Healthcare",
      "paragraphs": [
          {"title": "Introduction", "outline": "Intro outline", "research": [{"title": "Result 1", "url": "http://example.com/1"}], "latest_summary": ""},
          {"title": "Body", "outline": "Body outline", "research": [{"title": "Result 2", "url": "http://example.com/2"}], "latest_summary": ""},
          {"title": "Conclusion", "outline": "Conclusion outline", "research": [{"title": "Result 3", "url": "http://example.com/3"}], "latest_summary": ""}
      ]
    }
    report = compile_report(plan)
    print(report)
