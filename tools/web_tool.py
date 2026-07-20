from ddgs import DDGS
import requests
import markdownify

def duckduckgo_search(query: str) -> list:
    """Search DuckDuckGo and return the top results."""

    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=3))
    except Exception as e:
        return [{"error": str(e)}]


def web_search(query: str) -> str:
    """Search DuckDuckGo and return the pages in Markdown."""

    results = duckduckgo_search(query)

    if not results:
        return "No search results."

    if "error" in results[0]:
        return f"Search failed: {results[0]['error']}"

    output = [f"# DuckDuckGo Search: {query}\n"]

    for i, item in enumerate(results, 1):
        title = item.get("title", "")
        url = item.get("href", "")
        snippet = item.get("body", "")

        output.append(f"## {i}. {title}")
        output.append(f"**URL:** {url}")
        output.append(snippet)
        output.append("")

        try:
            html = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            ).text

            md = markdownify.markdownify(html, heading_style="ATX")
            output.append(md)

        except Exception as e:
            output.append(f"Failed to fetch page: {e}")

        output.append("\n---\n")

    return "\n".join(output)


if __name__ == "__main__":
    result = web_search("Wealt of Elon Musk?")
    with open("result.md","w") as f:
        f.write(result)
    print(result)