Multi-Agent Autonomous Workflow Engine

An autonomous, multi-agent AI system built with FastAPI, LangGraph, Groq API, and MongoDB. The engine orchestrates specialized LLM agents (Researcher, Code Writer, and Reviewer) working in a stateful execution loop to automatically research, code, review, and refine code solutions for multi-step software tasks.

---

Key Features

Autonomous Multi-Agent Orchestration**: Built using **LangGraph** stateful graphs with conditional feedback routing.
Ultra-Fast LLM Inference**: Powered by Groq API (llama-3.3-70b-versatile).
Clean Code Extraction**: Uses regex parsing to automatically extract pure executable Python code from conversational LLM output.
Persistent Task Caching**: Integrates MongoDB to store execution histories, code outputs, and agent logs.
Production-Ready REST API**: Fully asynchronous API built with **FastAPI** including interactive Swagger UI documentation.

---

Architecture & Workflow


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
