# AI Agents — Learn Agentic AI in Python

**Tier**: Intermediate → Advanced | **Learning Path**: AI Agents & LLMs
**Prerequisites**: comfortable with Python classes, type hints, and JSON; helpful (not
required) to have done `projects/ai_agent_chatbot/` first.

This folder is a hands-on curriculum for the five ideas almost every "AI agent" you'll
meet is built from: **tool use**, **reasoning loops**, **multi-agent collaboration**,
**memory/RAG**, and **planning**. Each idea gets its own self-contained subfolder with
working code, its own README, and tests you can run with no API key at all.

> **What is an "agent," really?** In this module, an agent is just: an LLM call, inside
> a loop, that can affect something outside itself (run a tool, talk to another agent,
> read/write memory, execute a plan) and decide what to do next based on the result.
> Every agent here is that same idea wearing a different hat.

## The five agents

| # | Folder | Concept | One-line description |
|---|---|---|---|
| 1 | [`agent1_web_search/`](./agent1_web_search) | **Tool use** | The model decides when to search the web, reads the results, and answers with citations. |
| 2 | [`agent2_react_reasoning/`](./agent2_react_reasoning) | **ReAct reasoning** | The same "reason → act → observe" loop as Agent 1, written by hand with regex parsing instead of an API's `tools=` parameter. |
| 3 | [`agent3_multi_agent_team/`](./agent3_multi_agent_team) | **Multi-agent collaboration** | A Writer and a Reviewer pass drafts and feedback back and forth until a Coordinator (plain Python) is satisfied. |
| 4 | [`agent4_memory_rag/`](./agent4_memory_rag) | **Memory / RAG** | Answers are grounded in a small, from-scratch vector store (bag-of-words + cosine similarity) instead of the model's own knowledge. |
| 5 | [`agent5_planner_executor/`](./agent5_planner_executor) | **Planning & autonomy** | The model commits to a full multi-step plan up front; a separate executor works through it without checking back in. |

**Suggested order**: 1 → 2 → 3 → 4 → 5. Agents 1 and 2 teach the same idea two ways so you
can compare a framework-assisted loop to a hand-rolled one; 3-5 each add a new capability
on top of that base loop.

## Setup (once, for all five agents)

Run everything from the **repository root** (not from inside this folder — see
"Why `python -m`" below).

```bash
pip install -r projects/ai_agents/requirements.txt
cp projects/ai_agents/.env.example .env
# then edit .env and set ANTHROPIC_API_KEY
```

You need exactly one API key: **`ANTHROPIC_API_KEY`**, from
<https://console.anthropic.com/>. Agent 1 additionally installs `ddgs` for web search, but
that backend needs no API key of its own. Nothing else in this module talks to any other
external service.

Optional overrides (all have working defaults — see `.env.example`):

| Variable | Default | Used by |
|---|---|---|
| `ANTHROPIC_API_KEY` | *(required)* | all five agents |
| `AI_AGENTS_MODEL` | `claude-sonnet-5` | all five agents |
| `AI_AGENTS_MAX_TOKENS` | `1024` | all five agents |
| `AI_AGENTS_MEMORY_PATH` | `agent4_memory_rag/memory_store.json` | Agent 4 only |

Model IDs change over time — if `claude-sonnet-5` isn't valid for your account, check the
current list at <https://docs.anthropic.com/> and set `AI_AGENTS_MODEL` accordingly.

## Running an agent

Every agent is run the same way, as a module, from the repo root:

```bash
python -m projects.ai_agents.agent1_web_search.main "What is the latest stable Python release?"
python -m projects.ai_agents.agent2_react_reasoning.main "What is the capital of France, and what is 12 * 8?"
python -m projects.ai_agents.agent3_multi_agent_team.main "Why Python is a good first programming language"
python -m projects.ai_agents.agent4_memory_rag.main "What is projects/ai_agents?"
python -m projects.ai_agents.agent5_planner_executor.main "Explain a 20% tip on a $45.50 bill and save it to a file"
```

Run any of them with no arguments and it uses the sample question shown above, so you can
verify your setup works before writing your own prompt.

### Why `python -m ...` instead of `python main.py`?

Each agent imports shared code from `projects/utils/` and, in a couple of cases, from its
own sibling modules using absolute imports (`from projects.ai_agents.agent1_web_search...`).
That only resolves correctly if the **repository root** is on `sys.path`, which is exactly
what `python -m package.path.to.module` guarantees when run from the root. `cd`-ing into a
subfolder and running `python main.py` directly will raise `ModuleNotFoundError`.

## Running the tests

Every agent's tests mock the Anthropic client (and, for Agent 1, the search backend too),
so **none of them make network calls or need a real API key**:

```bash
python -m pytest projects/ai_agents/ -v
```

Or scope it to one agent while you're working on it:

```bash
python -m pytest projects/ai_agents/agent3_multi_agent_team/tests/ -v
```

## Repository conventions these agents follow

Consistent with the rest of this repo (see the root `CLAUDE.md` / `CONTRIBUTING.md`):

- Absolute imports rooted at `projects.` (not relative `from agent import ...`), so
  `pytest projects/` works from the repo root without any path hacks.
- Shared error handling via `projects/utils/errors.BaseProjectError` — every agent raises
  its own `AgentError` subclass rather than a bare exception.
- Shared logging via `projects/utils/logging_config.setup_logger()`.
- Google-style docstrings and type hints throughout.
- `tests/test_*.py`, class-based, one test class per unit under test.

## Cost and rate limits

Every `main.py` invocation makes at least one real API call once you supply a key (2+ for
Agents 3 and 5, since they coordinate multiple model calls per run). These are small
requests, but they are not free and are subject to your account's rate limits — the tests
never hit the API, but running the agents themselves does.

## Where to go from here

Each subfolder's README ends with a "Things to try next" section — those are the fastest
way to turn reading this code into understanding it. A natural next step after all five is
combining ideas: e.g. give the Agent 3 team a web-search tool (Agent 1), or make Agent 5's
planner re-plan using retrieved memory (Agent 4).
