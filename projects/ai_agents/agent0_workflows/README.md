# Agent 0 — Workflows (Prompt Chaining & Routing)

**Concept taught:** the two patterns you should reach for *before* building a full agent.
Read this one first, even though the folder numbering makes it look like an afterthought —
it's the missing "easier option" that every other folder in this module skips past.

## Why this folder exists

Agents 1-5 are all, in one way or another, a **loop**: the model gets another turn,
decides what to do next, and the number of steps isn't known in advance. That's powerful,
but it's also slower, harder to test, and harder to debug than it needs to be for a lot of
real tasks. Plenty of problems are better solved with a **fixed sequence of LLM calls**
that a human designed — no loop, no autonomy, the model never decides "what happens next."
That's a **workflow**, and this folder has two of the most common ones.

## 1. Prompt chaining (`prompt_chain.py`)

Break one task into ordered steps, each a separate (smaller, more reliable) LLM call, with
a plain **Python** check — a "gate" — in between that can stop the chain early:

```
text ──▶ [Call 1: summarize] ──▶ summary ──▶ [Gate: is it short enough?]
                                                    │ no            │ yes
                                                    ▼                ▼
                                          stop, report          [Call 2: translate]
                                          gate_passed=False           │
                                                                        ▼
                                                              gate_passed=True
```

The gate (`PromptChainWorkflow._passes_gate`) is not an LLM call — it's an ordinary
`if len(summary.split()) <= max_summary_words`. That's the point: cheap, instant,
deterministic checks between expensive, non-deterministic model calls.

## 2. Routing (`router.py`)

Classify the input first, then hand it to a category-specific prompt instead of one prompt
trying to handle every case:

```
message ──▶ [Call 1: classify] ──▶ category ──▶ [Call 2: category's own system prompt] ──▶ response
```

If the classifier ever returns something that isn't one of the known categories,
`classify()` falls back to `"general"` instead of raising — a misrouted message should
degrade gracefully, not crash the whole workflow.

## Files

| File | Purpose |
|---|---|
| `prompt_chain.py` | `PromptChainWorkflow` — summarize → gate → translate |
| `router.py` | `RouterWorkflow` — classify → dispatch to a category's system prompt |
| `main.py` | CLI: `chain` and `route` subcommands |
| `tests/` | Offline tests (Anthropic client mocked); the chain tests specifically assert the *second* call never happens when the gate fails |

## Setup

```bash
pip install -r projects/ai_agents/requirements.txt   # from the repo root
cp projects/ai_agents/.env.example .env               # add your ANTHROPIC_API_KEY
```

## Run it

```bash
python -m projects.ai_agents.agent0_workflows.main chain "some long text to summarize" Spanish
python -m projects.ai_agents.agent0_workflows.main route "My payment failed twice today"
```

Run with no arguments and it defaults to the `chain` demo on a sample paragraph about
Python.

## Run the tests

```bash
python -m pytest projects/ai_agents/agent0_workflows/tests/ -v
```

## Things to try next

- Lower `max_summary_words` until the gate in `test_gate_rejects_long_summary_and_skips_translation`
  starts rejecting real summaries, and watch `main.py chain` report the rejection instead of
  crashing.
- Add a third stage to the chain (e.g. summarize → translate → shorten-to-one-sentence) and
  a second gate between the new steps.
- Add a fourth category to `router.py`'s `ROUTE_SYSTEM_PROMPTS` and update
  `CLASSIFY_SYSTEM_PROMPT`'s category list (it's generated from the dict, so nothing else
  needs to change).
- Once both feel familiar, go compare them to `agent2_react_reasoning`: same building
  blocks (a system prompt, a user message, parsing the reply), but agent2 keeps looping
  based on what the model says instead of following a fixed number of steps. That
  difference — fixed steps vs. model-decided steps — is the line between a workflow and
  an agent.
