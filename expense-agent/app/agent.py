import os
import google.auth
from pydantic import BaseModel

from google.adk.workflow import Workflow
from google.adk.events.event import Event
from google.adk.events.request_input import RequestInput
from google.genai import types
from google.adk.agents.context import Context
from google.adk.agents import LlmAgent
from google.adk.apps import App

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

class Expense(BaseModel):
    amount: float
    description: str

extractor = LlmAgent(
    name="extractor",
    model="gemini-flash-latest",
    instruction="Extract the expense amount and description from the user's input.",
    output_schema=Expense,
    output_key="expense"
)

def route_expense(ctx: Context, node_input: dict):
    amount = node_input.get("amount", 0.0)
    if amount < 100:
        return Event(output=node_input, route="auto_approve")
    else:
        return Event(output=node_input, route="review")

def auto_approve(node_input: dict):
    msg = f"Expense of ${node_input.get('amount', 0)} ({node_input.get('description', '')}) automatically approved."
    return Event(output=msg, content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]))

async def review_agent(ctx: Context, node_input: dict):
    if not ctx.resume_inputs:
        yield RequestInput(
            interrupt_id="review_expense", 
            message=f"Review required for expense of ${node_input.get('amount', 0)} ({node_input.get('description', '')}). Approve? (yes/no)"
        )
        return
    
    decision = ctx.resume_inputs.get("review_expense", "").lower()
    if decision == "yes" or decision == "y":
        msg = "Expense approved by human."
        yield Event(output=msg, content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]))
    else:
        msg = "Expense rejected by human."
        yield Event(output=msg, content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]))

root_agent = Workflow(
    name="expense_agent",
    edges=[
        ('START', extractor),
        (extractor, route_expense),
        (route_expense, {'auto_approve': auto_approve, 'review': review_agent}),
    ]
)

app = App(
    root_agent=root_agent,
    name="app",
)
