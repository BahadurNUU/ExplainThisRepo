def clear_markdown(markdown: str) -> str:
    lines = markdown.strip().splitlines()
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return "\n".join(lines[1:-1])
    return markdown