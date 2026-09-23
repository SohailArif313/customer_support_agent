# state.py
# Purpose: Define the "shared memory" that flows through every node in the graph.
# Every node reads from this and returns updates to it.

# state.py
from typing import TypedDict, Optional


class AgentState(TypedDict):
    user_message: str
    intent: Optional[str]
    order_id: Optional[str]   # extracted from the message, if present
    response: Optional[str]