import datetime
import re
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from app.graph import workflow
from app.config import MONGO_URI, MONGO_DB_NAME

app = FastAPI(
    title="Multi-Agent Autonomous Workflow Engine",
    description="Production-grade AI Workflow Engine powered by LangGraph, Groq, and MongoDB",
    version="1.0.0"
)

# Initialize MongoDB Client with connection timeouts
try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = mongo_client[MONGO_DB_NAME]
    tasks_collection = db["agent_tasks"]
except Exception as e:
    print(f"Failed to initialize MongoDB client: {e}")


def extract_clean_code(text: str) -> str:
    """
    Extracts raw executable code from Markdown blocks (```python ... ```).
    If no code block tags are found, returns the cleaned string.
    """
    if not text:
        return ""
    
    # Pattern to extract content inside ```python ... ``` or ``` ... ```
    pattern = r"```(?:python)?\s*(.*?)\s*```"
    matches = re.findall(pattern, text, re.DOTALL)
    
    if matches:
        # Join multiple code blocks if the agent generated more than one
        return "\n\n".join(match.strip() for match in matches)
    
    # Fallback: return raw text if no Markdown code fences are present
    return text.strip()


class TaskRequest(BaseModel):
    task_id: str
    task_description: str


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "status": "Online",
        "engine": "Multi-Agent Autonomous Workflow Engine",
        "database": "MongoDB"
    }


@app.post("/run-workflow")
async def run_workflow(request: TaskRequest):
    """
    Executes the multi-agent graph (Researcher -> Coder -> Reviewer),
    strips markdown formatting to return clean code, and saves state to MongoDB.
    """
    try:
        initial_state = {
            "task": request.task_description,
            "research_notes": "",
            "draft_code": "",
            "review_feedback": "",
            "final_output": "",
            "messages": []
        }

        # 1. Execute the LangGraph Multi-Agent Workflow
        final_state = workflow.invoke(initial_state)

        # 2. Extract clean, executable code from LLM raw response
        raw_output = final_state.get("final_output", "")
        cleaned_code = extract_clean_code(raw_output)

        # 3. Construct Document Payload for MongoDB
        task_document = {
            "task_id": request.task_id,
            "task_description": request.task_description,
            "generated_code": cleaned_code,
            "raw_output": raw_output,
            "logs": final_state.get("messages", []),
            "status": "COMPLETED",
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

        # 4. Upsert Document into MongoDB
        try:
            tasks_collection.update_one(
                {"task_id": request.task_id},
                {"$set": task_document},
                upsert=True
            )
        except (ConnectionFailure, ServerSelectionTimeoutError) as db_err:
            print(f"Warning: Failed to save task to MongoDB: {db_err}")

        # 5. Return Clean JSON Response
        return {
            "status": "Success",
            "task_id": request.task_id,
            "result": cleaned_code,
            "logs": final_state.get("messages", [])
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Workflow execution failed: {str(e)}"
        )


@app.get("/task/{task_id}")
def get_task_result(task_id: str) -> Dict[str, Any]:
    """
    Retrieves a cached task execution record from MongoDB.
    """
    try:
        # Exclude internal MongoDB '_id' field from response
        task = tasks_collection.find_one({"task_id": task_id}, {"_id": 0})
        if not task:
            raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found in MongoDB.")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")