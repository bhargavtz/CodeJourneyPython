# Step 1 — Call a Real AI Model from Python (from scratch)

This module teaches one core idea: **Python sends a request to a model; the model returns data; your Python code decides what to do next.** It is deliberately placed before the agent modules. You do not need to understand agents, embeddings, or model training to use a model API.

## What you will learn

1. Make one real chat completion call.
2. Understand the URL, API key, model name, messages, and response.
3. Continue a conversation by resending previous messages (the model is otherwise stateless).
4. Use a system message to constrain role and output.
5. Request JSON, parse it, validate it, and handle invalid output.
6. Turn a classification result into a normal Python `if` decision.

## Mental model

```text
Your Python program
  ├─ sends: model + messages + settings
  ├─ over HTTPS to a provider endpoint
  └─ receives: JSON response
       ├─ Python extracts assistant text
       ├─ optionally parses/validates JSON inside that text
       └─ Python performs the next action
```

The model does not automatically remember earlier API calls. For conversational context, your app sends the previous `user` and `assistant` messages again.

## Files

- `client.py` — small OpenAI-compatible HTTP client using Python's standard library. Read this first to see the raw request/response mechanics.
- `main.py` — basic call, conversation history, and structured support-message classification.
- `test_model_coding.py` — offline tests; the model is mocked, so tests don't consume API credits.
- `.env.example` — safe configuration template. Never commit a real `.env`.

## Setup

Run commands from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r projects/ai_agents/requirements.txt
cp projects/ai_agents/model_coding_from_scratch/.env.example .env
```

Edit `.env` and fill in the API key from your chosen OpenAI-compatible provider. The default example uses Router.bynara.id, but the base URL, key, and model are configurable. **Do not put the key in source code or commit `.env`.**

```dotenv
AI_BASE_URL=https://router.bynara.id/v1
AI_API_KEY=put_your_own_key_here
AI_MODEL=gpt-6-luna
```

If you use another provider, set its compatible base URL, API key, and exact model ID. Check that provider's docs for its supported parameters; some models don't support `temperature` or JSON mode.

## Run the lesson

```bash
python -m projects.ai_agents.model_coding_from_scratch.main
```

This makes **two real API calls**: one normal text answer, one JSON classification. API calls may cost money and are subject to the provider's limits.

## Run offline tests (no key, no network)

```bash
python -m pytest projects/ai_agents/model_coding_from_scratch/ -v
```

## Follow-along: what each part means

### 1. Configuration

```python
BASE_URL = os.getenv("AI_BASE_URL", "https://router.bynara.id/v1")
API_KEY = os.getenv("AI_API_KEY", "")
MODEL = os.getenv("AI_MODEL", "gpt-6-luna")
```

- `BASE_URL`: the provider's API address.
- `API_KEY`: secret proving your request is authorized.
- `MODEL`: which model the provider should run.

A model name is provider-specific; use a name enabled for your account.

### 2. Messages

```python
[
  {"role": "system", "content": "You are a concise support assistant."},
  {"role": "user", "content": "I was charged twice."}
]
```

- `system`: instructions for the task (optional).
- `user`: request/data from the end user.
- `assistant`: prior model answer, included when you want conversation history.

### 3. HTTP request

`client.py` serializes a Python dictionary as JSON and sends it to `/chat/completions` with an `Authorization: Bearer ...` header. This is the same underlying HTTP pattern used by many SDKs, made explicit for learning.

### 4. Response

A typical compatible response has `choices[0].message.content` and a `usage` object. The first is the generated text; `usage` reports token counts when the provider returns them. Response shapes may vary across providers.

### 5. JSON and validation

In `main.py`, the model is asked to return a small JSON object. Python then runs `json.loads` and checks expected keys and allowed category/urgency labels. **Never let unvalidated model output directly trigger a payment, email, deletion, or other high-impact action.** Use human approval for consequential actions.

## Exercises

1. Change the user question in `basic_call()` and run it again.
2. Change the system message so the summary is in Gujarati; observe whether the JSON shape stays intact.
3. Add a new allowed category such as `shipping`; update both the instruction and Python validation.
4. Add a deterministic rule: if the message contains `"charged twice"`, classify it as billing without calling the model. Compare this with the model result.
5. Break the API key on purpose in a local environment variable and read the friendly error. Never write the real key into a file you plan to commit.

## What this is not

This is not model training and does not teach how transformer weights are built. It is **model application development**: using a model someone else hosts as one component in software you control. That is the first practical step before agents, tools, memory, and Jev.

## Next step

After this works, add retries, stronger schema validation, logging, and parallel calls. Then compare a chat model classifier with Jev's Choice/Noul/Score API on the same labeled test examples.
