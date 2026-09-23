# nodes.py

import re
from typing import Literal

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from app.agents.state import AgentState
from app.config import OPENAI_API_KEY
from app.tools.db_tools import get_order, check_refund_eligibility


# ============================================================
# LLM
# ============================================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=0,
)


# ============================================================
# INTENT CLASSIFICATION
# ============================================================

class IntentClassification(BaseModel):
    intent: Literal["refund", "escalation", "support"] = Field(
        description=(
            "Customer intent. "
            "Use 'refund' for refund, return, or money-back requests. "
            "Use 'escalation' for angry/frustrated customers or "
            "customers requesting a human agent. "
            "Use 'support' for all other support requests."
        )
    )


intent_classifier = llm.with_structured_output(IntentClassification)


def classify_intent_node(state: AgentState) -> AgentState:
    """
    Classifies the customer's message into exactly one intent:

    - refund
    - escalation
    - support
    """

    user_message = state["user_message"]

    prompt = f"""
Classify the customer's message into exactly one intent.

Intent rules:

refund:
- Refund request
- Return request
- Money-back request

escalation:
- Customer is angry or frustrated
- Customer explicitly asks for a human agent
- Customer demands to speak with support staff

support:
- Order status
- Delivery questions
- Product information
- Account questions
- General support questions
- Anything that is not refund or escalation

Customer message:
{user_message}
"""

    result = intent_classifier.invoke(prompt)

    return {
        "intent": result.intent
    }


# ============================================================
# ORDER ID EXTRACTION
# ============================================================

def extract_order_id(message: str) -> str | None:
    """
    Extracts an order ID from a customer message.

    Expected format:
        #1234
        #12345
        #123456

    Returns:
        Order ID without '#', or None if not found.
    """

    match = re.search(r"#(\d{3,6})\b", message)

    if match is None:
        return None

    return match.group(1)


# ============================================================
# GENERAL SUPPORT
# ============================================================

def general_support_node(state: AgentState) -> AgentState:
    """
    Handles general customer-support questions.
    If the message contains an order ID, looks it up and includes
    real status info in the response.
    """

    order_id = extract_order_id(state["user_message"])
    order = get_order(order_id) if order_id else None

    # Build context about the order (if we found one) to give the LLM real facts
    if order_id and order:
        order_context = (
            f"Order #{order_id} found. Current status: '{order['status']}'. "
            f"Customer name on file: {order['customer_name']}."
        )
    elif order_id and not order:
        order_context = f"Order #{order_id} was NOT found in our system."
    else:
        order_context = "No order ID was mentioned in the customer's message."

    prompt = f"""
You are a professional customer support agent.

Rules:
- Be polite and concise.
- Use ONLY the order information given below — never invent order status.
- If no order info is available and the question needs it, ask the
  customer for their order ID.
- Do not mention internal code, tools, or implementation details.

Order information:
{order_context}

Customer message:
{state["user_message"]}
"""

    result = llm.invoke(prompt)

    return {
        "order_id": order_id,
        "response": result.content.strip(),
    }

# ============================================================
# REFUND
# ============================================================

def refund_node(state: AgentState) -> AgentState:
    """
    Handles refund requests.

    Flow:
        1. Extract order ID.
        2. Look up order.
        3. Check refund eligibility.
        4. Return an appropriate response.
    """

    order_id = extract_order_id(state["user_message"])

    # --------------------------------------------------------
    # No order ID
    # --------------------------------------------------------

    if order_id is None:
        return {
            "order_id": None,
            "response": (
                "I can help with your refund request. "
                "Please provide your order ID, for example #1234."
            ),
        }

    # --------------------------------------------------------
    # Order not found
    # --------------------------------------------------------

    order = get_order(order_id)

    if order is None:
        return {
            "order_id": order_id,
            "response": (
                f"I couldn't find an order with ID #{order_id}. "
                "Please double-check the order ID and try again."
            ),
        }

    # --------------------------------------------------------
    # Check refund eligibility
    # --------------------------------------------------------

    eligible = check_refund_eligibility(order_id)

    if eligible:
        return {
            "order_id": order_id,
            "response": (
                f"I checked order #{order_id}. "
                f"Its current status is '{order['status']}', "
                "and it is eligible for a refund. "
                "The refund has not been processed yet."
            ),
        }

    # --------------------------------------------------------
    # Not eligible
    # --------------------------------------------------------

    return {
        "order_id": order_id,
        "response": (
            f"I checked order #{order_id}. "
            f"Its current status is '{order['status']}', "
            "but it is not currently eligible for a refund. "
            "A human support agent will need to review your request."
        ),
    }


# ============================================================
# ESCALATION
# ============================================================

def escalation_node(state: AgentState) -> AgentState:
    """
    Handles customers who need human assistance.
    """

    return {
        "response": (
            "I'm sorry for the trouble. "
            "I'll connect you with a human support agent "
            "who can assist you further."
        ),
    }