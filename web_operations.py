# web_operations.py
import requests
from urllib.parse import urljoin
from duckduckgo_search import DDGS

USER_AGENT = "Mozilla/5.0 (GenAI-Research-Agent by Hasan)"

def serp_search(query: str, engine: str = "duckduckgo"):
    """
    Replacement for Google/Bing scraping via Bright Data.
    Returns a list of results: [{"title": ..., "snippet": ..., "url": ...}, ...]
    """
    results_clean = []
    # DDGS().text returns dicts with 'title', 'href', 'body'
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=10):
            results_clean.append({
                "title": r.get("title"),
                "url": r.get("href"),
                "snippet": r.get("body"),
                "source_engine": engine
            })
    return results_clean

def reddit_search_api(keyword: str, limit: int = 8):
    """
    Simple, no-auth Reddit search using old.reddit.com JSON.
    Returns a dict similar to before: {"parsed_posts": [...], "total_found": N}
    """
    url = "https://old.reddit.com/search.json"
    params = {"q": keyword, "sort": "relevance", "t": "year", "limit": limit}
    headers = {"User-Agent": USER_AGENT}

    r = requests.get(url, params=params, headers=headers, timeout=20)
    r.raise_for_status()
    data = r.json()

    parsed = []
    for child in data.get("data", {}).get("children", []):
        d = child.get("data", {})
        parsed.append({
            "title": d.get("title"),
            "url": urljoin("https://www.reddit.com", d.get("permalink", "")),
            "score": d.get("score"),
            "subreddit": d.get("subreddit"),
            "num_comments": d.get("num_comments"),
        })

    return {"parsed_posts": parsed, "total_found": len(parsed)}

def reddit_post_retrieval(urls: list[str], max_comments: int = 20):
    """
    For each Reddit post URL, fetch top-level comments using the public .json endpoint.
    Returns {"comments": [...], "total_retrieved": N}
    """
    headers = {"User-Agent": USER_AGENT}
    all_comments = []

    for url in urls:
        api_url = url.rstrip("/") + ".json"
        try:
            resp = requests.get(api_url, headers=headers, timeout=20)
            resp.raise_for_status()
            j = resp.json()

            # comments are typically in j[1]["data"]["children"]
            if len(j) > 1:
                for c in j[1]["data"]["children"]:
                    if c.get("kind") != "t1":  # t1 = comment
                        continue
                    body = c.get("data", {}).get("body")
                    if body:
                        all_comments.append({
                            "comment_id": c["data"].get("id"),
                            "content": body
                        })
                        if len(all_comments) >= max_comments:
                            break
        except Exception as e:
            print(f"Reddit fetch failed for {url}: {e}")

    return {
        "comments": all_comments,
        "total_retrieved": len(all_comments),
    }