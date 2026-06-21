import vertexai
from vertexai.preview import reasoning_engines
import json

vertexai.init(project="project-3006a471-126f-4d6d-b73", location="us-central1")
engine_id = "5829019662968422400"
remote_app = reasoning_engines.ReasoningEngine(f"projects/267548798260/locations/us-central1/reasoningEngines/{engine_id}")

print("Testing auto-approve:")
try:
    response = remote_app.query(
        user_id="test_user",
        session_id="test_session_1",
        message='{"data": {"amount": 50.0, "submitter": "user@example.com", "category": "meals", "description": "Lunch", "date": "2026-06-04"}}'
    )
    print(response)
except Exception as e:
    print("Error:", e)

print("\nTesting HITL:")
try:
    response2 = remote_app.query(
        user_id="test_user",
        session_id="test_session_2",
        message='{"data": {"amount": 150.0, "submitter": "user@example.com", "category": "meals", "description": "Client dinner", "date": "2026-06-04"}}'
    )
    print(response2)
except Exception as e:
    print("Error:", e)
