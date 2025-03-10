import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def set_workflow_state(workflow_id, state):
    r.set(f"workflow:{workflow_id}", state)


def get_workflow_state(workflow_id):
    return r.get(f"workflow:{workflow_id}")


def delete_workflow_state(workflow_id):
    r.delete(f"workflow:{workflow_id}")
