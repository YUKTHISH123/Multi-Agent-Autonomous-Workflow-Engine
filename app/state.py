from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    task: str
    research_notes: str
    draft_code: str
    review_feedback: str
    final_output: str
    messages: Annotated[List[str], operator.add]