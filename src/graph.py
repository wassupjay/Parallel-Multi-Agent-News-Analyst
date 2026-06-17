import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy, Send
from tavily import TavilyClient
from src.state import AgentState, NewsState
load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def route_topics(state: NewsState):
    return [Send("research_agent", {"topic": topic}) for topic in state["topics"]]

def research_agent(state: AgentState) -> dict:
    topic = state["topic"]
    results = tavily.search(query=topic, max_results=2)
    context = "\n\n".join(
        f"Title: {r['title']}\n{r['content'][:300]}" for r in results["results"]
    )

    response = llm.invoke([
        HumanMessage(content=(
            f"You are a news analyst. Write a concise briefing (3-4 sentences) on: {topic}\n\n"
            f"Search Results:\n{context}"
        ))
    ])
    return {"briefings": [f"## {topic}\n\n{response.content}"]}

def consolidate(state: NewsState) -> dict:
    report = "# Daily News Briefing\n\n" + "\n\n---\n\n".join(state["briefings"])
    print(report)
    return {}

builder = StateGraph(NewsState)
retry = RetryPolicy(max_attempts=5, initial_interval=1.0, backoff_factor=2.0)

builder.add_node("research_agent", research_agent, retry=retry)
builder.add_node("consolidate", consolidate)
builder.add_conditional_edges(START, route_topics, ["research_agent"])
builder.add_edge("research_agent", "consolidate")
builder.add_edge("consolidate", END)

graph = builder.compile()
