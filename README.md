# Multi-Agent Autonomous Workflow Engine 🤖⚡

An autonomous, multi-agent AI system built with **FastAPI**, **LangGraph**, **Groq API**, and **MongoDB**. The engine orchestrates specialized LLM agents (Researcher, Code Writer, and Reviewer) working in a stateful execution loop to automatically research, code, review, and refine code solutions for multi-step software tasks.

---

## 🌟 Key Features

* **Autonomous Multi-Agent Orchestration**: Built using **LangGraph** stateful graphs with conditional feedback routing.
* **Ultra-Fast LLM Inference**: Powered by **Groq API** (`llama-3.3-70b-versatile`).
* **Clean Code Extraction**: Uses regex parsing to automatically extract pure executable Python code from conversational LLM output.
* **Persistent Task Caching**: Integrates **MongoDB** to store execution histories, code outputs, and agent logs.
* **Production-Ready REST API**: Fully asynchronous API built with **FastAPI** including interactive Swagger UI documentation.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Engine Health Check |
| `POST` | `/run-workflow` | Triggers multi-agent graph execution |
| `GET` | `/task/{task_id}` | Fetches stored execution record from MongoDB 

---

🚀 Getting Started
Prerequisites

Python 3.10+

Groq API Key

MongoDB (Local instance or MongoDB Atlas Cloud URI)

Setup & Installation
Clone the repository:

Bash
>>git clone [https://github.com/YOUR_GITHUB_USERNAME/multi-agent-engine.git](https://github.com/YOUR_GITHUB_USERNAME/multi-agent-engine.git)
>>cd multi-agent-engine

Create and activate virtual environment:

>>python -m venv venv
# On Windows PowerShell:
>>.\venv\Scripts\Activate.ps1
Install dependencies:


>>pip install -r requirements.txt
Environment Setup:
Create a .env file in the root directory:

Code snippet
GROQ_API_KEY=your_groq_api_key_here
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=agent_engine
Run the API:

Bash
>>uvicorn app.main:app --reload
Open http://127.0.0.1:8000/docs in your browser to test endpoints via Swagger UI.
|

## 🏗️ Architecture & Workflow

```text
       ┌──────────────┐
       │   User /     │
       │ API Request  │
       └──────┬───────┘
              │
              ▼
    ┌──────────────────┐
    │ Researcher Agent │ (Analyzes task & requirements)
    └─────────┬────────┘
              │
              ▼
    ┌──────────────────┐
    │ Code Writer Agent│ ◄──────────┐
    └─────────┬────────┘            │
              │                     │ (Needs Changes)
              ▼                     │
    ┌──────────────────┐            │
    │  Reviewer Agent  ├────────────┘
    └─────────┬────────┘
              │ (APPROVED)
              ▼
    ┌──────────────────┐
    │ MongoDB Caching  │
    └──────────────────┘

---





🚀 Getting Started
Prerequisites

Python 3.10+

Groq API Key

MongoDB (Local instance or MongoDB Atlas Cloud URI)

Setup & Installation
Clone the repository:

Bash
>>git clone [https://github.com/YOUR_GITHUB_USERNAME/multi-agent-engine.git](https://github.com/YOUR_GITHUB_USERNAME/multi-agent-engine.git)
>>cd multi-agent-engine

Create and activate virtual environment:

>>python -m venv venv
# On Windows PowerShell:
>>.\venv\Scripts\Activate.ps1
Install dependencies:


>>pip install -r requirements.txt
Environment Setup:
Create a .env file in the root directory:

Code snippet
GROQ_API_KEY=your_groq_api_key_here
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=agent_engine
Run the API:

Bash
>>uvicorn app.main:app --reload
Open http://127.0.0.1:8000/docs in your browser to test endpoints via Swagger UI.
|
