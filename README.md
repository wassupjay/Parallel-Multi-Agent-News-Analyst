# Parallel Multi-Agent News Analyst

5 AI agents research and summarize 5 news topics simultaneously using LangGraph's Send API. Full briefing generated in under 10 seconds — no loops, no queues.

## Architecture

```
START
  │
  ▼
route_topics()  ──── Send ──►  research_agent (topic 1)  ──►┐
                ──── Send ──►  research_agent (topic 2)  ──►│
                ──── Send ──►  research_agent (topic 3)  ──►├──► consolidate ──► END
                ──── Send ──►  research_agent (topic 4)  ──►│
                ──── Send ──►  research_agent (topic 5)  ──►┘
```

Each `research_agent` runs independently in parallel:
1. Searches the web via **Tavily**
2. Summarizes results via **Groq** (llama-3.1-8b-instant)
3. Returns briefing into shared state via reducer

`consolidate` runs once after all agents finish, printing the merged report.

## Stack

| Tool | Purpose | Cost |
|------|---------|------|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Parallel agent orchestration via Send API | Free |
| [Groq](https://console.groq.com) | LLM inference (llama-3.1-8b-instant) | Free tier |
| [Tavily](https://tavily.com) | Real-time web search | Free tier |

## Setup

**1. Clone and install**
```bash
git clone <repo-url>
cd parallel-multi-agent-news-analyst
uv sync
```

**2. Set API keys**
```bash
cp .env_example .env
# Add your keys to .env
```

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Get free keys: [Groq Console](https://console.groq.com) · [Tavily](https://tavily.com)

**3. Run**
```bash
uv run main.py
```

## Output

```
# Daily News Briefing

## AI and machine learning breakthroughs

Recent advances include...

---

## Climate change and renewable energy

...
```

## Customise Topics

Edit `TOPICS` in `main.py`:

```python
TOPICS = [
    "AI and machine learning breakthroughs",
    "Climate change and renewable energy",
    "Global economic trends",
    "Space exploration news",
    "Cybersecurity threats and developments",
]
```

## Project Structure

```
├── main.py          # Entry point, defines topics
├── src/
│   ├── graph.py     # LangGraph graph definition
│   └── state.py     # NewsState + AgentState
└── pyproject.toml
```
