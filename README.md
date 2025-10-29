# Multi-Source Research Agent

An AI research assistant that takes a natural language question, searches multiple public sources (web search, Reddit discussions), analyzes findings with an LLM, and returns a synthesized answer with reasoning.

This project demonstrates a small but realistic agent workflow using LangGraph, retrieval, structured LLM output, and multi-step analysis.

---

## How it Works

### 1. User question
The user asks a question in a simple CLI loop (`python main.py`).

### 2. Retrieval
The agent:
- Queries DuckDuckGo for general web results.
- Searches Reddit for relevant discussions (no Reddit API key required).
- Fetches full Reddit comment threads for the most relevant posts.

All retrieval happens in `web_operations.py` using public endpoints (DuckDuckGo and Reddit `.json`), so there is no Bright Data dependency.

### 3. Ranking and selection
The agent asks an LLM to decide which Reddit threads are actually worth reading.  
The model is required to return a structured list of URLs.  
That structure is enforced using a Pydantic model (`RedditURLAnalysis`), which guarantees predictable output for downstream steps.

### 4. Analysis
Each data source (web results, Reddit posts, Reddit comments) is analyzed by a dedicated node.  
Prompts for those nodes live in `prompts.py`.  
This lets us generate:
- factual summaries from web sources,
- community sentiment from Reddit,
- caveats / disagreements.

### 5. Synthesis
A final node combines all analyses into a single response and returns it back to the user as the final answer.

---

## Tech Stack

- **LangGraph**  
  Used to define the agent workflow as a graph of nodes. Each node is a step (search, analyze, synthesize), and edges define execution order.

- **OpenAI (GPT-4o or compatible)**  
  Used for reasoning, summarization, and source selection. The model is called through LangChain (`init_chat_model(...)`) and can be required to return structured JSON.

- **Pydantic**  
  Enforces schema on LLM output. For example, the `RedditURLAnalysis` model defines that the LLM must return `selected_urls: List[str]`. This makes chaining steps reliable.

- **DuckDuckGo Search**  
  Replaces paid SERP scrapers. Returns organic web results and snippets for analysis.

- **Reddit public JSON**  
  Used both for discovery (finding relevant Reddit posts) and deep dive (pulling comments from those posts), without needing credentials.

---

## Project Structure

```text
.
├── main.py                # Orchestrates the graph, runs the CLI chatbot loop
├── web_operations.py      # Web and Reddit retrieval logic (DuckDuckGo + Reddit JSON)
├── prompts.py             # Prompt templates for analysis and synthesis
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
└── README.md
```

---

## Setup and Run

1. Clone the repo:
```bash
git clone https://github.com/<your-username>/multi-source-research-agent.git
cd multi-source-research-agent
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows PowerShell
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key:
```text
OPENAI_API_KEY=sk-your-key-here
```

5. Run the agent:
```bash
python main.py
```

Then type a question, e.g.:
```text
what are people saying about getting an h1b after graduation
```

The agent will:
- search the web,
- pull Reddit discussions,
- analyze both,
- and respond with a final summarized answer in the terminal.

---

## Why this project matters

- Shows agent-style orchestration, not just “call GPT once.”
- Demonstrates retrieval + reasoning + synthesis across multiple sources.
- Uses structured LLM output with Pydantic to make downstream automation possible.
- Avoids paid scrapers; uses only reproducible public data sources.
- Clean separation between retrieval layer, analysis layer, and orchestration layer.

This is the type of architecture companies use for internal research assistants, competitive intelligence tools, and AI analyst copilots.
