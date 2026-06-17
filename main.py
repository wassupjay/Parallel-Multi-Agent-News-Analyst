from dotenv import load_dotenv
load_dotenv()
from src.graph import graph

TOPICS = [
    "AI and machine learning breakthroughs",
    "Climate change and renewable energy",
    "Global economic trends",
    "Space exploration news",
    "Cybersecurity threats and developments",
]

def main():
    graph.invoke({"topics": TOPICS, "briefings": []})

if __name__ == "__main__":
    main()
