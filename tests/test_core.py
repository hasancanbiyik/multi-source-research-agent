"""
Core tests for the Multi-Source Research Agent.
These tests validate graph structure, data models, and formatting logic
WITHOUT requiring API keys or external service calls.
"""

from unittest.mock import patch

# ---------------------------------------------------------------------------
# 1. Pydantic model tests
# ---------------------------------------------------------------------------

def test_reddit_url_analysis_model():
    """RedditURLAnalysis should accept a list of URL strings."""
    from main import RedditURLAnalysis

    valid = RedditURLAnalysis(selected_urls=["https://reddit.com/r/test/1", "https://reddit.com/r/test/2"])
    assert len(valid.selected_urls) == 2
    assert all(isinstance(u, str) for u in valid.selected_urls)


def test_reddit_url_analysis_empty():
    """RedditURLAnalysis should accept an empty list."""
    from main import RedditURLAnalysis

    empty = RedditURLAnalysis(selected_urls=[])
    assert empty.selected_urls == []


# ---------------------------------------------------------------------------
# 2. State schema tests
# ---------------------------------------------------------------------------

def test_state_schema_has_required_keys():
    """State TypedDict should contain all expected keys."""
    from main import State

    expected_keys = {
        "messages",
        "user_question",
        "google_results",
        "bing_results",
        "reddit_results",
        "selected_reddit_urls",
        "reddit_post_data",
        "google_analysis",
        "bing_analysis",
        "reddit_analysis",
        "final_answer",
    }
    assert expected_keys == set(State.__annotations__.keys())


# ---------------------------------------------------------------------------
# 3. Graph structure tests
# ---------------------------------------------------------------------------

def test_graph_compiles():
    """The LangGraph workflow should compile without errors."""
    from main import graph

    assert graph is not None


def test_graph_has_expected_nodes():
    """The compiled graph should contain all pipeline nodes."""
    from main import graph

    node_names = set(graph.nodes.keys())
    expected_nodes = {
        "google_search",
        "bing_search",
        "reddit_search",
        "analyze_reddit_posts",
        "retrieve_reddit_posts",
        "analyze_google_results",
        "analyze_bing_results",
        "analyze_reddit_results",
        "synthesize_analyses",
    }
    # Graph may also include __start__ and __end__ nodes
    assert expected_nodes.issubset(node_names), (
        f"Missing nodes: {expected_nodes - node_names}"
    )


# ---------------------------------------------------------------------------
# 4. Search formatting tests
# ---------------------------------------------------------------------------

def test_google_search_formats_results():
    """google_search node should format results into markdown links."""
    from main import google_search

    mock_results = [
        {"title": "Test Result", "url": "https://example.com", "snippet": "A snippet"},
        {"title": "Another", "url": "https://example.org", "snippet": "More text"},
    ]

    with patch("main.serp_search", return_value=mock_results):
        state = {"user_question": "test query"}
        result = google_search(state)

    assert "google_results" in result
    assert "Test Result" in result["google_results"]
    assert "https://example.com" in result["google_results"]
    assert "Another" in result["google_results"]


def test_bing_search_formats_results():
    """bing_search node should format results into markdown links."""
    from main import bing_search

    mock_results = [
        {"title": "Bing Result", "url": "https://bing.example.com", "snippet": "Bing snippet"},
    ]

    with patch("main.serp_search", return_value=mock_results):
        state = {"user_question": "test query"}
        result = bing_search(state)

    assert "bing_results" in result
    assert "Bing Result" in result["bing_results"]


def test_google_search_handles_empty_results():
    """google_search should handle empty search results gracefully."""
    from main import google_search

    with patch("main.serp_search", return_value=[]):
        state = {"user_question": "obscure query"}
        result = google_search(state)

    assert "google_results" in result
    assert result["google_results"] == ""


# ---------------------------------------------------------------------------
# 5. Analysis node tests (with mocked LLM)
# ---------------------------------------------------------------------------

def test_analyze_google_no_results():
    """analyze_google_results should return fallback when no results."""
    from main import analyze_google_results

    state = {"user_question": "test", "google_results": ""}
    result = analyze_google_results(state)

    assert "google_analysis" in result
    assert "No Google results" in result["google_analysis"]


def test_analyze_bing_no_results():
    """analyze_bing_results should return fallback when no results."""
    from main import analyze_bing_results

    state = {"user_question": "test", "bing_results": ""}
    result = analyze_bing_results(state)

    assert "bing_analysis" in result
    assert "No Bing results" in result["bing_analysis"]


def test_analyze_reddit_posts_no_results():
    """analyze_reddit_posts should return empty URLs when no reddit data."""
    from main import analyze_reddit_posts

    state = {"user_question": "test", "reddit_results": ""}
    result = analyze_reddit_posts(state)

    assert result["selected_reddit_urls"] == []


def test_retrieve_reddit_posts_no_urls():
    """retrieve_reddit_posts should return empty list when no URLs selected."""
    from main import retrieve_reddit_posts

    state = {"selected_reddit_urls": []}
    result = retrieve_reddit_posts(state)

    assert result["reddit_post_data"] == []


# ---------------------------------------------------------------------------
# 6. Integration: run_agent_question signature
# ---------------------------------------------------------------------------

def test_run_agent_question_signature():
    """run_agent_question should be callable with a string argument."""
    from main import run_agent_question

    assert callable(run_agent_question)
