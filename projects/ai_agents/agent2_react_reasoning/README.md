# Agent 2 — ReAct Reasoning Agent

**Concept taught:** the ReAct pattern (Reason + Act), written by hand with regular
expressions and plain-text parsing — no `tools=` API parameter. This is what tool-use
libraries and SDKs are automating *for* you; seeing it done manually once makes every
"agent framework" you meet afterwards much less mysterious.

## What it does

The model is instructed (entirely through its system prompt — no API-level tool support)
to respond in a strict `Thought / Action / Observation` format:

```
Thought: I need to know the capital of France.
Action: knowledge_lookup[capital of france]
```

The agent parses that text with a regex, runs the matching Python function locally,
appends `Observation: Paris` to the conversation, and sends it back. This repeats until
the model instead responds with:

```
Thought: I now have everything I need.
Final Answer: Paris
```

## Files

| File | Purpose |
|---|---|
| `tools.py` | `calculator()` and `knowledge_lookup()` — plain Python functions, no schema, no API involvement |
| `agent.py` | `ReActAgent` — builds the transcript, calls the model, parses `Action:`/`Final Answer:` with regex, dispatches to `tools.py` |
| `main.py` | CLI: `python -m projects.ai_agents.agent2_react_reasoning.main "your question"` |
| `tests/` | Offline tests — the Anthropic client is mocked with canned ReAct-formatted text, so parsing logic and tool dispatch are fully covered without any API key |

## Setup

```bash
pip install -r projects/ai_agents/requirements.txt   # from the repo root
cp projects/ai_agents/.env.example .env               # add your ANTHROPIC_API_KEY
```

## Run it

```bash
python -m projects.ai_agents.agent2_react_reasoning.main "What is the capital of France, and what is 12 * 8?"
```

Example transcript (abridged):

```
Thought: I need the capital of France first.
Action: knowledge_lookup[capital of france]
Observation: Paris

Thought: Now the arithmetic.
Action: calculator[12 * 8]
Observation: 96

Thought: I have both answers.
Final Answer: The capital of France is Paris, and 12 * 8 = 96.
```

## Run the tests

```bash
python -m pytest projects/ai_agents/agent2_react_reasoning/tests/ -v
```

## Things to try next

- Break the format on purpose (delete the `Action:` line requirement from the system
  prompt) and watch the "no Action or Final Answer" recovery message in `agent.py` kick in.
- Add a third tool to `tools.py` and to `TOOL_DESCRIPTIONS` — nothing else needs to change.
- Compare `_ACTION_RE` / `_FINAL_ANSWER_RE` in `agent.py` with how `agent1_web_search`
  gets the same information as structured JSON from `response.stop_reason` and
  `block.type == "tool_use"` instead of parsing text — that's the difference between a
  model with native tool-use support and one without.
