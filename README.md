# Customer Support Agent

An AI-powered customer support agent built with FastAPI and LangGraph.

The agent can understand a customer's request, classify the intent, route it to the appropriate workflow, check order information, handle refund requests, and escalate conversations to human support when needed.

## Features

- Intent classification
- Intent-based routing with LangGraph
- Refund eligibility checking
- Order lookup using demo data
- Human support escalation
- General customer support responses
- FastAPI backend
- Web-based chat interface
- HTML/CSS/JavaScript frontend
- Health check endpoint
- CORS support

## Tech Stack

- Python
- FastAPI
- LangGraph
- LangChain
- OpenAI
- Pydantic
- HTML
- CSS
- JavaScript

.
├── app/
│   ├── agents/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   ├── routing.py
│   │   └── state.py
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   ├── templates/
│   │   └── index.html
│   ├── tools/
│   │   └── db_tools.py
│   ├── config.py
│   └── main.py
├── src/
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
├── test_graph.py
└── uv.lock

## How It Works

Customer
   ↓
Web Chat Interface
   ↓
FastAPI
   ↓
LangGraph
   ↓
Intent Classification
   ├── Refund
   ├── Escalation
   └── Support
   ↓
Response
   ↓
Customer

## Example Requests

### Refund

I want a refund for order #1234.

The agent identifies the request as a refund and checks the order's refund eligibility.

### Escalation

I'm really frustrated. I want to speak to a human.

The agent identifies the request as an escalation and provides a human-support handoff response.

### General Support

I need help with my order.

The agent routes the request to the general support workflow.

## Running Locally

### 1. Clone the repository

git clone https://github.com/SohailArif313/customer_support_agent.git

cd customer-support-agent

### 2. Create a virtual environment

Using uv:

uv venv

Activate it on Windows:

.venv\Scripts\activate

### 3. Install dependencies


Create a virtual environment and install dependencies:
``
uv venv

uv sync
``

### 4. Add environment variables

Create a .env file and add:

OPENAI_API_KEY=your_api_key_here

Never commit your .env file or API keys to GitHub.

### 5. Run the application

uvicorn main:app --reload

Open the application:

http://127.0.0.1:8000/

Health check:

http://127.0.0.1:8000/health

## API

### GET /

Serves the customer support chat interface.

### GET /health

Returns the API health status.

Example response:

{
  "status": "ok",
  "service": "customer-support-agent"
}

### POST /chat

Accepts a customer message and returns the agent response.

Request:

{
  "message": "I want a refund for order #1234"
}

Response:

{
  "response": "Your order is eligible for a refund...",
  "intent": "refund",
  "order_id": "1234"
}

## Current Status

This is an early working version of the project.

The current version uses demo order data and focuses on the core agent workflow, intent routing, API, and chat interface.

## Planned Improvements

- Conversation memory
- Better follow-up questions
- Real database integration
- Real customer and order actions
- Human support handoff
- Authentication
- Better error handling
- Deployment
- Monitoring and logging

## Disclaimer

This project is built for learning and demonstration purposes.

The current order data is fake/demo data and no real customer information is used.


## 👤 Author

**Sohail**
* GitHub: [@SohailArif313](https://github.com/SohailArif313)


boht zyada emjies na use kerna