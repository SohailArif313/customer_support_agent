# graph.py
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import (
    classify_intent_node,
    general_support_node,
    refund_node,
    escalation_node,
)
from app.agents.routing import route_by_intent


def build_graph():
    workflow = StateGraph(AgentState)

    # Register all nodes
    workflow.add_node("classify", classify_intent_node)
    workflow.add_node("support", general_support_node)
    workflow.add_node("refund", refund_node)
    workflow.add_node("escalation", escalation_node)

    # Start at classify
    workflow.set_entry_point("classify")

    # Conditional branching: after "classify", check route_by_intent(),
    # and go to whichever node name it returns.
    workflow.add_conditional_edges(
        "classify",
        route_by_intent,
        {
            "support": "support",
            "refund": "refund",
            "escalation": "escalation",
        },
    )

    # All three handler nodes end the graph after running
    workflow.add_edge("support", END)
    workflow.add_edge("refund", END)
    workflow.add_edge("escalation", END)

    return workflow.compile()