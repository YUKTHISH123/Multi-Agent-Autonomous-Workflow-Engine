from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY
from app.state import AgentState

# Initialize LLM using Groq
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY
)

def researcher_agent(state: AgentState) -> dict:
    """Researches requirements for the given task."""
    prompt = f"Perform brief research and technical requirements for: {state['task']}"
    response = llm.invoke(prompt)
    return {
        "research_notes": response.content,
        "messages": ["Researcher completed analysis."]
    }

def code_writer_agent(state: AgentState) -> dict:
    """Generates Python code based on research notes and review feedback."""
    feedback = f"\nAddress this review feedback: {state['review_feedback']}" if state.get("review_feedback") else ""
    prompt = f"Write Python code for task: {state['task']}.\nNotes: {state['research_notes']}{feedback}"
    response = llm.invoke(prompt)
    return {
        "draft_code": response.content,
        "messages": ["Code Writer generated new draft."]
    }

def reviewer_agent(state: AgentState) -> dict:
    """Reviews code quality and provides critique or approval."""
    prompt = (
        f"Review this Python code for bugs and correctness:\n{state['draft_code']}\n"
        "If it is acceptable, respond with 'APPROVED'. Otherwise, provide improvement feedback."
    )
    response = llm.invoke(prompt)
    content = response.content
    
    if "APPROVED" in content.upper():
        return {
            "review_feedback": "APPROVED",
            "final_output": state["draft_code"],
            "messages": ["Reviewer approved the implementation."]
        }
    else:
        return {
            "review_feedback": content,
            "messages": ["Reviewer requested modifications."]
        }