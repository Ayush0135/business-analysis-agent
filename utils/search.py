from ddgs import DDGS

def search_web(query, max_results=5):
    """
    Searches the web using DuckDuckGo (Free).
    Returns a list of dictionaries with 'title', 'href', 'body'.
    """
    try:
        results = DDGS().text(query, max_results=max_results)
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []

def get_search_summary(query):
    """
    Returns a string summary of search results.
    """
    results = search_web(query)
    summary = ""
    for r in results:
        summary += f"Title: {r['title']}\nLink: {r['href']}\nSnippet: {r['body']}\n\n"
    return summary
