# Multi-Source Research Agent  
### LLM-Powered Multi-Source Research Assistant with FastAPI, LangGraph, and ChromaDB

A fully modular **multi-source research agent** that collects and synthesizes insights from **Google, Bing, and Reddit** — powered by **LangGraph** orchestration, **FastAPI** backend, **Streamlit** UI, and a **ChromaDB vector store** for local embedding search.
**Based on a tutorial and foundational code provided by [Tech With Tim](https://www.youtube.com/watch?v=cUC-hyjpNxk)** (LLM-Powered Multi-Source Research Assistant with LangGraph, Python, Bright Data.)

---

## Key Features

- **LangGraph + GPT-4/3.5 Integration:** Parallel multi-source retrieval and synthesis pipeline.
- **FastAPI Backend:** Production-grade API layer with `/ask`, `/health`, and `/version` endpoints.
- **Streamlit Frontend:** Simple, interactive UI to query and visualize responses.
- **Vector Database (ChromaDB):** Local semantic retrieval with OpenAI embeddings (`text-embedding-3-small`).
- **Monitoring & Health Checks:** Built-in Prometheus instrumentation and uptime-ready `/health` route.
- **Extensible Modular Design:** Swap or extend sources, vector DBs, and LLM providers easily.

---

## Project Structure

```text
multi-source-research-agent
├── main.py               # LangGraph workflow definition
├── server.py             # FastAPI backend with monitoring endpoints
├── app.py                # Streamlit UI
├── vector_store.py       # ChromaDB vector storage logic
├── web_operations.py     # Web search functions (Google/Bing/Reddit)
├── prompts.py            # Prompt templates for different analysis steps
├── requirements.txt      # Dependencies
└── README.md             # Project overview
```

---

## Installation

```bash
git clone https://github.com/hasancanbiyik/multi-source-research-agent.git
cd multi-source-research-agent

python3 -m venv venv
source venv/bin/activate  # (or .\venv\Scripts\activate on Windows)

pip install -r requirements.txt
```

---

## Running the App

### 1️⃣ Start the FastAPI backend:
```bash
uvicorn server:app --reload
```

### 2️⃣ (Optional) Start the Streamlit UI:
```bash
streamlit run app.py
```

### 3️⃣ Example API usage:
POST to `/ask`:
```json
{
  "question": "What are recent trends in LLM fine-tuning techniques?"
}
```

Response:
```json
{
  "final_answer": "...",
  "google_analysis": "...",
  "reddit_analysis": "...",
  "latency_ms": 2543.67
}
```

---

## How It Works

Each query triggers a **LangGraph pipeline**:
1. Searches Google, Bing, and Reddit.
2. Retrieves relevant Reddit posts and comments.
3. Analyzes each source using GPT models.
4. Synthesizes a final multi-source answer.
5. (Optional) Stores text chunks in **ChromaDB** for semantic re-querying.

---

## Monitoring & Health

The API exposes:
- `GET /health` → Health check for uptime monitoring  
- `GET /version` → Model and service metadata  
- Prometheus metrics are available for performance monitoring if configured.

---

## Deployment

Easily deployable on:
- **AWS EC2 / ECS / Lambda**
- **Render / Railway / Hugging Face Spaces**
- or containerized with Docker (`Dockerfile` in progress)

---

## Future Enhancements

- [ ] Integrate FAISS / Pinecone for scalable retrieval  
- [ ] Add async parallelization for faster API calls  
- [ ] Include Hugging Face model options for analysis  
- [ ] Full Docker + CI/CD pipeline  

---

🔗  [LinkedIn](https://www.linkedin.com/in/hasancanbyk)

---

