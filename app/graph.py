from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.agents import researcher_agent, code_writer_agent, reviewer_agent

def router(state: AgentState):
    """Route back to coder if feedback needs changes, else end."""
    if state.get("review_feedback") == "APPROVED":
        return END
    return "code_writer"

# Initialize StateGraph
builder = StateGraph(AgentState)

# Add Agent Nodes
builder.add_node("researcher", researcher_agent)
builder.add_node("code_writer", code_writer_agent)
builder.add_node("reviewer", reviewer_agent)

# Set Graph Edges
builder.set_entry_point("researcher")
builder.add_edge("researcher", "code_writer")
builder.add_edge("code_writer", "reviewer")

# Conditional Loop Edge
builder.add_conditional_edges("reviewer", router, {
    END: END,
    "code_writer": "code_writer"
})

workflow = builder.compile()