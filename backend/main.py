from fastapi import FastAPI
from tasks import run_workflow
import redis

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, db=0)


@app.post("/start_workflow/")
def start_workflow(source: str, destination: str, email: str = None):
    """
    Start a workflow:
    - `source`: "gdrive" or "local"
    - `destination`: "gdrive" or "local"
    - `email`: Optional, for notifications
    """
    # Enqueue the task using Celery
    task = run_workflow.delay(source, destination, email)
    return {"message": "Workflow started!", "task_id": task.id}
