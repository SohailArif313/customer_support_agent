# routing.py
# Purpose: A tiny function that tells the graph WHICH node to go to next,
# based on the "intent" field in the state.

from app.agents.state import AgentState


def route_by_intent(state: AgentState) -> str:
    """
    LangGraph calls this after classify_intent_node runs.
    Whatever string we return here must match a node name in graph.py.
    """
    return state["intent"]