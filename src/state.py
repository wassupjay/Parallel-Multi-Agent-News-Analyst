import operator
from typing import Annotated, TypedDict

class NewsState(TypedDict):
    topics: list[str]
    briefings: Annotated[list[str], operator.add]

class AgentState(TypedDict):
    topic: str
