# 💸 Ambient Expense Agent

An intelligent, event-driven expense processing agent built with the **Google Agent Development Kit (ADK 2.0)** and deployed to **Google Cloud Agent Runtime**.

This agent automatically extracts expense details from natural language or JSON payloads, evaluates the expense amount, and either automatically approves it or pauses execution to request a manual Human-in-the-Loop (HITL) review.

## 🚀 Features & Architecture

This project implements a robust Graph Workflow using `google.adk.workflow.Workflow`.

1. **Extraction Node (`extractor`)**: An `LlmAgent` powered by Gemini that reads the user's prompt (e.g., *"I bought a flight to Tokyo for 800 dollars"*) and extracts the `amount` and `description` into a strict Pydantic model.
2. **Routing Node (`route_expense`)**: A Python Function node that evaluates the extracted amount.
   - If `amount < $100`: Routes to the Auto-Approve branch.
   - If `amount >= $100`: Routes to the Manual Review branch.
3. **Auto-Approve Node (`auto_approve`)**: Automatically approves small expenses and returns a confirmation message to the user.
4. **Human-in-the-Loop Node (`review_agent`)**: A critical workflow node that uses `adk_request_input` to pause the agent's execution, yielding a tool call to the frontend requesting manual approval.

## 🛠️ Technologies Used
- **Google ADK 2.0**: For creating the workflow graph and LLM integrations.
- **Agents CLI (`google-agents-cli`)**: For scaffolding, local execution, and deployment.
- **Agent Runtime (Vertex AI Reasoning Engine)**: Fully managed, stateful production deployment environment on Google Cloud.
- **uv**: Ultra-fast Python package manager.

---

## 📂 Project Structure

```
expense-agent/
├── app/         
│   ├── agent.py               # Core graph workflow and logic (ADK 2.0)
│   ├── agent_runtime_app.py   # Agent Runtime application wrapper
│   └── app_utils/             # App utilities and helpers
├── deployment/                # Terraform infrastructure and deployment configuration
├── tests/                     # Unit, integration, and load tests
├── pyproject.toml             # Project dependencies
└── README.md                  # This documentation
```

---

## 💻 Running Locally

1. **Install dependencies:**
   Make sure you have `uv` installed, then run:
   ```bash
   agents-cli install
   ```

2. **Run the local Playground:**
   To test the agent locally with an interactive UI:
   ```bash
   agents-cli playground
   ```

3. **CLI Testing:**
   Test the auto-approval flow directly in your terminal:
   ```bash
   agents-cli run "I bought a coffee for 5 dollars"
   ```

---

## ☁️ Deployment

This agent is configured to be deployed to **Google Cloud Agent Runtime**. 

1. **Authenticate and set up your Google Cloud project:**
   ```bash
   gcloud auth application-default login
   gcloud config set project <YOUR_PROJECT_ID>
   ```

2. **Deploy the agent:**
   ```bash
   agents-cli deploy --region <YOUR_REGION>
   ```

The deployment will automatically build the necessary packages, provision the Vertex AI Reasoning Engine instance, and return a production endpoint URL.

---

## 🧪 Testing the Live Agent

Once deployed, you can verify its functionality against the live endpoint.

**Test Auto-Approval (<$100):**
```bash
agents-cli run --url https://<REGION>-aiplatform.googleapis.com/v1/projects/<PROJECT_ID>/locations/<REGION>/reasoningEngines/<ENGINE_ID> --mode adk '{"data": {"amount": 50.0, "submitter": "user@example.com", "category": "meals", "description": "Lunch"}}'
```

**Test Human-in-the-Loop (>=$100):**
```bash
agents-cli run --url https://<REGION>-aiplatform.googleapis.com/v1/projects/<PROJECT_ID>/locations/<REGION>/reasoningEngines/<ENGINE_ID> --mode adk '{"data": {"amount": 150.0, "submitter": "user@example.com", "category": "meals", "description": "Client dinner"}}'
```
*(The agent will pause execution and return an `adk_request_input` function call requesting human approval).*

---

> 💡 **Developed during the 5-Day AI Agents Intensive Vibe Coding Course with Google.**
