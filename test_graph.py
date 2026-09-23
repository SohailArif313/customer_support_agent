# test_graph.py

from app.agents.graph import build_graph


graph = build_graph()


test_messages = [
    "My order #1234 has not arrived yet. What is the issue?",
    "I want a refund for order #1234 because the product is defective.",
    "I want a refund for order #5678.",
    "I want a refund, but I don't remember my order number.",
    "This is the 3rd time I'm contacting you and nobody has replied!! Your service is terrible!",
]


for msg in test_messages:
    result = graph.invoke({
        "user_message": msg,
        "intent": None,
        "order_id": None,
        "response": None,
    })

    print(f"Message : {msg}")
    print(f"Intent  : {result['intent']}")
    print(f"Order ID: {result.get('order_id')}")
    print(f"Response: {result['response']}")
    print("-" * 50)